// The Sims 3: idioma do jogo (sims3.toml "language"), ver thesims3_language.cpp.

#pragma once

namespace sims3::language {

// Aplica o user_language do SDK a partir de "language" ("brazilian" e o padrao
// deste projeto; "auto" = idioma do console/PC). Antes de qualquer codigo guest:
// o jogo pergunta no inicio (XGetLanguage).
void Apply();

}  // namespace sims3::language
