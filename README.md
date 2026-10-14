# TS3NX — The Sims 3 (Xbox 360, Title ID 454108E2) para PC e Switch

Port por recompilação estática ReXGlue (PPC Xbox 360 -> C++) + runtime Horizon.
**Versão base, sem mods. Jogo e comunicação em PTBR.**

## Pastas

| Pasta | O que vai aqui |
|---|---|
| `inputs/` | VAZIO no git. Aponta para seu dump em `../THE SIMS 3/THE SIMS 3 (XBOX360) JTAG-RGH`. Nunca copiar jogo pra cá |
| `referencias/` | Links/fontes consultadas, versões, hashes |
| `ferramentas/` | Scripts do host (inventário, checagens) |
| `thesims3/src/` | Runtime: VFS, locale PTBR, hooks, renderer, áudio, input |
| `thesims3/generated/` | Saída do ReXGlue (ignorado no git) |
| `thesims3/runtime/` | Camada libnx/Horizon |
| `thesims3/toolchains/` | `switch.cmake` (devkitA64) + `windows.cmake` |
| `thesims3/config/` | Manifestos ReXGlue por versão do disco |
| `thesims3/tests/` | Percurso curto de teste + saves de referência |
| `thesims3/docs/` | Estado, etapas, medidas |
| `thesims3/LOGS/` | Logs copiados do console pelo usuário |
| `thesims3/out/` | Builds locais + ZIPs (ignorados) |
| `thesims3/evidence/hardware/` | Medidas por sessão no aparelho |

## Dump validado (13/10/2026)

- `default.xex` Title ID **454108E2** em `0x544` (confirmado)
- `Sims3.xex` 20.332.544 bytes (executável principal), `PrivLoader.xex` loader
- 64 `.package` DBPF + `Paul_World.world` + `Shaders_Xenon.precomp`, total ~4,01 GB
- PTBR: **não confirmado** em texto plano (textos ficam comprimidos no `UI.package`). Testar com console em PTBR no Xenia/RGH; se abrir em PTBR, trava locale BRA, senão precisa de dump BRA

## Como usar com OpenCode (otimizado)

- Trabalhe **uma etapa por vez** de `thesims3/docs/ETAPAS-NRO.md`, valide antes de avançar
- Use subagentes em paralelo: um continua o caminho principal, outro audita classes de crash em CÓPIA da árvore
- Todo teste PC: mutado + minimizado, nunca toma o desktop
- Todo teste Switch: entrega ZIP `switch/thesims3/thesims3.nro` + arquivos, preserva saves do usuário
- Cada análise carrega evidência; reporte também o não verificado
- Atualize `thesims3/docs/ESTADO.md` a cada rodada (pesquisa x hipótese x implementação x medido)

## Etapas até o NRO — resumo

Ver detalhe em `thesims3/docs/ETAPAS-NRO.md`. Ordem: inventário -> codegen PC -> boot emulado -> renderer nativo PC -> primeiro NRO com logs -> gameplay -> otimizações medidas -> ZIP final.

## GitHub

Repositório: `https://github.com/barbaruiva25/TS3NX` (mesma conta do `fc3-nx`).
Sem dado do jogo. Remote `origin` já configurado.
Para publicar: `gh auth login` e depois `gh repo create TS3NX --public --source=. --remote=origin --push` (ou crie `TS3NX` vazio no site e `git push -u origin main`).
