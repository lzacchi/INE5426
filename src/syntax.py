#
# syntax.py
#
# Authors: Artur Barichello
#          Lucas Verdade
#          Lucas Zacchi

import re
from dataclasses import dataclass
from collections import namedtuple
from typing import Any, Dict, List, Tuple
from ply.lex import LexToken
from output import VariableAlreadyDeclared


@dataclass
class AtribStat:
    lvalue: str
    atrib_right: str


@dataclass
class AllocExpression:
    datatype: Any
    indexes: List[int]


@dataclass
class PrintStat:
    value: Any


@dataclass
class StatementList:
    value: List[Any]


#              label      type value
variables: Dict[str, Tuple[str, Any]] = {}


def p_PROGRAM(p: LexToken) -> None:
    """
    PROGRAM : STATEMENT
            | FUNCLIST
            | empty
    """
    result = p[1]
    if type(result) is StatementList:
        statement_results = [r.value for r in result.value]
        statement_results.reverse()
        p[0] = statement_results
    else:
        p[0] = p[1]


def p_FUNCLIST(p: LexToken) -> None:
    """
    FUNCLIST : FUNCDEF FUNCLISTTMP
    """
    p[0] = (p[1], p[2])


def p_FUNCLISTTMP(p: LexToken) -> None:
    """
    FUNCLISTTMP : FUNCLIST
                | empty
    """
    p[0] = p[1]


def p_FUNCDEF(p: LexToken) -> None:
    """
    FUNCDEF : FUNCTION_DECLARATION LABEL LEFT_PARENTHESIS PARAMLIST RIGHT_PARENTHESIS LEFT_BRACKET STATELIST RIGHT_BRACKET
    """
    # pass
    # list containing label, paramlist and statelist
    label = p[2]
    paramlist = p[4]
    statelist = p[7]
    p[0] = (label, paramlist, statelist)


def p_DATATYPE(p: LexToken) -> None:
    """
    DATATYPE : INTEGER
             | FLOATING_POINT
             | STRING
    """
    p[0] = p[1]


def p_PARAMLIST(p: LexToken) -> None:
    """
    PARAMLIST : DATATYPE LABEL PARAMLISTTMP
              | empty
    """
    # CONFERIR A LÓGICA AQUI EMBAIXO PQ MUDOU
    if len(p) == 5:  # multiple parameters
        params = [param for param in p[4]]
        p[0] = (p[1], p[2], params)
    elif len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]


def p_PARAMLISTTMP(p: LexToken) -> None:
    """
    PARAMLISTTMP : COMMA PARAMLIST
                 : empty
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
    if len(p) == 3 and type(p[1]) is AtribStat:
        atribstat = p[1]
        lvalue = atribstat.lvalue
        atrib_right = atribstat.atrib_right
        label = lvalue[0]
        variables[label] = (label, atrib_right)
        p[0] = p[1]
    elif len(p) == 3 and type(p[1]) is PrintStat:
        p[0] = p[1]
    elif len(p) == 4 and type(p[2]) is StatementList:
        p[0] = p[2]


def p_VARDECL(p: LexToken) -> None:
    """
    VARDECL : DATATYPE LABEL OPTIONAL_VECTOR
    """
    datatype = p[1]
    label = p[2]
    # opt_vector = p[3]  # todo

    if label in variables.keys():
        raise VariableAlreadyDeclared

    # if opt_vector:
    # variables[label] = (datatype, opt_vector)
    # else:
    variables[label] = (datatype, None)


def p_OPTIONAL_VECTOR(p: LexToken) -> None:
    """
    OPTIONAL_VECTOR : LEFT_SQUARE_BRACKET INTEGER_CONSTANT RIGHT_SQUARE_BRACKET OPTIONAL_VECTOR
                    | empty
    """
    if len(p) == 5:  # multiple opt_vector
        vectors = [v for v in p[4]]
        vectors.insert(p[0], 0)
        p[0] = vectors


def p_ATRIB_RIGHT(p: LexToken) -> None:
    """
    ATRIB_RIGHT : ALLOCEXPRESSION
                | EXPRESION_OR_FUNCCALL
    """
    p[0] = p[1]


def p_EXPRESION_OR_FUNCCALL(p: LexToken) -> None:
    """
    EXPRESSION_OR_FUNCCALL  : PLUS FACTOR RECURSIVE_UNARYEXPR RECURSIVE_MINUS_OR_PLUS_TERM OPTIONAL_REL_OP_NUMEXPRESSION
                            | MINUS FACTOR RECURSIVE_UNARYEXPR RECURSIVE_MINUS_OR_PLUS_TERM OPTIONAL_REL_OP_NUMEXPRESSION
                            | INTEGER_CONSTANT RECURSIVE_UNARYEXPR RECURSIVE_MINUS_OR_PLUS_TERM OPTIONAL_REL_OP_NUMEXPRESSION
                            | FLOATING_POINT_CONSTANT RECURSIVE_UNARYEXPR RECURSIVE_MINUS_OR_PLUS_TERM OPTIONAL_REL_OP_NUMEXPRESSION
                            | STRING_CONSTANT RECURSIVE_UNARYEXPR RECURSIVE_MINUS_OR_PLUS_TERM OPTIONAL_REL_OP_NUMEXPRESSION
                            | NULL RECURSIVE_UNARYEXPR RECURSIVE_MINUS_OR_PLUS_TERM OPTIONAL_REL_OP_NUMEXPRESSION
                            | LEFT_PARENTHESIS NUMEXPRESSION RIGHT_PARENTHESIS RECURSIVE_UNARYEXPR RECURSIVE_MINUS_OR_PLUS_TERM OPTIONAL_REL_OP_NUMEXPRESSION
                            | LABEL FOLLOW_LABEL
    """
    pass


def p_FOLLOW_LABEL(p: LexToken) -> None:
    """
    FOLLOW_LABEL : OPTIONAL_ALLOC_NUMEXPRESSION RECURSIVE_UNARYEXPR RECURSIVE_MINUS_OR_PLUS_TERM OPTIONAL_REL_OP_NUMEXPRESSION | LEFT_PARENTHESIS PARAMLISTCALL RIGHT_PARENTHESIS
    """
    pass


def p_ATRIBSTAT(p: LexToken) -> None:
    """
    ATRIBSTAT : LVALUE ATTRIBUTION ATRIB_RIGHT
    """
    lvalue = p[1]
    atrib_right = p[3]
    p[0] = (lvalue, atrib_right)


def p_FUNCCALL(p: LexToken) -> None:
    """
    FUNCCALL : LABEL LEFT_PARENTHESIS PARAMLISTCALL RIGHT_PARENTHESIS
    """
    label = p[1]
    paramlistcall = p[3]
    p[0] = (label, paramlistcall)


def p_PARAMLISTCALL(p: LexToken) -> None:
    """
    PARAMLISTCALL : LABEL PARAMLISTCALLTMP
                  | empty
    """
    # CONFERIR
    if len(p) > 2:
        p[0] = (p[1], p[3])
    else:
        p[0] = p[1]


def p_PARAMLISTCALLTMP(p: LexToken) -> None:
    """
    PARAMLISTCALLTMP : COMMA PARAMLISTCALL
                     | empty
    """
    pass


def p_PRINTSTAT(p: LexToken) -> None:
    """
    PRINTSTAT : PRINT EXPRESSION
    """
    expression = PrintStat(p[2])
    p[0] = expression


def p_READSTAT(p: LexToken) -> None:
    """
    READSTAT : READ LVALUE
    """
    p[0] = p[2]


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
    OPTIONAL_ELSE : ELSE LEFT_BRACKET STATELIST RIGHT_BRACKET
                  | empty
    """
    if len(p) == 2:
        p[0] = None
    else:
        p[0] = p[3]


