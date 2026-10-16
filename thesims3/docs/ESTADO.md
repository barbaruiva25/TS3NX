# ESTADO — TS3NX (atualizar a cada rodada; nao inventar)

## 2026-10-14 (cadeia de boot) - default.xex virou o entrypoint; jogo e modulo
- Medido: 11 boots no PC (sims3.exe, 95 MB). Todos terminaram em `Execution complete` + `0xC0000374` (heap), nunca em codigo guest indefinido.
- Pesquisa (disassembly dos 3 XEX, ppc_mini.py sobre LOGS/*_image.bin): o CRT do Sims3.xex e beco sem saida - entry 0x88F12800 -> 0x88F126A8 -> main stub 0x887D3CF8 (`li r3,1; blr`). Quem chama o jogo e o default.xex: `sub_82040C10` = XexLoadImage("sims3.xex", flags=9) e `sub_82040BA0` = XexGetProcedureAddress(handle, 3) e (..., 1). Sem launch data do dashboard chama o **ord 1**; com 1020 bytes chama o **ord 3** com (buffer, 1020).
- Erro meu corrigido: a linha `F 820005C4 820A6F10 199 (409) XexLoadImage` do log do Xenia NAO e uma chamada, e a resolucao do simbolo do thunk de import (0x00010199 = registro da tabela de imports). Os unicos `bl` reais para XexLoadImage estao em 0x82040C28 e 0x820005C4-area de thunks.
- PrivLoader.xex: o default so compara a string "privloader.xex" (0x820B0054) em `sub_82040C58` para decidir a copia do launch data; o codigo do priv nao entra no caminho executado. Saiu do manifesto; os 3 overrides dele foram para overrides_priv.toml (enderecos 0x820xxxxx caem na faixa do default).
- Implementacao: sims3_manifest.toml agora tem default.xex como [entrypoint] e Sims3.xex como [[modules]] (guest_path "sims3.xex"); main.cpp includes sims3_default_init.h; sims3_app.h OnLoadXexImage -> game:\default.xex; OnConfigurePaths procura default.xex; hack da flag 0x89398418 e os hooks de redirecionamento para o ord 3 foram removidos (eram hipoteses da rota antiga).
- Mecanismo do SDK aprendido: o dispatcher chama `__imp__` direto; os hooks (wrappers weak) so pegam chamada entre funcoes guest. E `0x88F12800` nao tem DEFINE proprio (fundido em sub_88F126A8), por isso hook nele nunca disparava.

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
