import sys

from lexer import Lexer
from ply.lex import LexToken
from typing import List
from output import print_tokens


def main(src: str) -> None:
    with open(src) as f:
        src = f.read()

    lexer = Lexer()
    lexer.build()
    lexer.input(src)

    print_tokens(lexer)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path/to/source-code>")
    else:
        src = sys.argv[1]
        main(src)
