param([switch]$Quiet)
# Sem $ErrorActionPreference=Stop: o rexglue escreve progresso em stderr e o
# PowerShell trataria isso como excecao. Tudo passa por cmd /c + arquivo de log.
$root = 'C:\Users\barba\Documents\xbox360\TS3NX'
Set-Location $root
$rexglue = "$root\..\FARCRY3\xbox360\fc3-nx\sdk\out\win-amd64\rexglue.exe"

# 1. codegen (o alvo do build tambem roda isto; aqui para ter log proprio)
Write-Host '[1/4] codegen'
cmd /c "`"$rexglue`" codegen `"$root\thesims3\sims3_manifest.toml`" > `"$root\thesims3\LOGS\codegen-chain.log`" 2>&1"
$codegen = $LASTEXITCODE
Write-Host "      codegen=$codegen"

# 2. reparos cross-file (o gerador os apaga; --check nao repara nada)
Write-Host '[2/4] post_codegen'
cmd /c "python `"$root\ferramentas\post_codegen.py`" > `"$root\thesims3\LOGS\post-codegen.log`" 2>&1"
Write-Host "      post_codegen=$LASTEXITCODE (ultimas:)"
Get-Content "$root\thesims3\LOGS\post-codegen.log" -Tail 2 | ForEach-Object { "      $_" }

# 3. carimba os stamps DEPOIS do reparo: sem isso o ninja re-executa o codegen
#    no proximo build (o alvo sims3_codegen) e apaga os reparos de novo.
Write-Host '[3/4] touch dos stamps'
Get-ChildItem "$root\thesims3\generated" -Recurse -Filter 'codegen.build.stamp' |
    ForEach-Object { $_.LastWriteTime = Get-Date; "      $($_.Name)" }

# 4. build
Write-Host '[4/4] build'
cmd /c "`"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat`" >NUL && set `"PATH=C:\Program Files\LLVM\bin;%PATH%`" && python -m cmake --build `"$root\thesims3\out\pc`" --parallel 12 > `"$root\thesims3\LOGS\pc-build.log`" 2>&1"
$build = $LASTEXITCODE
Write-Host "      build=$build"
if (-not $Quiet -and $build -ne 0) {
    Select-String -Path "$root\thesims3\LOGS\pc-build.log" -Pattern 'error' |
        Select-Object -First 8 | ForEach-Object { "      $($_.Line)" }
}
if ($codegen -ne 0 -or $build -ne 0) { exit 1 }