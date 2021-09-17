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
	@echo -e "${CCGREEN}Installing Poetry...${CCEND}"
	@curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
	@echo -e "${CCGREEN}Done!${CCEND}"

.PHONY:
install:
	@echo -e "${CCGREEN}Installing dependencies through Poetry...${CCEND}"
	@poetry install
	@echo -e "${CCGREEN}Done!${CCEND}"


.PHONY:
run:
	@echo -e "${CCGREEN}Creating output/ directory ${CCEND}"
	@mkdir -p output/

	@echo -e "${CCGREEN}Executing all three programs... ${CCEND}"

	@echo -e "${CCGREEN}Executing main program1.lua${CCEND}"
	@poetry run python src/main.py ${program_1} > output/program1.txt

	@echo -e "${CCGREEN}Executing main program2.lua${CCEND}"
	@poetry run python src/main.py ${program_2} > output/program2.txt

	@echo -e "${CCGREEN}Executing main program3.lua${CCEND}"
	@poetry run python src/main.py ${program_3} > output/program3.txt

	@echo -e "${CCGREEN}Executing main program4.lua${CCEND}"
	@poetry run python src/main.py ${program_4} > output/program4.txt

	@echo -e "${CCGREEN}Done! Execution outputs are located in the output directory.${CCEND}"


.PHONY:
test:
	@echo -e "${CCGREEN}Creating output/ directory ${CCEND}"
	@mkdir -p output/

	@echo -e "${CCGREEN}Executing all three programs... ${CCEND}"

	@echo -e "${CCGREEN}Executing main program1.lua${CCEND}"
	@poetry run python src/test.py test-code/small.lua > output/small.txt

	@echo -e "${CCGREEN}Done! Execution outputs are located in the output directory.${CCEND}"


.PHONY:
example:
	@echo -e "${GREEN}Executing main lexer.py...${CCEND}"
	@echo -e "If you didn't specify a source program"
	@echo -e "An example file will be used"
	@echo -e "You can change that by executing ${CCYELLOW}make run src=<path/to/file>${CCEND}"
	@poetry run python src/main.py ${src}


.PHONY:
clean:
	@echo -e "${CCRED}Cleaning output directory${CCEND}"
	@rm -r  -f output/*


.PHONY:
uninstall:
	@echo -e "${CCRED}Uninstalling Poetry...${CCEND}"
	@POETRY_UNINSTALL=1 bash -c 'curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python'
	@echo -e "${CCGREEN}Done!${CCEND}"
