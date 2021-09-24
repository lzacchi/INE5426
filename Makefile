SHELL := /bin/bash

# Colors
CCGREEN=\033[0;32m
CCYELLOW=\033[0;33m
CCRED=\033[0;31m
CCEND=\033[0m

# src=test-code/syntax-analysis/success.lua
src=test-code/syntax-analysis/printstat.lua
program_1=test-code/program1.lua
program_2=test-code/program2.lua
program_3=test-code/program3.lua
program_4=test-code/program4.lua

.PHONY:
all: install-poetry install run

.PHONY:
install-poetry:
	@echo -e "${CCGREEN}Instalando Poetry...${CCEND}"
	@curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
	@echo -e "${CCGREEN}Done!${CCEND}"

.PHONY:
install:
	@echo -e "${CCGREEN}Installing dependencies through Poetry...${CCEND}"
	@poetry install
	@echo -e "${CCGREEN}Done!${CCEND}"


.PHONY:
test:
	@echo -e "${CCGREEN}Criando diretorio output/ ${CCEND}"
	@mkdir -p output/

	@echo -e "${CCGREEN}Executando os tres programas...${CCEND}"

	@echo -e "${CCGREEN}Executando main program1.lua${CCEND}"
	@poetry run python src/main.py --src ${program_1} > output/program1.txt

	@echo -e "${CCGREEN}Executando main program2.lua${CCEND}"
	@poetry run python src/main.py --src ${program_2} > output/program2.txt

	@echo -e "${CCGREEN}Executando main program3.lua${CCEND}"
	@poetry run python src/main.py --src ${program_3} > output/program3.txt

	@echo -e "${CCGREEN}Executando main program4.lua${CCEND}"
	@poetry run python src/main.py --src ${program_4} > output/program4.txt

	@echo -e "${CCGREEN}Concluido! Outputs de execucao estao salvos no diretorio 'output'.${CCEND}"


.PHONY:
run:
	@echo -e "${CCGREEN}Creating output/ directory ${CCEND}"
	@mkdir -p output/

	@echo -e ""
	@echo -e "${CCYELLOW}--- TESTES DE VERIFICACAO DE TIPOS --- ${CCEND}"

	@echo -e "${CCGREEN}Executando test-code/semantic-analysis/valid-operations.lua com output salva em output/operations.txt${CCEND}"
	@poetry run python src/main.py --src test-code/semantic-analysis/valid-operations.lua --print-typecheck > output/operations.txt
	@echo -e "${CCGREEN}test-code/semantic-analysis/valid-operations.lua nao possui operacoes invalidas.${CCEND}"

	@echo -e "${CCYELLOW}--- TESTES DE DECLARAÇÂO DE VARIAVEIS POR ESCOPO --- ${CCEND}"

	@echo -e "${CCGREEN}Executando test-code/semantic-analysis/valid-variable-declaration.lua com output salva em output/variable-declaration.txt${CCEND}"
	@poetry run python src/main.py --src test-code/semantic-analysis/valid-variable-declaration.lua > output/variable-declaration.txt
	@echo -e "${CCGREEN}test-code/semantic-analysis/valid-variable-declaration.lua possui declarações de variáveis por escopo válidas.${CCEND}"

	@echo -e "${CCYELLOW}--- TESTES DE ESCOPO DE OPERADOR 'BREAK' --- ${CCEND}"

	@echo -e "${CCGREEN}Executando test-code/semantic-analysis/valid-break-operator.lua com output salva em output/break-operator.txt${CCEND}"
	@poetry run python src/main.py --src test-code/semantic-analysis/valid-break-operator.lua > output/break-operator.txt
	@echo -e "${CCGREEN}test-code/semantic-analysis/valid-break-operator.lua nao possui operadores 'break' invalidos.${CCEND}"

	@echo -e "${CCYELLOW}--- EXECUTANDO PROGRAMAS DE TESTE --- ${CCEND}"

	@echo -e "${CCGREEN}Executando main program1.lua${CCEND}"
	@poetry run python src/main.py --src ${program_1} > output/program1.txt

	@echo -e "${CCGREEN}Executando main program2.lua${CCEND}"
	@poetry run python src/main.py --src ${program_2} > output/program2.txt

	@echo -e "${CCGREEN}Executando main program3.lua${CCEND}"
	@poetry run python src/main.py --src ${program_3} > output/program3.txt

	@echo -e "${CCGREEN}Executando main program4.lua${CCEND}"
	@poetry run python src/main.py --src ${program_4} > output/program4.txt

	@echo -e "${CCGREEN}Concluido! Outputs de execucao foram salvos no diretorio 'output'${CCEND}"


.PHONY:
example:
	@echo -e "${GREEN}Executando main lexer.py...${CCEND}"
	@echo -e "Se voce nao especificou um programa fonte"
	@echo -e "um arquivo de exemplo sera utilizado."
	@echo -e "Voce pode muda-lo utilizando o comando ${CCYELLOW}make run src=<path/to/file>${CCEND}"

	@echo -e "${CCYELLOW}Executando o arquivo de exemplo...${CCEND}"
	@poetry run python src/main.py --src ${src}

.PHONY:
example-debug:
	@echo -e "${CCYELLOW}Executando o arquivo de exemplo...${CCEND}"
	@poetry run python src/main.py --src ${src} --debug


.PHONY:
clean:
	@echo -e "${CCRED}Limpando diretorio output${CCEND}"
	@rm -r  -f output/*


.PHONY:
uninstall:
	@echo -e "${CCRED}Desinstalando Poetry...${CCEND}"
	@POETRY_UNINSTALL=1 bash -c 'curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python'
	@echo -e "${CCGREEN}Concluido!${CCEND}"
