#
# main.py
#
# Authors: Artur Barichello
#          Lucas Verdade
#          Lucas Zacchi
#
#

from argparse import Namespace
import sys
import ply.yacc as yacc
from lexer import Lexer
from output import (
    parse_arguments,
    print_tokens,
    print_symbol_table,
    InvalidTokenError,
    print_separator,
)
from pprint import pprint

# Ply necessary imports
from lexer import TOKENS as tokens
from syntax import *


def main(args: Namespace) -> None:
    with open(args.src) as f:
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
    # print_symbol_table(token_list)
    # print_separator()

    print("Executing yacc")
    # TODO: check recursion true or false?
    parser = yacc.yacc(start="PROGRAM", check_recursion=True)
    result = parser.parse(src, debug=args.debug, lexer=lexer)
    if not args.print_typecheck:
        pprint(result["scopes"])


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
