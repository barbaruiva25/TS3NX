# PLANO — TS3NX (The Sims 3 360 -> PC -> Switch, base PTBR sem mods)

Espelha o `fc3-nx` (mesma conta `barbaruiva25`): mesmo SDK ReXGlue, mesmas ferramentas, renderer PM4 Vulkan via banjo-nx.
O específico do Sims 3 é manifesto, análises e VFS de `.package`/`.world` + locale BRA.

## Fase 1 — PC emulado (atual)
1. SHA-256 dos XEX + `HASHES.md`
2. `sims3-base.toml` final (PrivLoader como [[modules]] só com evidência de XexLoadImage)
3. codegen + zerar "target not in any function"
4. sweep ponteiros/jump-tables/setjmp + boot emulado + vídeo de referência

## Fase 2 — Renderer nativo PC
D3D do XDK exato, shader library zerada, `compare_video.py` sem diferença em boot/menu/CAS/vida/loading.

## Fase 3 — Primeiro NRO
devkitA64, logs desde o boot, ZIP `switch/thesims3/thesims3.nro`, title takeover, percurso curto PTBR.

## Fase 4 — Gameplay + otimizações medidas
Só depois do gameplay correto. Tudo pixel-idêntico e medido no aparelho. LTO/PGO com evidência.
