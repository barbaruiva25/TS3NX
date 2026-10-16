// The Sims 3 (Xbox 360): ponto de entrada da aplicacao.
//
// sims3_init.h vem do codegen do ENTRYPOINT (default.xex, generated/default):
// e ele que declara PPCImageConfig (com register_modules, que o ReXApp chama
// antes do launch) e a tabela de registros do modulo carregado como
// executavel. O jogo (Sims3.xex) e um modulo DLL em generated/sims3, com alvo
// proprio (sims3_Sims3) criado por generated/default/dll_targets.cmake.

#include "sims3_init.h"

#include "sims3_app.h"

REX_DEFINE_APP(sims3, sims3App::Create)
