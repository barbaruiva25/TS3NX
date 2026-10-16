# Cadeia de boot do The Sims 3 (Xbox 360) — como o jogo realmente entra

Tudo abaixo vem de disassembly dos três XEX do dump, com
`ferramentas/ppc_mini.py` sobre as imagens em `thesims3/LOGS/*_image.bin`
(geradas por `REXGLUE_DUMP_IMAGE` no codegen). Nada aqui é hipótese sem
evidência; quando havia duas leituras possíveis, está escrito qual foi testada.

## Resumo

| XEX | Papel | Imagem base | Entry |
|---|---|---|---|
| `default.xex` | entrypoint da mídia (loader) | `0x82000000` | `0x82041028` |
| `Sims3.xex` | módulo do jogo, carregado por `XexLoadImage` | `0x88000000` | exports (não usado) |
| `PrivLoader.xex` | não participa do caminho executado | `0x82000000` | `0x82010510` |

O `default.xex` carrega `Sims3.xex` e chama **um dos dois exports** dele:
o **ord 3** quando existe launch data do dashboard (1020 bytes), o **ord 1**
quando não existe. Os dois exports são funções reais (não o CRT).

## 1. O CRT do `Sims3.xex` é beco sem saída

Entry `0x88F12800` → `b 0x88F126A8`. Em `0x88F126A8`:

```
88F126C8  cmplwi cr6,r4,0        ; r4 = 2o argumento do entry
88F126CC  bne   cr6, 0x88F126EC
88F126D4  lis   r11,0x893A0000
88F126D8  lwz   r11,-31720(r11)  ; flag em 0x89398418
88F126DC  cmpwi cr6,r11,0
88F126E0  bne   cr6, 0x88F126EC
88F126E4  li    r3,0             ; r3=0 -> sai
```

Segue para `0x887D3CF8`, que é literalmente `li r3,1; blr` — um stub. Com
`r4` = 1 ou 2 ele entra em `sub_88F12508`, que só retorna 0 (falha) se um de
quatro inits falhar. Medido em runtime: a thread guest retorna em ~1 ms e o
processo morre com `0xC0000374` no teardown, sempre **depois** de
`Execution complete`. Nenhum caminho desse CRT chega ao jogo.

Por isso o entry do jogo **não** é o entry do XEX: são os exports.

## 2. Exports do `Sims3.xex`

Tabela de exportação em `0x8926037C` (180 entradas, `imagebase = 0x8800`):

| ordinal | endereço | corpo |
|---|---|---|
| 1 | `0x88329E58` | monta objeto local e chama `sub_88354158` → `sub_88329CC8` → `sub_88328EA8` |
| 2 | `0x88329E08` | `b 0x885A5670`: `stb r3,16288(0x892F0000)` — arma um byte de flag |
| 3 | `0x88329E10` | idem ao 1, com `sub_88354118` no lugar do `58` |

O `default.xex` resolve os dois (3 e 1) com `XexGetProcedureAddress` em
`sub_82040BA0` e chama um deles com `mtctr` + `bctrl`.

## 3. O `default.xex`

```
82040A60  lis   r11,0x820B0000
82040A68  addi  r11,r11,80       ; 0x820B0050
82040A6C  lwz   r3,4(r11)        ; [0x820B0054] = "privloader.xex"
82040A70  bl    0x82040C58       ; comparacao de string (flag de launch data)
82040A7C  lwz   r3,80(r11)       ; [0x820B0050] = "sims3.xex"
82040A80  bl    0x82040C10       ; XexLoadImage
82040A94  bl    0x82040BA0       ; GetProcAddress(handle, 3) -> r31
82040AA4  bl    0x82040BA0       ; GetProcAddress(handle, 1) -> r30
82040AAC  cmplwi cr6,r31,0 ; beq -> falha
82040AB4  cmplwi cr6,r30,0 ; beq -> falha
82040ABC  rlwinm. r11,r28,0,24,31   ; r28 = tem launch data?
82040AC0  beq   cr0, 0x82040ACC
82040AC4  addi  r3,r1,96         ; tem launch data -> buffer de 1020 bytes
82040ACC  bl    0x82040CE8       ; senao -> malloc(1020)
82040AD8  mtctr r31
82040ADC  bctrl                  ; ord 3 com (buffer, 1020)
82040AE4  mr    r4,r25
82040AE8  mtctr r30
82040AEC  mr    r3,r26
82040AF0  bctrl                  ; ord 1 com (r3 = r26, r4 = r25)
```

`sub_82040C10` é o wrapper de `XexLoadImage`:

```
82040C10  mflr  r12
82040C1C  mr    r5,r4
82040C20  addi  r6,r1,80        ; out = handle
82040C24  li    r4,9            ; flags = 9
82040C28  bl    0x820A6F10      ; XexLoadImage
82040C40  lwz   r3,80(r1)       ; devolve handle
```

`sub_82040BA0` é o wrapper de `XexGetProcedureAddress(h=r3, ord=r4, out=r5)`.

## 4. Launch data

O dashboard passaria 1020 bytes (`XamLoaderGetLaunchDataSize` → 0x3FC =
1020, em `0x820409E4`). Em emulador e no PC, `XamLoaderGetLaunchDataSize`
devolve `X_ERROR_NOT_FOUND` (0xC0000225) e o tamanho fica 0 — por isso o
caminho executado é o **ord 1**, não o ord 3. É o mesmo caminho que o Xenia
executou com sucesso.

## 5. `PrivLoader.xex`

O `default.xex` referencia a string `"privloader.xex"` (em `0x82000670`,
apontada por `0x820B0054`) apenas em `sub_82040C58`, que compara a string e
ajusta um bit de flag que decide de onde sai o buffer do ord 3. O código do
`PrivLoader.xex` não é chamado nesse caminho. Ele saiu do manifesto
(`priv_manifest.toml` continua existindo só para auditoria, com
`overrides_priv.toml`).

> Nota de leitura: no log do Xenia, a linha
> `F 820005C4 820A6F10 199 ( 409) XexLoadImage` **não** é uma chamada — é a
> resolução do símbolo do thunk de import em `0x820005C4`
> (`0x00010199`, registro 409 da tabela de imports). As chamadas reais de
> `XexLoadImage` estão em `0x82040C28`.

## 6. O que isso mudou no projeto

- `sims3_manifest.toml`: `default.xex` como `[entrypoint]`, `Sims3.xex` como
  `[[modules]]` com `guest_path = "sims3.xex"`. O codegen passa a emitir
  `generated/default/module_registry.cpp` e `dll_targets.cmake`, e o módulo
  do jogo vira a biblioteca `sims3_Sims3` (carregada pelo kernel em
  `XexLoadImage`).
- `guest_path = "sims3.xex"` (só o nome) é o que casa: `LoadUserModule`
  junta o nome com o diretório do executável (`game:\sims3.xex`) e
  `NormalizeGuestPath` remove o prefixo de volume antes de comparar com o
  registro.
- Não há mais hack de flag nem redirecionamento de entry no app: o
  `default.xex` recompilado é quem faz o trabalho, com os argumentos reais.