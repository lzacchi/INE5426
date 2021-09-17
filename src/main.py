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
from pprint import pprint

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

    # Prints da entrega 1:
    # print_tokens(token_list)
    print_symbol_table(token_list)
    # print_separator()

    print("Executing yacc")
    # TODO: check recursion true or false?
    parser = yacc.yacc(start="PROGRAM", check_recursion=True)
    debug = True  # uncomment for debug mode
    # debug = False
    result = parser.parse(src, debug=debug, lexer=lexer)
    pprint(result)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path/to/source-code>")
    else:
        src = sys.argv[1]
        main(src)
