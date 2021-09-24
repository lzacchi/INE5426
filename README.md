# INE5426

## INSTRUÇÕES

Instalação:
1. `make install-poetry`
2. `make install`

Entrega:
- `make run` ou apenas `make` mostra toda a output esperada segundo o enunciado da entrega 3 (`ASem.pdf`). A output inclui alguns testes  de módulos internos do compilador e roda os arquivos de exemplo.
- `make test` roda apenas os programas de exemplo que foram requisitados no enunciado.
- `make example` roda um exemplo fixo ou passado por argumento (ex: `make example src=<path/to/source_code>`).

Extra:
- `make clean` remove os arquivos da pasta `output/`
- `make uninstall` remove o POoetry

## Docs
Relatórios e outras documentações estão na pasta `pdf`

## Exemplos
Diversos exemplos da linguagem estão na pasta `test-code`, cada pasta procura reunir exemplos para mostrar diversas partes do compilador funcionando ou dando erro como esperado.

Existem exemplos propositalmente errados para demonstrar a detecção de erros do compilador. E estes podem ser executados das seguintes formas:
- `make example src=test-code/semantic-analysis/invalid-break-operator.lua`
- `make example src=test-code/semantic-analysis/invalid-operations.lua`
- `make example src=test-code/semantic-analysis/invalid-variable-declaration.lua`

E existem exemplos de análise semântica que estão corretos e válidos. Podem ser executados das seguintes forma:
- `make example src=test-code/semantic-analysis/valid-break-operator.lua`
- `make example src=test-code/semantic-analysis/valid-operations.lua`
- `make example src=test-code/semantic-analysis/valid-variable-declaration.lua`
