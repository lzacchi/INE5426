SHELL := /bin/bash

# Colors
CCGREEN=\033[0;32m
CCYELLOW=\033[0;33m
CCRED=\033[0;31m
CCEND=\033[0m

src=source-code/success.lua


install-poetry:
	@echo -e "${CCGREEN}Installing Poetry...${CCEND}"
	@curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
	@echo -e "${CCGREEN}Done!${CCEND}"
install:
	@echo -e "${CCGREEN}Installing dependencies through Poetry...${CCEND}"
	@poetry install
	@echo -e "${CCGREEN}Done!${CCEND}"

run:
	@echo -e "${GREEN}Executing main program...${CCEND}"
	@echo -e "If you didn't specify a source program"
	@echo -e "An example file will be used"
	@echo -e "You can change that by executing ${CCYELLOW}make run src=<path/to/file>${CCEND}"
	@poetry run python src/main.py ${src}

clean:
	@echo -e "${CCRED}Uninstalling Poetry...${CCEND}"
	@POETRY_UNINSTALL=1 bash -c 'curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python'
	@echo -e "${CCGREEN}Done!${CCEND}"
