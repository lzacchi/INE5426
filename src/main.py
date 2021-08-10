#
# main.py
#
# Authors: Artur Barichello
#          Lucas Verdade
#          Lucas Zacchi
#
#

import sys
import ply.yacc as yacc
from lexer import Lexer
from output import print_tokens, print_symbol_table, InvalidTokenError, print_separator

# Ply necessary imports
from lexer import TOKENS as tokens
from syntax import *


def main(src: str) -> None:
    with open(src) as f:
        src = f.read()

    lexer = Lexer()
    lexer.build()
    lexer.input(src)

    try:
        token_list = lexer.token_list()
    except InvalidTokenError as err:
        sys.exit(-1)

    print_tokens(token_list)
    # TODO: fix symbol table as requested in T1
    # print_symbol_table(token_list)
    print_separator()

    print("Executing yacc")
    parser = yacc.yacc()
    result = parser.parse(src)
    print(result)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path/to/source-code>")
    else:
        src = sys.argv[1]
        main(src)
