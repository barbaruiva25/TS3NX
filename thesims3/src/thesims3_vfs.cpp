// thesims3_vfs.cpp — stub PTBR (fora do jogo, só redireciona)
// Regra: nenhum dado do jogo no repo. Caminhos lidos do manifesto, nunca hardcoded com jogo copiado.
#include <string>

// Raiz do dump ajustada em runtime via config (ex: ../THE SIMS 3/...).
// Redireciona .package / .world / .sims3 para fora do repo.
std::string thesims3_resolve(const std::string& virtual_path);

// Locale travado em pt-BR. Se BRA ausente: erro visível, sem fallback silencioso p/ EN.
// Candidatos: Strings_BRA.package, *_BRA.package. Evidência: log de qual arquivo abriu.
bool thesims3_force_bra_locale();
