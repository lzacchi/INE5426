#
# syntax.py
#
# Authors: Artur Barichello
#          Lucas Verdade
#          Lucas Zacchi

import re
from typing import Any, Dict, Tuple
from ply.lex import LexToken

from output import VariableAlreadyDeclared


#              label  type value
variables: Dict[str, Tuple[str, Any]] = {}


def p_PROGRAM(p: LexToken) -> None:
    """
    PROGRAM : STATEMENT
            | FUNCLIST
            | empty
    """
    p[0] = p[1]


def p_FUNCLIST(p: LexToken) -> None:
    """
    FUNCLIST : FUNCDEF FUNCLISTTMP
    """
    pass


def p_FUNCLISTTMP(p: LexToken) -> None:
    """
    FUNCLISTTMP : FUNCLIST
                | empty
    """
    pass


def p_FUNCDEF(p: LexToken) -> None:
    """
    FUNCDEF : FUNCTION_DECLARATION LABEL LEFT_PARENTHESIS PARAMLIST RIGHT_PARENTHESIS LEFT_BRACKET STATELIST RIGHT_BRACKET
    """
    # list containing label, paramlist and statelist
    pass
    # p[0] = (p[2], p[4], p[7])


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
              | empty
    """
    pass
    # if len(p) == 5:  # multiple parameters
    #     params = [param for param in p[4]]
    #     p[0] = (p[1], p[2], params)
    # else:
    #     p[0] = (p[1], p[2])


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
    if len(p) == 3 and p[2] == ";":
        p[0] = p[1]


def p_VARDECL(p: LexToken) -> None:
    """
    VARDECL : DATATYPE LABEL OPTIONAL_VECTOR
    """
    datatype = p[1]
    label = p[2]
    # opt_vector = p[3] # todo

    if label in variables.keys():
        raise VariableAlreadyDeclared

    variables[label] = (datatype, None)


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
    p[0] = p[1]


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
    print(p[2])


def p_READSTAT(p: LexToken) -> None:
    """
    READSTAT : READ LVALUE
    """
    p[0] = input(p[2])


def p_RETURNSTAT(p: LexToken) -> None:
    """
    RETURNSTAT : RETURN
    """
    pass


def p_IFSTAT(p: LexToken) -> None:
    """
    IFSTAT : IF LEFT_PARENTHESIS EXPRESSION RIGHT_PARENTHESIS STATEMENT OPTIONAL_ELSE
    """
    if p[3] is True:
        p[0] = p[5]
    else:
        p[0] = p[6]


def p_OPTIONAL_ELSE(p: LexToken) -> None:
    """
    OPTIONAL_ELSE : LEFT_BRACKET STATEMENT RIGHT_BRACKET
                  | empty
    """
    if p[1]:
        p[0] = p[2]
    else:
        p[0] = None


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
    ALLOCEXPRESSION : NEW DATATYPE LEFT_SQUARE_BRACKET NUMEXPRESSION RIGHT_SQUARE_BRACKET OPTIONAL_ALLOC_NUMEXPRESSION
    """
    pass


def p_OPTIONAL_ALLOC_NUMEXPRESSION(p: LexToken) -> None:
    """
    OPTIONAL_ALLOC_NUMEXPRESSION : LEFT_SQUARE_BRACKET NUMEXPRESSION RIGHT_SQUARE_BRACKET OPTIONAL_ALLOC_NUMEXPRESSION
                                 | empty
    """
    pass


def p_EXPRESSION(p: LexToken) -> None:
    """
    EXPRESSION : NUMEXPRESSION OPTIONAL_REL_OP_NUMEXPRESSION
    """
    optional = p[2]
    numexpr = p[1]
    if not optional:
        p[0] = numexpr
    else:
        optional_op = optional[0]
        optional_numexpr = optional[1]
        p[0] = eval(f"{numexpr} {optional_op} {optional_numexpr}")


def p_OPTIONAL_REL_OP_NUMEXPRESSION(p: LexToken) -> None:
    """
    OPTIONAL_REL_OP_NUMEXPRESSION : REL_OP NUMEXPRESSION
                                  | empty
    """
    if p[1] is None:
        p[0] = None
    else:
        operator = p[1]
        numexpr = p[2]
        p[0] = (operator, numexpr)


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
    term = p[1]
    recursion = p[2]
    if recursion is None:
        p[0] = term
    else:
        rec_operator = recursion[0]
        rec_term = recursion[1]
        p[0] = eval(f"{term} {rec_operator} {rec_term}")


def p_RECURSIVE_MINUS_OR_PLUS(p: LexToken) -> None:
    """
    RECURSIVE_MINUS_OR_PLUS : MINUS_OR_PLUS TERM RECURSIVE_MINUS_OR_PLUS
                            | empty
    """
    if len(p) == 2:
        p[0] = None
    elif len(p) == 4 and p[3] is None:
        operator = p[1]
        term = p[2]
        p[0] = (operator, term)
    elif len(p) == 4 and p[3] is not None:
        operator = p[1]
        term = p[2]
        recursion = p[3]
        rec_operator = recursion[0]
        rec_term = recursion[1]
        p[0] = eval(f"{operator} {term} {rec_operator} {rec_term}")


# str
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
    operator = p[1][0]
    factor = p[1][1]
    try:
        operator = p[2][0]
        rec_term = p[2][1]
        eval_str = f"{factor} {operator} {rec_term}"
        p[0] = eval(eval_str)
    except:
        # when the recursive_unaryexpression returns a 'None' operator we
        # return the accumulated factor
        p[0] = factor


# Tuple(operator, term)
def p_RECURSIVE_UNARYEXPR(p: LexToken) -> None:
    """
    RECURSIVE_UNARYEXPR : UNARYEXPR_OPERATOR TERM
                        | empty
    """
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = None


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
    operator = p[1] if len(p) == 3 else None
    factor = p[2] if len(p) == 3 else p[1]
    p[0] = (operator, factor)


def p_FACTOR(p: LexToken) -> None:
    """
    FACTOR : INTEGER_CONSTANT
           | FLOATING_POINT_CONSTANT
           | STRING_CONSTANT
           | NULL
           | LVALUE
           | LEFT_PARENTHESIS NUMEXPRESSION RIGHT_PARENTHESIS
    """
    text = str(p[1])
    is_integer = re.search(r"\d+", text)
    is_floating_point = re.search(r"\d+\.\d+", text)
    is_string = re.search(r'".*"', text)
    if len(p) == 4:  # numexpr
        p[0] = p[2]
    elif p[1] == "nil":
        p[0] = None
    elif is_integer:
        p[0] = int(p[1])
    elif is_floating_point:
        p[0] = float(p[1])
    elif is_string:
        p[0] = p[1]
    else:  # lvalue
        p[0] = p[1]


def p_LVALUE(p: LexToken) -> None:
    """
    LVALUE : LABEL OPTIONAL_ALLOC_NUMEXPRESSION
    """
    p[0] = p[1]


def p_empty(p: LexToken) -> None:
    "empty :"
    pass


def p_error(p: LexToken) -> None:
    print(f"Syntax error at token {p}\nlexer info:\n{p.lexer}")
