// thesims3_input.h — entrada do TS3NX (PTBR, base sem mods).
// Switch (libnx): par Joy-Con, Joy-Con solto, Pro Controller + touchscreen.
// PC: mouse/teclado + SDL para controles genericos. Sem remapeamento de botoes do sistema.
#pragma once

// Acoes logicas do jogo (mouse + atalhos do Sims 3).
enum class Sims3Action {
  CursorMove,     // relativo (stick) ou absoluto (toque)
  ClickLeft,
  ClickRight,
  DragBegin,
  DragEnd,
  ZoomIn,
  ZoomOut,
  RotateLeft,
  RotateRight,
  Pause,
  SpeedCycle,     // 1 -> 2 -> 3
  Confirm,
  Cancel,
  Shortcut0,      // D-pad: necessidades, trabalho, mapa...
  Shortcut1,
  Shortcut2,
  Shortcut3,
  CameraScroll,   // stick esquerdo / WASD
};

// Estado amostrado por frame.
struct Sims3InputState {
  float cursor_dx = 0.f;   // relativo (stick); ignorado com toque absoluto
  float cursor_dy = 0.f;
  float cursor_x = -1.f;   // absoluto normalizado 0..1 (<0 = sem toque)
  float cursor_y = -1.f;
  bool touch_down = false;
  unsigned pressed = 0;    // bit por Sims3Action (usa 1u << (int)acao)
  float scroll_x = 0.f;
  float scroll_y = 0.f;
};

void thesims3_input_init();
void thesims3_input_poll(Sims3InputState& out);  // Switch: hidScanInput + touch; PC: SDL/mouse
void thesims3_input_shutdown();
