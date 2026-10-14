// thesims3_vfs.h — sistema de arquivos virtualizado da engine do The Sims 3.
// Nenhum dado do jogo no repo: caminhos lidos do manifesto, so leitura no dump.
#pragma once

#include <string>

// Raiz do dump ajustada em runtime via config (ex: ../THE SIMS 3/...).
// Redireciona .package / .world / .sims3 para fora do repo.
std::string thesims3_resolve(const std::string& virtual_path);

// Locale travado em pt-BR. Se BRA ausente: erro visivel, sem fallback silencioso p/ EN.
// Candidatos: Strings_BRA.package, *_BRA.package. Evidencia: log de qual arquivo abriu.
bool thesims3_force_bra_locale();
