# ESTADO — TS3NX (atualizar a cada rodada; nao inventar)

## 2026-10-14 (configure PC) — CMake OK, aguardando codegen-06
- Medido: configure exit 0 em 185s (SDK 0.10.0-dev, win-amd64, Clang 23.1.3, build em thesims3/out/pc). GPU emulada via D3D12 no stage 1.
- Codegen-06 rodando (glue+codigo no lugar certo); build do thesims3.exe so depois dele.
- GitHub limpo apos reversao do commit gordo (force-push 78e3265). Licao: manifesto movido exige revisar relativos + git status antes de add -A.

## 2026-10-14 (app scaffold) — codegen-05 limpo
- Medido: codegen-05 exit 0 (527 escritos, 0 erros) com manifesto em thesims3/; glue em generated/rexglue.cmake.
- Implementacao: thesims3/CMakeLists.txt (rexglue_setup_target + xenos + ffp-contract), main/app/language-PTBR/VFS/input.

## 2026-10-14 (fixpoint) — +395 funcoes, convergiu
- Medido: pass1 33.096 gaps, 414 candidatos, 395 aceitos; pass2 sem candidatos novos. Codegen real apos pass1 limpo. overrides.toml com 395 entradas + evidencia.
- Audit: 238 vtable-like triados pelo fixpoint (gap) ou ja dentro de corpos (sem entrada necessaria).
- setjmp/longjmp: 0 pela forma — pendente de runtime, sem invencao.

## 2026-10-14 (codegen zerado) — 527 arquivos, 63.969 funcoes
- Medido: codegen-03 exit 0 em 104s. Faixa de codigo 0x88290000-0x89260678. Funcao 0x88DDA818 tem 1.077.424 B (> 1 MB; gerador concluiu).
- Switches: 0 truncadas/erradas/perdidas (SWITCHES.md); 8 "sem bound" revisadas a mao.
- Xenia: dump boota, Sims3.xex executa, XGetLanguage em 0x8925F77C (BOOT-XENIA.md). PTBR pendente de console real.

## Dump validado
- Title ID 454108E2, media 21CDDF46, v0.0.0.4. default.xex (loader 0x82000000) + Sims3.xex (jogo 0x88000000, entry 0x88F12800) + PrivLoader.xex (fora do manifesto). SHA-256 em HASHES.md.
