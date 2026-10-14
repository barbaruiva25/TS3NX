# BOOT-XENIA — teste de fumaça do dump (só referência, em inglês)

Data: 14/10/2026. Xenia canary 40cee11 (`ferramentas/xenia/canary`, fora do repo).
Comando: `xenia_canary.exe "<dump>/default.xex"` minimizado, teto 600s. Saiu sozinho, exit 0.

## O que andou
- Título reconhecido ("The Sims 3"), achievements lidos (Karma Powers etc.).
- `Sims3.xex` carregou na base 0x88000000 e executou: `XamEnumerate`, `XGetLanguage`
  (2x: loader 0x820A6EB0 e jogo 0x8925F77C — ponto do hook de locale!), Mono
  (`mscorlib`, `SimIFace`), enumeração de conteúdo.
- Sem FATAL. Avisos esperados de emulador: `IoDismountVolumeByFileHandle` sem
  implementação (2x), `XFileXctdCompressionInformation` sem implementação,
  `XFileSectorInformation` stub, probes Mono `.config` falhando (benigno).

## Como terminou
- `Cheap-skate exit` (guest chamou saída sozinho). Pista: `ResolvePath(sims3.xex)
  failed - device not found` no início — o loader tentou `\sims3.xex` absoluto e
  falhou uma vez (depois o jogo rodou mesmo assim; checar caminho exato).
- Não chegou a menu visível nesta janela; log tem 3144 linhas (`xenia.log`
  guardado fora do repo).

## Limite deste teste
- Xenia responde inglês ao jogo: **não valida PTBR**. PTBR exige console RGH em
  português ou inspeção dos recursos de idioma no `UI.package` (comprimidos).
- Próximo: repetir com captura de tela + segmentos de 60s até o menu; investigar
  o `ResolvePath(\sims3.xex)` (montagem de pasta vs arquivo no Xenia).
