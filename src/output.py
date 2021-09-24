# output.py
#
# Authors: Artur Barichello
#          Lucas Verdade
#          Lucas Zacchi
#
# Helper functions to output data into terminal
#

import argparse
from typing import List
from pprint import pprint
from tabulate import tabulate


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("--src", dest="src", help="Source file input", type=str)
    parser.add_argument(
        "--debug", dest="debug", help="PLY debug mode", action="store_true"
    )
    parser.add_argument(
        "--print-typecheck",
        dest="print_typecheck",
        help="Print typecheck operations",
        action="store_true",
    )
    return parser.parse_args()


# --- Compiler generated errors ---


class InvalidTokenError(Exception):
    pass


class VariableNotDeclared(Exception):
    pass


class VariableInScopeError(Exception):
    pass


class InvalidBreakError(Exception):
    pass


class InvalidBinaryOperation(Exception):
    pass


class InvalidSyntaxError(Exception):
    pass


# --- Output helper functions ---


def print_tokens(tokens: List) -> None:
    result = [(t.type, t.value) for t in tokens]
    pprint("\nPrinting token list: ('Token enumerator', 'Token value'):")
    pprint(result, indent=4)


def print_symbol_table(tokens: List) -> None:
    print("\nPrinting symbol table:")

    symbol_table: dict = {}
    token_table = [[t.lexpos, t.lineno, t.type, t.value] for t in tokens]

    for token in token_table:
        if token[2] == "LABEL":
            if token[3] in symbol_table:
                symbol_table[token[3]][2].append(token[1])
            else:
                symbol_table[token[3]] = (token[0], token[1], [])

    headers = ["Label", "Index", "Declaration (line)", "Referenced (lines)"]
    print(tabulate([(k,) + v for k, v in symbol_table.items()], headers=headers))
    print_separator()


def print_separator() -> None:
    print("\n===========================\n")
