SHELL := /bin/bash

# Colors
GREEN=\033[0;32m
RED=\033[0;31m
NC=\033[0m

help:
	@echo Available commands:
	@echo -e "${GREEN} ESSE TEXTO EH VERDE ${NC}"

run:
	@python src/lexer.py
