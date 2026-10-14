# INVENTÁRIO — dump THE SIMS 3 (XBOX360) JTAG-RGH (só leitura)

## Executáveis (cabecalhos lidos com ferramentas/extract_iso.py --info, 14/10/2026)

| Arquivo | Tamanho | Title ID | Media ID | Versão | Base | Entry | Imagem | Flags | Cripto |
|---|---|---|---|---|---|---|---|---|---|
| `default.xex` | 1.351.680 | 454108E2 | 21CDDF46 | 0.0.0.4 | 0x82000000 | 0x82041028 | 1.441.792 | 0x1 | AES-128 + basic |
| `Sims3.xex` | 20.332.544 | 454108E2 | 21CDDF46 | 0.0.0.4 | 0x88000000 | 0x88F12800 | 21.495.808 | 0x9 | AES-128 + basic |
| `PrivLoader.xex` | 692.224 | 454108E2 | 21CDDF46 | 0.0.0.4 | 0x82000000 | 0x82010510 | 786.432 | 0x1 | AES-128 + basic |

- `default.xex` é o loader de entrada (base 0x82000000, imagem 1,4 MB).
- `Sims3.xex` é o jogo principal (base própria 0x88000000, imagem 21,5 MB) — **entrada do codegen**.
- Descriptografia/descompressão ficam com o rexglue (a ferramenta não descriptografa, por desenho).
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
