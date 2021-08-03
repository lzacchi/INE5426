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
    table = [[t.lexpos, t.lineno, t.type, t.value] for t in tokens]

    sorted_table = sorted(table, key=lambda x: x[2])

    # lex_pos = []
    # line_no = []
    # token_value = []
    output_table = []

    for key, tokens in groupby(sorted_table, key=lambda k: k[2]):
        lex_pos_row = []
        line_no_row = []
        value_row = []
        for token in tokens:
            lex_pos_row.append(token[0])
            line_no_row.append(token[1])
            value_row.append(token[3])

        output_table.append([lex_pos_row, line_no_row, list(set(value_row))])
        # lex_pos.append(lex_pos_row)
        # line_no.append(line_no_row)
        # token_value.append(value_row)

    # print(lex_pos)
    # print(line_no)
    # print(token_value)
    print(tabulate(output_table, headers=["Index", "Line", "Type", "Value"]))


def print_separator() -> None:
    print("===========================")
