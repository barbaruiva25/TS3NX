# SWITCHES — revisão pré-boot (14/10/2026)

Ferramenta: `ferramentas/switch_check.py`, faixa 88290000:89260000, imagem despejada.
Binário: 1200 indirect + 101 half + 230 byte + 228 absolute bctrs; gerados 565 switches.

## Resultado da ferramenta
- **truncated: 0, wrong targets: 0, missed: 0, tabelas inalcançáveis: 0.**
- extra cases (gerados a mais, nunca tomados): 16 — inofensivo.
- no bound no código: 8 — revisados à mão abaixo.
- odd shapes (revisão à mão): 3 (bctr 0x889E7A34, 0x891359A0, 0x891376F0: gerador
  manteve tail call indireta; runtime dirá).

## Revisão manual dos 8 "no bound"
- 0x88FAC538 (half, 17 casos): corpos 0..14 sequenciais (0x88FAC57C..); entradas
  15,16 extras nunca tomadas — over-generation inofensiva. Caso irmão com bound
  (byte table, `cmplwi r9,14` em 0x88FAC4B0) confirma o domínio 0..14.
- 0x8904CFC4 (half, 16 casos): entradas 0..15 alternam fall-through/default;
  resto é outra tabela de dados colada — inofensivo.
- 6 absolute em código (0x891D648C/7034/8BF0/B0BC/BC6C/D848, 28/11 casos):
  regra "tabela acaba no menor alvo" + 0 alvos errados — ok por construção.
- Nenhum `[[switch_tables]]` necessário. Se o boot mostrar "Switch case out of
  range" ou illegal instruction, reabrir por endereço.
