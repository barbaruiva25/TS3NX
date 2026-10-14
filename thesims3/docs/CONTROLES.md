# CONTROLES — TS3NX (The Sims 3 é jogo de mouse; o mapeamento cobre isso)

Segue o layout padrão do Switch. Implementação: `thesims3/src/thesims3_input.*`
(`__SWITCH__` via libnx `hid:*`; PC via mouse/teclado + SDL para genéricos).

## Mapa padrão (Pro Controller e par Joy-Con)

| Ação no Sims 3 | Pro / Joy-Con (par) | Touchscreen | PC (genérico SDL + mouse) |
|---|---|---|---|
| Mover cursor | Stick direito (relativo, com aceleração) | Toque = cursor absoluto | Mouse |
| Clique esquerdo | A ou R (ou toque) | Toque curto | Botão esquerdo / botão 0 do pad |
| Clique direito (girar câmera) | B ou ZR segurar + stick | Toque longo | Botão direito / botão 1 |
| Arrastar | A segurar + stick / toque arrastar | Arrastar 1 dedo | Arrastar |
| Zoom | ZL/ZR (ou +/-) | Pinça 2 dedos | Roda / botões 4-5 |
| Girar câmera | L/R | Girar 2 dedos (fase 2) | Q/E ou botão direito + mouse |
| Pausar / velocidade 1-2-3 | Plus (pausa), Minus (ciclo velocidade) | Botões HUD (fase 2) | P / 1-2-3 |
| Confirmar / cancelar menus | A / B | Toque / gesto voltar | Enter / Esc |
| D-pad | Atalhos (necessidades, trabalho, mapa) | — | Setas |
| Stick esquerdo | Rolagem da câmera / WASD | — | WASD |
| SL/SR, captura | Padrão do sistema, sem remapeamento | — | — |

## Regras
- Joy-Con solto (1 unidade): mapa mínimo (cursor + A/B + Plus/Minus); sem recursos exclusivos.
- Controles genéricos no PC: SDL_GameController com o mapa acima; no Switch, só estilos
  libnx (`Handheld`, `JoyDual`, `JoyLeft/Right`, `ProController`).
- Deadzone de sticks configurável; toque com debounce; nada de gestos que conflitem
  com HOME/suspensão.
- Telemetria de input (estilo ativo, toques/s) entra no log de sessão para diagnóstico.
