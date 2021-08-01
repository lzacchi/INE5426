#
# lexer.py
#
# Authors: Artur Barichello
#          Lucas Verdade
#          Lucas Zacchi

from ply.lex import LexToken


def p_REL_OP(p: LexToken) -> None:
    """
    REL_OP : LESSER_THAN
           | GREATER_THAN
           | LESS_OR_EQUAL_THAN
           | GREATER_OR_EQUAL_THAN
           | EQUAL
           | NOT_EQUAL
    """
    p[0] = p[1]
