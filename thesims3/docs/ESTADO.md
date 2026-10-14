# ESTADO — TS3NX (atualizar a cada rodada; não inventar)

## 2026-10-13 — Andaime criado + inventário parcial
- Pesquisa: dump `THE SIMS 3 (XBOX360) JTAG-RGH` lido só-leitura. Title ID 454108E2 confirmado (default.xex @0x544). Sims3.xex 20.332.544 B. 64 .package + Paul_World.world, ~4,01 GB.
- Hipótese: textos PTBR estão comprimidos no UI.package; ficha "Multi" não prova BRA.
- Implementação: pastas + .gitignore + README + ETAPAS-NRO + manifesto base + VFS/locale stub + toolchain switch stub. Git local a iniciar.
- Medido: nada ainda (sem clang/CMake/Ninja/devkitA64 no host; gh sem login).
- Pendente: SHA-256, teste PTBR no Xenia/RGH, codegen, boot PC, NRO.
- Sem descoberta nova de otimização nesta rodada.
