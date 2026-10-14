# ESTADO — TS3NX (atualizar a cada rodada; não inventar)

## 2026-10-14 (fixpoint) — +395 funções, convergiu
- Medido: pass1 33.096 gaps, 414 candidatos, 395 aceitos; pass2 sem candidatos novos. Codegen real após pass1 limpo (sem sys.exit). overrides.toml com 395 entradas + evidência. Commit 0374b54 no ar.
- Audit: 238 vtable-like triados pelo fixpoint (gap) ou já dentro de corpos (sem entrada necessária).
- setjmp/longjmp: 0 pela forma — pendente de runtime, sem invenção.
- Próximo: app harness (CMake + runtime) p/ thesims3.exe e boot emulado.
- Medido: codegen-03 exit 0 em 104s, 527 escritos, 0 erros. Faixa de código 0x88290000–0x8925F2A8. Nota: função 0x88DDA818 tem 1.077.424 B (> 1 MB por arquivo; gerador concluiu).
- Implementação: `ferramentas/switch_check.py` no repo; varredura da faixa em andamento (log em LOGS/switch_check.log).
- Pendente: pointer_fixpoint/audit, setjmp/longjmp por forma, app CMake p/ thesims3.exe, boot PC, NRO.
- Implementação: `ferramentas/extract_iso.py` adaptado do fc3-nx (mesma conta, GPL-3.0) + THIRD_PARTY_NOTICES.md. Teste: `--info` no Sims3.xex sai exit 0 com os mesmos números do script original.
- Medido: default.xex base 0x82000000 entry 0x82041028 (loader 1,4 MB); Sims3.xex base 0x88000000 entry 0x88F12800 (jogo, 21,5 MB) = entrada do codegen; PrivLoader base 0x82000000 entry 0x82010510 (fora do manifesto). Todos 454108E2 / media 21CDDF46 / v0.0.0.4 / AES-128+basic.
- Pendente: teste PTBR no Xenia/RGH, SDK rexglue + toolchain (clang/CMake/Ninja/devkit) p/ codegen e boot. Sem Xenia instalado: boot real ainda não testável aqui.
- Implementação: SHA-256 dos 3 XEX registrados em HASHES.md; INVENTARIO.md com loader/principal/PrivLoader, mundo Paul_World (Moonlight Bay), 64 .package, 4,01 GB.
- Pesquisa (subagente): port 360 pela Edge of Reality; console tem loadings entre áreas (diferente do PC); edição BR com menus/legendas PT-BR (UOL 06/10/2010); idioma segue o console; sem prova de PT-BR em todo NTSC-U.
- Hipótese mantida: textos comprimidos no UI.package; PTBR só se confirma com boot em console PTBR.
- Medido: busca XexLoadImage/PrivLoader em Sims3.xex = 0 (XEX cifrado; precisa descriptografar antes de decidir [[modules]]). PrivLoader fora do manifesto por enquanto.
- Pendente: teste PTBR no Xenia/RGH, descriptografia p/ imports, codegen.
- Pesquisa: dump `THE SIMS 3 (XBOX360) JTAG-RGH` lido só-leitura. Title ID 454108E2 confirmado (default.xex @0x544). Sims3.xex 20.332.544 B. 64 .package + Paul_World.world, ~4,01 GB.
- Hipótese: textos PTBR estão comprimidos no UI.package; ficha "Multi" não prova BRA.
- Implementação: pastas + .gitignore + README + ETAPAS-NRO + manifesto base + VFS/locale stub + toolchain switch stub. Git local a iniciar.
- Medido: nada ainda (sem clang/CMake/Ninja/devkitA64 no host; gh sem login).
- Pendente: SHA-256, teste PTBR no Xenia/RGH, codegen, boot PC, NRO.
- Sem descoberta nova de otimização nesta rodada.
