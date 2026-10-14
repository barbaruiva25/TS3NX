# INVENTÁRIO — dump THE SIMS 3 (XBOX360) JTAG-RGH (só leitura)

## Executáveis
- `default.xex` 1.351.680 B — loader, Title ID `454108E2` em `0x544`. SHA-256 em HASHES.md.
- `Sims3.xex` 20.332.544 B — executável principal.
- `PrivLoader.xex` 692.224 B — contém a string `PrivLoader` em si; papel ainda sem evidência.
- Busca textual por `XexLoadImage` / `XexLoadExecutable` / `PrivLoader` dentro de `Sims3.xex` e `default.xex`: **0 ocorrências**. XEXs estão cifrados/comprimidos (padrão 360: AES-128 + LZX), então imports só aparecem após descriptografia, como no `fc3-nx`.
- Conclusão: `PrivLoader.xex` **não** vai para `[[modules]]` ainda. Evidência pendente: imagem descriptografada + análise de import/carga.

## Mundo e assets
- Mundo: `GameData/NonPackaged/Worlds/Paul_World.world` (bairro de console: Moonlight Bay, único do disco — fonte: The Sims Wiki / pesquisa).
- 64 `.package` DBPF + `UI/UI.package` (14 MB, textos comprimidos — sem `Strings_BRA` em texto plano) + `Shaders_Xenon.precomp`.
- Total do dump: ~4,01 GB, bate com DVD base 2010.

## Idioma PTBR
- Ficha "Multi" não prova BRA. Pesquisa: edição distribuída no Brasil tinha menus/legendas PT-BR (UOL Start 06/10/2010, via Warner/EA); sem dublagem em nenhuma língua (Simlish). Não confirma que todo NTSC-U tem PT-BR.
- No 360 o jogo segue o idioma do console; sem evidência de seletor interno no Sims 3.
- Validação pendente: boot no Xenia/RGH com console em português.
