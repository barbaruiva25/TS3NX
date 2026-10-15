// The Sims 3: o objeto de aplicacao ReXGlue (caminhos, GPU, idioma, ajudas de analise).

#pragma once

#include <cstdio>
#include <cstdlib>
#include <filesystem>
#include <system_error>

#include <rex/cvar.h>
#include <rex/filesystem.h>
#include <rex/logging.h>
#include <rex/rex_app.h>
#include <rex/runtime.h>

#include "thesims3_language.h"
#include "thesims3_vfs.h"

class sims3App : public rex::ReXApp {
 public:
  using rex::ReXApp::ReXApp;

  static std::unique_ptr<rex::ui::WindowedApp> Create(rex::ui::WindowedAppContext& ctx) {
    return std::unique_ptr<sims3App>(new sims3App(ctx, "sims3", PPCImageConfig));
  }

  void OnPostInitLogging() override {
    // GPU emulada por padrao (thesims3_renderer_native = false); o renderer
    // nativo entra na fase 4. Escolha explicita por linha de comando/config vence.
    if (!rex::cvar::HasNonDefaultValue("gpu_plugin")) {
      rex::cvar::SetFlagByName("gpu_plugin", "xenos");
    }
    // Idioma do jogo (sims3.toml "language"; padrao brazilian): antes de o jogo perguntar.
    sims3::language::Apply();
  }

  // Ponto de entrada: Sims3.xex (o jogo; default.xex e so o loader do disco).
  void OnLoadXexImage(std::string& xex_image) override { xex_image = "game:\\Sims3.xex"; }

  // Sem --game_data_root, procura game_root/ ao lado do executavel (dump
  // JTAG-RGH com Sims3.xex na raiz). Caminho explicito sempre vence.
  void OnConfigurePaths(rex::PathConfig& paths) override {
    if (!paths.game_data_root.empty()) {
      return;
    }
    std::error_code ec;
    const auto folder = rex::filesystem::GetExecutableFolder();
    if (folder.empty()) {
      return;
    }
    for (auto candidate = folder; !candidate.empty(); candidate = candidate.parent_path()) {
      for (const auto& sub : {std::filesystem::path("game_root")}) {
        if (std::filesystem::is_regular_file(candidate / sub / "Sims3.xex", ec)) {
          paths.game_data_root = candidate / sub;
          return;
        }
      }
      if (candidate == candidate.parent_path()) {
        break;
      }
    }
  }

  // O loader original (default.xex -> privloader.xex) prepara o jogo antes do
  // entry: com r4==0 o entry so prossegue se *(0x89398418) != 0
  // (lis 0x893A0000 + lwz -31720 em 0x88F126D4; o init incrementa ali).
  // No HW o privloader (loader manual) deixa essa flag armada; aqui o entry
  // recebe r4==0 e a flag nasce zerada -> exit imediato. Replica o efeito
  // observavel: flag != 0 antes do launch. TODO: confirmar valor exato no HW.
  void OnPreLaunchModule() override {
    auto* mem = runtime() ? runtime()->memory() : nullptr;
    if (!mem) {
      return;
    }
    if (uint8_t* host = mem->TranslateVirtual<uint8_t*>(0x89398418)) {
      host[0] = 0;
      host[1] = 0;
      host[2] = 0;
      host[3] = 1;
      REXLOG_INFO("launch: flag 0x89398418 armada (privloader)");
    }
  }
  // carregada para varredura de ponteiros (ferramentas/pointer_scan.py).
  void OnPostLoadXexImage() override {
    if (!runtime() || !runtime()->memory()) {
      return;
    }
    const char* path = std::getenv("sims3_DUMP_IMAGE");
    if (!path) {
      return;
    }
    const uint8_t* image =
        runtime()->memory()->TranslateVirtual<const uint8_t*>(PPCImageConfig.image_base);
    if (std::FILE* f = std::fopen(path, "wb")) {
      std::fwrite(image, 1, PPCImageConfig.image_size, f);
      std::fclose(f);
      REXLOG_INFO("guest image written to {}", path);
    }
  }
};
