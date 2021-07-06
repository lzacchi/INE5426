import lexer as project_lexer

from ply.lex import LexToken
from typing import List
from pprint import pprint
from tabulate import tabulate


def print_tokens(tokens: List) -> None:
    result: List = []
    for t in tokens:
        result.append((t.type, t.value))
    print("\nPrinting token list: ('Token enumerator', 'Token value'):")
    pprint(result, indent=4)


def print_symbol_table(tokens: List) -> None:
    print("\nPrinting symbol table:")
    table: List = []
    for t in tokens:
        table.append([t.lexpos, t.lineno, t.type, t.value])
    print(tabulate(table, headers=["Index", "Line", "Type", "Value"]))
