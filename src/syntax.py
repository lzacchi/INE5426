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
    pass


def p_FUNCLIST(p: LexToken) -> None:
    """
    FUNCLIST : FUNCDEF FUNCLIST
             | FUNCDEF
    """
    pass


def p_FUNCDEF(p: LexToken) -> None:
    """
    FUNCDEF : FUNCTION_DECLARATION LABEL LEFT_PARENTHESIS PARAMLIST RIGHT_PARENTHESIS LEFT_BRACKET STATELIST RIGHT_BRACKET
    """
    pass


def p_DATATYPE(p: LexToken) -> None:
    """
    DATATYPE : INTEGER
             | FLOATING_POINT
             | STRING
    """
    pass


def p_PARAMLIST(p: LexToken) -> None:
    """
    PARAMLIST : DATATYPE LABEL COMMA PARAMLIST
              | DATATYPE LABEL
              | empty
    """
    pass


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
    pass


def p_VARDECL(p: LexToken) -> None:
    """
    VARDECL : DATATYPE LABEL OPTIONAL_VECTOR
    """
    pass


def p_OPTIONAL_VECTOR(p: LexToken) -> None:
    """
    OPTIONAL_VECTOR : LEFT_SQUARE_BRACKET INTEGER_CONSTANT RIGHT_SQUARE_BRACKET OPTIONAL_VECTOR
                    | empty
    """
    pass


def p_ATRIB_RIGHT(p: LexToken) -> None:
    """
    ATRIB_RIGHT : EXPRESSION
                | ALLOCEXPRESSION
                | FUNCCALL
    """
    pass


def p_ATRIBSTAT(p: LexToken) -> None:
    """
    ATRIBSTAT : LVALUE ATTRIBUTION ATRIB_RIGHT
    """
    pass


def p_FUNCCALL(p: LexToken) -> None:
    """
    FUNCCALL : LABEL LEFT_PARENTHESIS PARAMLISTCALL RIGHT_PARENTHESIS
    """
    pass


def p_PARAMLISTCALL(p: LexToken) -> None:
    """
    PARAMLISTCALL : LABEL COMMA PARAMLISTCALL
                  | LABEL
                  | empty
    """
    pass


def p_PRINTSTAT(p: LexToken) -> None:
    """
    PRINTSTAT : PRINT EXPRESSION
    """
    pass


def p_READSTAT(p: LexToken) -> None:
    """
    READSTAT : READ LVALUE
    """
    pass


def p_RETURNSTAT(p: LexToken) -> None:
    """
    RETURNSTAT : RETURN
    """
    pass


def p_IFSTAT(p: LexToken) -> None:
    """
    IFSTAT : IF LEFT_PARENTHESIS EXPRESSION RIGHT_PARENTHESIS STATEMENT OPTIONAL_ELSE
    """
    pass


def p_OPTIONAL_ELSE(p: LexToken) -> None:
    """
    OPTIONAL_ELSE : LEFT_PARENTHESIS STATEMENT RIGHT_PARENTHESIS
                  | empty
    """
    pass


def p_FORSTAT(p: LexToken) -> None:
    """
    FORSTAT : FOR LEFT_PARENTHESIS ATRIBSTAT SEMICOLON EXPRESSION SEMICOLON ATRIBSTAT RIGHT_PARENTHESIS STATEMENT
    """
    pass


def p_STATELIST(p: LexToken) -> None:
    """
    STATELIST : STATEMENT OPTIONAL_STATELIST
    """
    pass


def p_OPTIONAL_STATELIST(p: LexToken) -> None:
    """
    OPTIONAL_STATELIST : STATELIST
                       | empty
    """
    pass


def p_ALLOCEXPRESSION(p: LexToken) -> None:
    """
    ALLOCEXPRESSION : NEW DATATYPE LEFT_SQUARE_BRACKET NUMEXPRESSION RIGHT_SQUARE_BRACKET OPTIONAL_ALLOCATION_NUMEXPRESSION
    """
    pass


def p_OPTIONAL_ALLOCATION_NUMEXPRESSION(p: LexToken) -> None:
    """
    OPTIONAL_ALLOCATION_NUMEXPRESSION : LEFT_SQUARE_BRACKET NUMEXPRESSION RIGHT_SQUARE_BRACKET OPTIONAL_ALLOCATION_NUMEXPRESSION
                                      | empty
    """
    pass


def p_EXPRESSION(p: LexToken) -> None:
    """
    EXPRESSION : NUMEXPRESSION OPTIONAL_REL_OP_NUMERICAL_EXPRESSION
    """
    pass


def p_OPTIONAL_REL_OP_NUMERICAL_EXPRESSION(p: LexToken) -> None:
    """
    OPTIONAL_REL_OP_NUMERICAL_EXPRESSION : REL_OP NUMEXPRESSION
                                         | empty
    """
    pass


def p_REL_OP(p: LexToken) -> None:
    """
    REL_OP : LESSER_THAN
           | GREATER_THAN
           | LESS_OR_EQUAL_THAN
           | GREATER_OR_EQUAL_THAN
           | EQUAL
           | NOT_EQUAL
    """
    pass


def p_NUMEXPRESSION(p: LexToken) -> None:
    """
    NUMEXPRESSION : TERM RECURSIVE_MINUS_OR_PLUS
    """
    pass


def p_RECURSIVE_MINUS_OR_PLUS(p: LexToken) -> None:
    """
    RECURSIVE_MINUS_OR_PLUS : MINUS_OR_PLUS TERM RECURSIVE_MINUS_OR_PLUS
                            | empty
    """
    pass


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
    pass


def p_RECURSIVE_UNARYEXPR(p: LexToken) -> None:
    """
    RECURSIVE_UNARYEXPR : UNARYEXPR_OPERATOR TERM
                        | empty
    """
    pass


def p_UNARYEXPR_OPERATOR(p: LexToken) -> None:
    """
    UNARYEXPR_OPERATOR : TIMES
                       | DIVISION
                       | MODULO
    """
    p[0] = p[1]


def p_UNARYEXPR(p: LexToken) -> None:
    """
    UNARYEXPR : MINUS_OR_PLUS FACTOR
              | FACTOR
    """
    pass


def p_FACTOR(p: LexToken) -> None:
    """
    FACTOR : INTEGER_CONSTANT
           | FLOATING_POINT_CONSTANT
           | STRING_CONSTANT
           | NULL
           | LVALUE
           | LEFT_PARENTHESIS NUMEXPRESSION RIGHT_PARENTHESIS
    """
    if p[1] == "(":
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_LVALUE(p: LexToken) -> None:
    """
    LVALUE : LABEL OPTIONAL_ALLOCATION_NUMEXPRESSION
    """
    p[0] = p[1]


def p_empty(p: LexToken) -> None:
    "empty :"
    pass


def p_error(p: LexToken) -> None:
    print(f"Syntax error at token {p}")