def p_FORSTAT(p: LexToken) -> None:
    """
    FORSTAT : FOR LEFT_PARENTHESIS ATRIBSTAT SEMICOLON EXPRESSION SEMICOLON ATRIBSTAT RIGHT_PARENTHESIS STATEMENT
    """
    forstat = p[1]
    first_atrib = p[3]
    expression = p[5]
    second_atrib = p[7]
    statement = p[9]

    p[0] = (forstat, first_atrib, expression, second_atrib, statement)


def p_STATELIST(p: LexToken) -> None:
    """
    STATELIST : STATEMENT OPTIONAL_STATELIST
    """
    statement = p[1]
    optional_rec = p[2]
    if optional_rec is None:
        p[0] = statement
    else:
        if type(statement) is StatementList:
            statement.value.append(optional_rec)
            p[0] = statement
        else:
            optional_rec.value.extend([statement])
            p[0] = optional_rec


def p_OPTIONAL_STATELIST(p: LexToken) -> None:
    """
    OPTIONAL_STATELIST : STATELIST
                       | empty
    """
    production = p[1]
    if p[1]:
        p[0] = StatementList([production])
    else:
        p[0] = None


def p_ALLOCEXPRESSION(p: LexToken) -> None:
    """
    ALLOCEXPRESSION : NEW DATATYPE LEFT_SQUARE_BRACKET NUMEXPRESSION RIGHT_SQUARE_BRACKET OPTIONAL_ALLOC_NUMEXPRESSION
    """
    datatype = p[2]
    numexpr = p[4]
    optional_alloc = p[6]
    if optional_alloc is None:
        p[0] = AllocExpression(datatype, [numexpr])
    else:
        accumulated_index_list = optional_alloc[0]
        p[0] = (datatype, numexpr + accumulated_index_list)


def p_OPTIONAL_ALLOC_NUMEXPRESSION(p: LexToken) -> None:
    """
    OPTIONAL_ALLOC_NUMEXPRESSION : LEFT_SQUARE_BRACKET NUMEXPRESSION RIGHT_SQUARE_BRACKET OPTIONAL_ALLOC_NUMEXPRESSION
                                 | empty
    """
    if len(p) == 2:
        p[0] = None
    else:
        numexpression = p[2]
        optional_alloc = p[4]
        if optional_alloc is None:
            p[0] = ("", numexpression)
        acc = optional_alloc[0]
        rec_numexpression = optional_alloc[1]
        p[0] = (acc + rec_numexpression, numexpression)


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
    print(
        f"""Syntax error at token {p}
Line:{p.lineno-1} | Column:{p.lexpos-2}"""
    )
