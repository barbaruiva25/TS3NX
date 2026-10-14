# ETAPAS ATÉ O NRO DE TESTE — TS3NX (PTBR, base sem mods)

Ordem fixa. Uma etapa por vez, valide antes de avançar. Marque [x] conforme concluir.

## 0. Pré-requisitos do host

- [ ] Windows: LLVM clang 20 portátil + VS Build Tools + Python 3.13 (ok) + Git (ok)
- [ ] Instalar: CMake + Ninja + devkitA64 + libnx + switch-tools (pendente — `cmake`/`ninja` não encontrados em 13/10/2026)
- [ ] `gh auth login` para push (pendente)
- [ ] Espaço livre para objetos, ELF, mapa, NRO e evidências

## 1. Inventário (jogo intacto, só leitura)

- [x] Dump localizado: `../THE SIMS 3/THE SIMS 3 (XBOX360) JTAG-RGH`
- [x] Title ID 454108E2 confirmado no `default.xex` em 0x544
- [x] `Sims3.xex` 20.332.544 bytes, 64 `.package`, `Paul_World.world`, ~4,01 GB
- [ ] Registrar SHA-256 do `default.xex` / `Sims3.xex` em `thesims3/docs/HASHES.md`
- [ ] Confirmar PTBR: boot no Xenia/RGH com console em português (se PTBR -> trava BRA; senão -> buscar dump BRA)
- [ ] Preencher `thesims3/config/sims3-base.toml` com os XEX + módulos (`PrivLoader.xex` como [[modules]] se for guest carregado)

## 2. Codegen ReXGlue no PC

- [ ] Clang 20 + `tools/win/env.ps1` + `run.ps1`, `-march=x86-64-v2`, `fetch_thirdparty.py` nos symlinks
- [ ] `rexglue codegen thesims3/config/sims3-base.toml`
- [ ] Zerar "target not in any function" (cada um ganha [functions] + evidência)
- [ ] Varredura antes do boot + após cada codegen: `pointer_fixpoint.py` + `pointer_audit.py`, `switch_check.py`, setjmp/longjmp pela forma (store em r3 vs loads espelhados)

## 3. Boot PC emulado (`thesims3_renderer_native=false`)

- [ ] `tools/win/boot_test.ps1` mutado + minimizado, `-VideoAt N -VideoFrames M`
- [ ] MP4 + contact sheet (`make_video.sh`), `compare_video.py` contra referência
- [ ] Triagem: call não registrada = pointer/gap; access violation = simboliza `thesims3.exe+0xRVA` (llvm-symbolizer + `thesims3_crash_log.cpp`); hooks temporários de caller em arquivo debug
- [ ] Valida: boot, menu PTBR, CAS, modo vida, loading. Subagente audita crash em CÓPIA em paralelo

## 4. Renderer nativo PC (PM4 Vulkan via banjo-nx)

- [ ] `d3d_match.py` + `listing_diff.py` para achar D3D do XDK exato; hooks `SetDeviceShaderOffsets`, `NoteDrawCall(r3)`, dump VS/PS, flip
- [ ] Loop até 0 loads não identificados (`THESIMS3_SHADER_DISCOVERY`, `VERTEX_VARIANTS`, `SHADER_MISSING`), repara D3D, `wrap_discovered.py` só órfãos, `build_shader_library.sh` (XenosRecomp + DXC)
- [ ] `compare_video.py` nativo x emulado frame a frame; `banjo_trace_frame_s` + `THESIMS3_DUMP_TEXTURE` em cada diferença

## 5. PRIMEIRO NRO (o que você vai testar no Switch)

- [ ] Toolchain devkitA64 + libnx, sem `-march=native`, confere Cortex-A57 no `compile_commands.json` + `ninja -t graph` + desasm
- [ ] Começa por exemplo do `switch-examples`, depois liga runtime: arquivos, threads/TLS, tempo, mutex/atomics, guest x host, HOME/suspensão, input, áudio, saída que salva
- [ ] **Logs desde o primeiro NRO** + ZIP pronto pra raiz do SD: `switch/thesims3/thesims3.nro` + arquivos. Preserva saves/configs/caches do usuário. Modo aplicativo via title takeover (nunca Álbum). Telemetria: modelo, RAM, dock/portátil, clocks, build/save/área
- [ ] Percurso curto repetível: boot -> menu PTBR -> CAS -> entra no lote -> anda 30s -> salva -> sai pelo menu (salva config)

## 6. Gameplay correto antes de otimizar

- [ ] Mundo, personagens, HUD, menus, streaming de `.package`, saves `.sims3` funcionando
- [ ] Sem prometer "todos os shaders": catálogo versionado + pré-warm no loading + continua registrando variantes

## 7. Otimizações (só medidas no aparelho, pixel-idênticas via `compare_video.py`)

- [ ] Resolução interna/HUD/swapchain separados, MSAA, blur/SSAO/bloom, sombras, LOD, frustum/backface, frente->fundo, occlusion conservador, batching
- [ ] Memória como orçamento (BSS/PGO, guest, heap, stacks, VMA, temporária) + histerese + testes de ciclo
- [ ] LTO verificado no grafo + PGO GENERATE -> perfil -> USE, cada um com evidência de ganho sem regressão
- [ ] ZIP final de release + `ESTADO.md` atualizado (pesquisa x hipótese x implementação x medido)

## Telemetria mínima por teste no aparelho

Modelo + RAM ao processo + dock/portátil + clocks CPU/GPU/MEM + build + save/área/percurso + clocks efetivos. Sem isso, sem comparar FPS.
