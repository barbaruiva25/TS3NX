# Roda o thesims3.exe por alguns segundos, para, e mostra o fim do log.
# Sempre mutado + minimizado (nunca toma o desktop). Nunca canalizar para
# Select-Object -First (o pipe fechado deixaria o jogo rodando).
param(
    [int]$Seconds = 60,
    [string]$Exe = 'out\pc\sims3.exe',
    [int]$Tail = 40
)
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\thesims3')).Path
$exePath = (Join-Path $root $Exe)
$dir = Split-Path $exePath
$game = 'C:\Users\barba\Documents\xbox360\THE SIMS 3\THE SIMS 3 (XBOX360) JTAG-RGH'
Get-CimInstance Win32_Process -Filter "Name='$(Split-Path $exePath -Leaf)'" -ErrorAction SilentlyContinue |
    Where-Object { $_.ExecutablePath -eq $exePath } | ForEach-Object {
        Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
        Wait-Process -Id $_.ProcessId -Timeout 20 -ErrorAction SilentlyContinue
    }
$started = Get-Date
$env:REX_AUDIO_MUTE = 'true'
$env:REX_WINDOW_START_MINIMIZED = 'true'
$p = Start-Process -FilePath $exePath -ArgumentList "--game_data_root=`"$game`"" -WorkingDirectory $dir -PassThru -WindowStyle Minimized
$p.WaitForExit($Seconds * 1000) | Out-Null
if ($p.HasExited) {
    '{0} saiu apos {1:n1} s com codigo 0x{2:X8}' -f (Split-Path $exePath -Leaf), ((Get-Date) - $started).TotalSeconds, $p.ExitCode
} else {
    $p.Refresh()
    'rodando apos {0} s: cpu {1:n1} s, memoria {2} MB; parado' -f $Seconds, $p.TotalProcessorTime.TotalSeconds, [math]::Round($p.WorkingSet64 / 1MB)
    Stop-Process -Id $p.Id -Force
    if (-not $p.WaitForExit(20000)) { "(aviso: processo $($p.Id) nao saiu em 20 s)" }
}
$log = Get-ChildItem (Join-Path $dir 'logs') -Filter *.log -ErrorAction SilentlyContinue |
    Where-Object { $_.LastWriteTime -ge $started.AddSeconds(-2) } | Sort-Object LastWriteTime | Select-Object -Last 1
if ($log) {
    "== $($log.FullName) ($($log.Length) bytes)"
    Get-Content $log.FullName -Tail $Tail
} else {
    'sem log escrito'
}
