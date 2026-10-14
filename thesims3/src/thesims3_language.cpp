// The Sims 3: idioma do jogo. O jogo escolhe textos e menus pelo idioma do
// sistema (XGetLanguage), que o SDK responde a partir de user_language.
// "brazilian" e o padrao deste projeto (jogo em PTBR, versao base sem mods);
// "auto" segue o idioma do console (no PC, o idioma de exibicao do Windows).
//
// Ids de idioma do Xbox 360 (XLanguage): 1 ingles, 2 japones, 3 alemao,
// 4 frances, 5 espanhol, 6 italiano. Portugues (Brasil) = 13, A CONFIRMAR no
// primeiro boot: ler o id no log do jogo rodando e corrigir este comentario.
// O Xenia responde ingles; por isso o teste de PTBR exige console RGH em
// portugues ou inspecao dos recursos de idioma do UI.package.

#include "thesims3_language.h"

#include <cctype>
#include <string>

#include <rex/cvar.h>
#include <rex/logging.h>

#if defined(__SWITCH__)
#include <switch.h>
#elif defined(_WIN32)
#define WIN32_LEAN_AND_MEAN
#define NOMINMAX
#include <windows.h>
#endif

REXCVAR_DEFINE_STRING(language, "brazilian", "sims3",
                      "Idioma do jogo: brazilian (padrao), auto (idioma do sistema), english, "
                      "japanese, french, german, spanish, italian, portuguese");

namespace sims3::language {
namespace {

constexpr unsigned kEnglish = 1, kJapanese = 2, kGerman = 3, kFrench = 4, kSpanish = 5, kItalian = 6;
constexpr unsigned kPortugueseBR = 13;  // TODO: confirmar no log do primeiro boot

unsigned SystemLanguage() {
#if defined(__SWITCH__)
  unsigned id = kPortugueseBR;  // padrao do projeto: PTBR mesmo sem leitura do sistema
  if (R_SUCCEEDED(setInitialize())) {
    u64 code = 0;
    SetLanguage language = SetLanguage_ENUS;
    if (R_SUCCEEDED(setGetSystemLanguage(&code)) && R_SUCCEEDED(setMakeLanguage(code, &language))) {
      switch (language) {
        case SetLanguage_JA: id = kJapanese; break;
        case SetLanguage_FR:
        case SetLanguage_FRCA: id = kFrench; break;
        case SetLanguage_DE: id = kGerman; break;
        case SetLanguage_IT: id = kItalian; break;
        case SetLanguage_ES:
        case SetLanguage_ES419: id = kSpanish; break;
        case SetLanguage_PTBR: id = kPortugueseBR; break;
        default: id = kPortugueseBR; break;
      }
    }
    setExit();
  }
  return id;
#elif defined(_WIN32)
  switch (PRIMARYLANGID(GetUserDefaultUILanguage())) {
    case LANG_JAPANESE: return kJapanese;
    case LANG_FRENCH: return kFrench;
    case LANG_GERMAN: return kGerman;
    case LANG_SPANISH: return kSpanish;
    case LANG_ITALIAN: return kItalian;
    case LANG_PORTUGUESE: return kPortugueseBR;
    default: return kPortugueseBR;  // padrao do projeto
  }
#else
  return kPortugueseBR;
#endif
}

}  // namespace

void Apply() {
  std::string name = REXCVAR_GET(language);
  for (char& c : name) c = char(std::tolower(static_cast<unsigned char>(c)));
  unsigned id = 0;
  if (name == "english") id = kEnglish;
  else if (name == "japanese") id = kJapanese;
  else if (name == "french") id = kFrench;
  else if (name == "german") id = kGerman;
  else if (name == "spanish") id = kSpanish;
  else if (name == "italian") id = kItalian;
  else if (name == "brazilian" || name == "portuguese") id = kPortugueseBR;
  else {
    if (name != "auto") REXLOG_WARN("language = \"{}\" desconhecido: auto e usado", name);
    id = SystemLanguage();
  }
  rex::cvar::SetFlagByName("user_language", std::to_string(id));
  REXLOG_INFO("language: {} (Xbox language {})", name, id);
}

}  // namespace sims3::language
