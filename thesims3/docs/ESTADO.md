# ESTADO ÔÇö TS3NX (atualizar a cada rodada; n├úo inventar)

## 2026-10-14 (app scaffold) ÔÇö codegen-05 limpo, CMake configurando
- Medido: codegen-05 exit 0 em ~221s (527 escritos, 0 erros) com manifesto em thesims3/; glue em generated/rexglue.cmake.
- Implementa├º├úo: thesims3/CMakeLists.txt (rexglue_setup_target + xenos + ffp-contract), main/app/language-PTBR/VFS/input. Configure PC em andamento (vcvars + clang + Ninja).
- Pr├│ximo: build thesims3.exe, boot emulado.
- Medido: pass1 33.096 gaps, 414 candidatos, 395 aceitos; pass2 sem candidatos novos. Codegen real ap├│s pass1 limpo (sem sys.exit). overrides.toml com 395 entradas + evid├¬ncia. Commit 0374b54 no ar.
- Audit: 238 vtable-like triados pelo fixpoint (gap) ou j├í dentro de corpos (sem entrada necess├íria).
- setjmp/longjmp: 0 pela forma ÔÇö pendente de runtime, sem inven├º├úo.
- Pr├│ximo: app harness (CMake + runtime) p/ thesims3.exe e boot emulado.
- Medido: codegen-03 exit 0 em 104s, 527 escritos, 0 erros. Faixa de c├│digo 0x88290000ÔÇô0x8925F2A8. Nota: fun├º├úo 0x88DDA818 tem 1.077.424 B (> 1 MB por arquivo; gerador concluiu).
- Implementa├º├úo: `ferramentas/switch_check.py` no repo; varredura da faixa em andamento (log em LOGS/switch_check.log).
- Pendente: pointer_fixpoint/audit, setjmp/longjmp por forma, app CMake p/ thesims3.exe, boot PC, NRO.
- Implementa├º├úo: `ferramentas/extract_iso.py` adaptado do fc3-nx (mesma conta, GPL-3.0) + THIRD_PARTY_NOTICES.md. Teste: `--info` no Sims3.xex sai exit 0 com os mesmos n├║meros do script original.
- Medido: default.xex base 0x82000000 entry 0x82041028 (loader 1,4 MB); Sims3.xex base 0x88000000 entry 0x88F12800 (jogo, 21,5 MB) = entrada do codegen; PrivLoader base 0x82000000 entry 0x82010510 (fora do manifesto). Todos 454108E2 / media 21CDDF46 / v0.0.0.4 / AES-128+basic.
- Pendente: teste PTBR no Xenia/RGH, SDK rexglue + toolchain (clang/CMake/Ninja/devkit) p/ codegen e boot. Sem Xenia instalado: boot real ainda n├úo test├ível aqui.
- Implementa├º├úo: SHA-256 dos 3 XEX registrados em HASHES.md; INVENTARIO.md com loader/principal/PrivLoader, mundo Paul_World (Moonlight Bay), 64 .package, 4,01 GB.
- Pesquisa (subagente): port 360 pela Edge of Reality; console tem loadings entre ├íreas (diferente do PC); edi├º├úo BR com menus/legendas PT-BR (UOL 06/10/2010); idioma segue o console; sem prova de PT-BR em todo NTSC-U.
- Hip├│tese mantida: textos comprimidos no UI.package; PTBR s├│ se confirma com boot em console PTBR.
- Medido: busca XexLoadImage/PrivLoader em Sims3.xex = 0 (XEX cifrado; precisa descriptografar antes de decidir [[modules]]). PrivLoader fora do manifesto por enquanto.
- Pendente: teste PTBR no Xenia/RGH, descriptografia p/ imports, codegen.
- Pesquisa: dump `THE SIMS 3 (XBOX360) JTAG-RGH` lido s├│-leitura. Title ID 454108E2 confirmado (default.xex @0x544). Sims3.xex 20.332.544 B. 64 .package + Paul_World.world, ~4,01 GB.
- Hip├│tese: textos PTBR est├úo comprimidos no UI.package; ficha "Multi" n├úo prova BRA.
- Implementa├º├úo: pastas + .gitignore + README + ETAPAS-NRO + manifesto base + VFS/locale stub + toolchain switch stub. Git local a iniciar.
- Medido: nada ainda (sem clang/CMake/Ninja/devkitA64 no host; gh sem login).
- Pendente: SHA-256, teste PTBR no Xenia/RGH, codegen, boot PC, NRO.
- Sem descoberta nova de otimiza├º├úo nesta rodada.
