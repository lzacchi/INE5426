#
# lexer.py
#
# Authors: Artur Barichello
#          Lucas Verdade
#          Lucas Zacchi

from ply.lex import LexToken


def p_PROGRAM(p: LexToken) -> None:
    """
    PROGRAM : STATEMENT
            | FUNCLIST
            | empty
    """
    p[0] = p[1]


def p_FUNCLIST(p: LexToken) -> None:
    """
    FUNCLIST : FUNCDEF FUNCLIST
             | FUNCDEF
    """
    p[0] = p[1]


def p_FUNCLISTAUX(p: LexToken) -> None:
    """
    FUNCLISTAUX : FUNCLIST
    """
    p[0] = p[1]


def p_FUNCDEF(p: LexToken) -> None:
    """
    FUNCDEF : FUNCTION_DECLARATION LABEL LEFT_PARENTHESIS PARAMLIST RIGHT_PARENTHESIS LEFT_BRACKET STATELIST RIGHT_BRACKET
    """
    p[0] = p[1]


def p_DATATYPE(p: LexToken) -> None:
    """
    DATATYPE : INTEGER
             | FLOATING_POINT
             | STRING
    """
    p[0] = p[1]


def p_PARAMLIST(p: LexToken) -> None:
    """
    PARAMLIST : DATATYPE LABEL COMMA PARAMLIST
              | DATATYPE LABEL
    """
    p[0] = p[1]


def p_STATEMENT(p: LexToken) -> None:
    """
    STATEMENT : VARDECL SEMICOLON
              | ATRIBSTAT SEMICOLON
              | PRINTSTAT SEMICOLON
              | READSTAT SEMICOLON
              | RETURNSTAT SEMICOLON
              | IFSTAT
              | FORSTAT
              | LEFT_BRACKET STATELIST RIGHT_BRACKET
              | BREAK SEMICOLON
              | SEMICOLON
    """
    p[0] = p[1]


def p_VARDECL(p: LexToken) -> None:
    """
    VARDECL : DATATYPE LABEL OPTIONAL_VECTOR
    """
    p[0] = p[1]


def p_OPTIONAL_VECTOR(p: LexToken) -> None:
    """
    OPTIONAL_VECTOR : LEFT_SQUARE_BRACKET INTEGER_CONSTANT RIGHT_SQUARE_BRACKET OPTIONAL_VECTOR
    """
    p[0] = p[1]


def p_ATRIB_RIGHT(p: LexToken) -> None:
    """
    ATRIB_RIGHT : EXPRESSION
                | ALOCEXPRESSION
                | FUNCCALL
    """
    p[0] = p[1]


def p_ATRIBSTAT(p: LexToken) -> None:
    """
    ATRIBSTAT : LVALUE ATTRIBUTION ATRIB_RIGHT
    """
    p[0] = p[1]


def p_FUNCCALL(p: LexToken) -> None:
    """
    FUNCCALL : LABEL LEFT_PARENTHESIS PARAMLISTCALL RIGHT_PARENTHESIS
    """
    p[0] = p[1]


def p_PARAMLISTCALL(p: LexToken) -> None:
    """
    PARAMLISTCALL : LABEL COMMA PARAMLISTCALL
                  | LABEL
    """
    p[0] = p[1]


def p_PRINTSTAT(p: LexToken) -> None:
    """
    PRINTSTAT : PRINT EXPRESSION
    """
    p[0] = p[1]


def p_READSTAT(p: LexToken) -> None:
    """
    READSTAT : READ LVALUE
    """
    p[0] = p[1]


def p_RETURNSTAT(p: LexToken) -> None:
    """
    RETURNSTAT : RETURN
    """
    p[0] = p[1]


def p_IFSTAT(p: LexToken) -> None:
    """
    IFSTAT : IF LEFT_PARENTHESIS EXPRESSION RIGHT_PARENTHESIS STATEMENT OPTIONAL_ELSE
    """
    p[0] = p[1]


def p_OPTIONAL_ELSE(p: LexToken) -> None:
    """
    OPTIONAL_ELSE : LEFT_PARENTHESIS STATEMENT RIGHT_PARENTHESIS
    """
    p[0] = p[1]


def p_FORSTAT(p: LexToken) -> None:
    """
    FORSTAT : FOR LEFT_PARENTHESIS ATRIBSTAT SEMICOLON EXPRESSION SEMICOLON ATRIBSTAT RIGHT_PARENTHESIS STATEMENT
    """
    p[0] = p[1]


def p_STATELIST(p: LexToken) -> None:
    """
    STATELIST : STATEMENT OPTIONAL_STATELIST
    """
    p[0] = p[1]


def p_OPTIONAL_STATELIST(p: LexToken) -> None:
    """
    OPTIONAL_STATELIST : STATELIST
                       | empty
    """
    p[0] = p[1]


def p_ALLOCEXPRESSION(p: LexToken) -> None:
    """
    ALLOCEXPRESSION : NEW DATATYPE NUMEXPRESION OPT_ALLOC_NUMEXP
                    | NEW DATATYPE OPT_ALLOC_NUMEXP
    """
    p[0] = p[1]


# def p_OPTIONAL_ALLOCATION_NUMEXPRESSION(p: LexToken) -> None:
#     """
#     OPTIONAL_ALLOCATION_NUMEXPRESSION : NUMEXPRESSION OPTIONAL_ALLOCATION_NUMEXPRESSION
#                                       | OPTIONAL_ALLOCATION_NUMEXPRESSION
#     """
#     p[0] = p[1]


def p_EXPRESSION(p: LexToken) -> None:
    """
    EXPRESSION : NUMEXPRESSION
    """
    p[0] = p[1]


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
