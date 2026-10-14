# ESTADO — TS3NX (atualizar a cada rodada; não inventar)

## 2026-10-14 — Hashes + inventário profundo
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
