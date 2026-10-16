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

  // Ponto de entrada: default.xex, o loader da midia. Ele carrega Sims3.xex
  // (XexLoadImage em sub_82040C10) e chama os exports 1 e 3 do jogo; o CRT do
  // Sims3.xex e beco sem saida (main stub), por isso nao serve de entry.
  void OnLoadXexImage(std::string& xex_image) override { xex_image = "game:\\default.xex"; }

  // Sem --game_data_root, procura game_root/ ao lado do executavel (dump
  // JTAG-RGH com default.xex na raiz). Caminho explicito sempre vence.
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
        if (std::filesystem::is_regular_file(candidate / sub / "default.xex", ec)) {
          paths.game_data_root = candidate / sub;
          return;
        }
      }
      if (candidate == candidate.parent_path()) {
        break;
      }
    }
  }

  // Sem hack de flag: o proprio default.xex prepara o estado do jogo antes de
  // chamar os exports dele (launch data do dashboard, GetProcAddress, etc.).
  // A hypothesis anterior (flag 0x89398418 armada no pre-launch) eratentativa
  // para rodar o CRT do Sims3.xex direto e nao se aplica a essa cadeia.

  // Ajuda de analise: com sims3_DUMP_IMAGE=<arquivo>, grava a imagem guest
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
