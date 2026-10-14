// thesims3_input.cpp — andaime (implementacao completa na fase do app Switch/PC).
// Regras: estilos libnx Handheld/JoyDual/JoyLeft/JoyRight/ProController;
// Joy-Con solto = mapa minimo; deadzone configuravel; debounce de toque;
// nao tocar em SL/SR/HOME; telemetria de estilo ativo vai ao log de sessao.
#include "thesims3_input.h"

void thesims3_input_init() {
#if defined(__SWITCH__)
  // TODO(fase Switch): hidInitialize + padConfigureInput + estilos Npad
  // (Handheld, JoyDual, JoyLeft, JoyRight, ProController); toque via
  // hidGetTouchScreenStates. Ver thesims3/docs/CONTROLES.md.
#else
  // TODO(fase PC): mouse/teclado + SDL_GameController (mapa CONTROLES.md).
#endif
}

void thesims3_input_poll(Sims3InputState& out) {
  (void)out;
  // TODO: preencher conforme CONTROLES.md (stick direito = cursor relativo com
  // aceleracao; toque = absoluto; A/R = clique esquerdo; B/ZR = direito;
  // ZL/ZR = zoom; Plus = pausa; Minus = ciclo de velocidade).
}

void thesims3_input_shutdown() {}
