#
# output.py
#
# Authors: Artur Barichello
#          Lucas Verdade
#          Lucas Zacchi
#
#

from ply.lex import LexToken
from typing import List
from pprint import pprint
from tabulate import tabulate
from collections import namedtuple

from itertools import groupby
from operator import itemgetter


class InvalidTokenError(Exception):
    pass


def print_tokens(tokens: List) -> None:
    result = [(t.type, t.value) for t in tokens]
    print("\nPrinting token list: ('Token enumerator', 'Token value'):")
    pprint(result, indent=4)


# TODO: fix symbol table as requested in T1
def print_symbol_table(tokens: List) -> None:
    print("\nPrinting symbol table:")

    symbol_table: dict = {}
    token_table = [[t.lexpos, t.lineno, t.type, t.value] for t in tokens]

    for token in token_table:
        if token[2] == "LABEL":
            if token[3] in symbol_table:
                # print("its there")
                symbol_table[token[3]][2].append(token[1])
            else:
                symbol_table[token[3]] = (token[0], token[1], [])

    headers = ["Value", "Index", "Declaration (line)", "Referenced (lines)"]
    print(tabulate([(k,) + v for k, v in symbol_table.items()], headers=headers))

    # print(tabulate(symbol_table, headers=["Index", "Line", "Type", "Value"]))


def print_separator() -> None:
    print("===========================")
