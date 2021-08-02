#
# lexer.py
#
# Authors: Artur Barichello
#          Lucas Verdade
#          Lucas Zacchi

from ply.lex import LexToken


def p_EXPRESSION(p: LexToken) -> None:
    """
    EXPRESSION : NUMEXPRESSION
    """
    p[0] = p[1]


# def p_OPTIONAL_ALLOCATION_NUMEXPRESSION(p: LexToken) -> None:
#     """
#     OPTIONAL_ALLOCATION_NUMEXPRESSION : NUMEXPRESSION OPTIONAL_ALLOCATION_NUMEXPRESSION
#                                       | OPTIONAL_ALLOCATION_NUMEXPRESSION
#     """
#     p[0] = p[1]


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


def p_NUMEXPRESSION(p: LexToken) -> None:
    """
    NUMEXPRESSION : TERM RECURSIVE_MINUS_OR_PLUS
    """
    p[0] = p[1]


# def p_RECURSIVE_MINUS_OR_PLUS(p: LexToken) -> None:
#     """
#     RECURSIVE_MINUS_OR_PLUS : MINUS_OR_PLUS
#                             | PLUS
#     """
#     p[0] = p[1]


def p_MINUS_OR_PLUS(p: LexToken) -> None:
    """
    MINUS_OR_PLUS : MINUS
                  | PLUS
    """
    p[0] = p[1]


def p_TERM(p: LexToken) -> None:
    """
    TERM : UNARYEXPR RECURSIVE_UNARYEXPR
    """
    p[0] = p[1]


def p_RECURSIVE_UNARYEXPR(p: LexToken) -> None:
    """
    RECURSIVE_UNARYEXPR : UNARYEXPR_OPERATOR
    """
    p[0] = p[1]


def p_UNARYEXPR_OPERATOR(p: LexToken) -> None:
    """
    UNARYEXPR_OPERATOR : TIMES
                       | DIVISION
                       | MODULO
    """
    p[0] = p[1]


def p_UNARYEXPR(p: LexToken) -> None:
    """
    UNARYEXPR : MINUS_OR_PLUS_FACTOR
              | FACTOR
    """
    p[0] = p[1]


def p_FACTOR(p: LexToken) -> None:
    """
    FACTOR : INTEGER_CONSTANT
           | FLOATING_POINT_CONSTANT
           | STRING_CONSTANT
           | NULL
           | LVALUE
           | NUMEXPRESSION
    """


# def p_LVALUE(p: LexToken) -> None:
#     """
#     LVALUE : LABEL OPTIONAL_ALLOCATION_NUMEXPRESSION
#     """


def p_error(p: LexToken) -> None:
    print(f"Syntax error at token {p}")
