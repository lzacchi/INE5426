#
# syntax.py
#
# Authors: Artur Barichello
#          Lucas Verdade
#          Lucas Zacchi
#
# Arquivo utilizado para análise sintática e
# análise semântica do código

import re
from ply import yacc
from dataclasses import dataclass
from collections import namedtuple
from typing import Any, Dict, List, Tuple
from output import VariableAlreadyDeclared, InvalidBreakError
from lexer import Lexer
from data import ScopeStack, EntryTable, DataType


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


lexer = Lexer()
lexer.build()
tokens = lexer.tokens

# TODO:
scopes = ScopeStack()

# As definicoes abaixo lidam com as producoes da gramatica
# e foram definidas seguindo o exemplo da documentação do
# ply Yacc.
#
# Exemplo:
# Get the token map from the lexer. This is required.
#
#     from calclex import tokens
#
#     def p_expression_plus(p):
#         'expression : expression PLUS term'
#         p[0] = p[1] + p[3]
#
# Para a entrega 3 foram adicionados alguns itens na gramática
# para poder fazer a lógica de escopos.
#
# Referência: https://www.dabeaz.com/ply/ply.html#ply_nn24

# --- Yacc rules ---


def p_PROGRAM(p: yacc.YaccProduction) -> None:
    """
    PROGRAM : NEW_SCOPE STATEMENT
            | NEW_SCOPE FUNCLIST
            | empty
    """
    pass


def p_FUNCLIST(p: yacc.YaccProduction) -> None:
    """
    FUNCLIST : FUNCDEF FUNCLISTTMP
    """
    pass


def p_FUNCLISTTMP(p: yacc.YaccProduction) -> None:
    """
    FUNCLISTTMP : FUNCLIST
                | empty
    """
    pass


def p_FUNCDEF(p: yacc.YaccProduction) -> None:
    """
    FUNCDEF : FUNCTION_DECLARATION LABEL NEW_SCOPE LEFT_PARENTHESIS PARAMLIST RIGHT_PARENTHESIS LEFT_BRACKET STATELIST RIGHT_BRACKET
    """
    # TODO DONE CONFERIR:
    scopes.pop()
    current_scope = scopes.seek()

    # Get function info to use in entry table
    func_label = p[2]
    func_line_number = p.lineno(2)

    new_func = EntryTable(
        label=func_label, datatype=DataType["func"], values=[], lineno=func_line_number
    )

    # Add function to current scope entry table
    if current_scope is not None:
        current_scope.add_entry(new_func)


# New functions to handle scopes
def p_LEFT_BRACKET(p: yacc.YaccProduction) -> None:
    """
    LEFT_BRACKET :
    """
    # TODO:
    # save current scope
    # Create new scope and pass current as father
    # move scope to the new one
    pass


def p_RIGHT_BRACKET(p: yacc.YaccProduction) -> None:
    """
    RIGHT_BRACKET :
    """
    # TODO CONFERIR:
    scopes.pop()
    pass


def p_DATATYPE(p: yacc.YaccProduction) -> None:
    """
    DATATYPE : INTEGER
             | FLOATING_POINT
             | STRING
    """
    pass


def p_PARAMLIST(p: yacc.YaccProduction) -> None:
    """
    PARAMLIST : DATATYPE LABEL PARAMLISTTMP
              | empty
    """
    # Check if token is not empty
    if len(p) > 2:
        current_scope = scopes.seek()

        paramlist_type = p[1]
        paramlist_label = p[2]
        paramlist_lineno = p.lineno(2)

        paramlist = EntryTable(
            label=paramlist_label,
            datatype=paramlist_type,
            values=[],
            lineno=paramlist_lineno,
        )
        current_scope.add_entry(paramlist)


def p_PARAMLISTTMP(p: yacc.YaccProduction) -> None:
    """
    PARAMLISTTMP : COMMA PARAMLIST
                 | empty
    """
    pass


def p_STATEMENT(p: yacc.YaccProduction) -> None:
    """
    STATEMENT : VARDECL SEMICOLON
              | ATRIBSTAT SEMICOLON
              | PRINTSTAT SEMICOLON
              | READSTAT SEMICOLON
              | RETURNSTAT SEMICOLON
              | IFSTAT
              | FORSTAT
              | STATELIST_STATEMENT
              | BREAK_STATEMENT
              | SEMICOLON
    """
    pass


def p_STATELIST_STATEMENT(p: yacc.YaccProduction) -> None:
    """
    STATELIST_STATEMENT : NEW_SCOPE LEFT_BRACKET STATELIST RIGHT_BRACKET
    """
    # TODO CONFERIR:
    scopes.pop()
    pass


def p_BREAK_STATEMENT(p: yacc.YaccProduction) -> None:
    """
    BREAK_STATEMENT : BREAK SEMICOLON
    """
    # TODO:
    # handle scope break and check if there is a loop
    current_scope = scopes.seek()

    while True:
        if current_scope.loop:
            break

        current_scope = current_scope.outer_scope

        # If there is no outer scope then it's an error
        if current_scope is not None:
            # Get error line number and raise an error
            error_lineno = p.lineno(2)
            raise InvalidBreakError(error_lineno)


def p_VARDECL(p: yacc.YaccProduction) -> None:
    """
    VARDECL : DATATYPE LABEL OPTIONAL_VECTOR
    """
    # TODO:
    # Variable info
    variable_type = p[1]
    variable_label = p[2]
    variable_values = p[3]
    variable_lineno = p.lineno(2)

    variable = EntryTable(
        label=variable_label,
        datatype=variable_type,
        values=variable_values,
        lineno=variable_lineno,
    )
    current_scope = scopes.seek()
    current_scope.add_entry(variable)
    # save variable as entry table
    # get current scope
    # add variable to current scope
    pass


def p_OPTIONAL_VECTOR(p: yacc.YaccProduction) -> None:
    """
    OPTIONAL_VECTOR : LEFT_SQUARE_BRACKET INTEGER_CONSTANT RIGHT_SQUARE_BRACKET OPTIONAL_VECTOR
                    | empty
    """
    pass


def p_ATRIB_RIGHT(p: yacc.YaccProduction) -> None:
    """
    ATRIB_RIGHT : ALLOCEXPRESSION
                | EXPRESSION_OR_FUNCCALL
    """
    pass


def p_EXPRESSION_OR_FUNCCALL(p: yacc.YaccProduction) -> None:
    """
    EXPRESSION_OR_FUNCCALL  : PLUS FACTOR RECURSIVE_UNARYEXPR RECURSIVE_MINUS_OR_PLUS OPTIONAL_REL_OP_NUMEXPRESSION
                            | MINUS FACTOR RECURSIVE_UNARYEXPR RECURSIVE_MINUS_OR_PLUS OPTIONAL_REL_OP_NUMEXPRESSION
                            | INTEGER_CONSTANT RECURSIVE_UNARYEXPR RECURSIVE_MINUS_OR_PLUS OPTIONAL_REL_OP_NUMEXPRESSION
                            | FLOATING_POINT_CONSTANT RECURSIVE_UNARYEXPR RECURSIVE_MINUS_OR_PLUS OPTIONAL_REL_OP_NUMEXPRESSION
                            | STRING_CONSTANT RECURSIVE_UNARYEXPR RECURSIVE_MINUS_OR_PLUS OPTIONAL_REL_OP_NUMEXPRESSION
                            | NULL RECURSIVE_UNARYEXPR RECURSIVE_MINUS_OR_PLUS OPTIONAL_REL_OP_NUMEXPRESSION
                            | LEFT_PARENTHESIS NUMEXPRESSION RIGHT_PARENTHESIS RECURSIVE_UNARYEXPR RECURSIVE_MINUS_OR_PLUS OPTIONAL_REL_OP_NUMEXPRESSION
                            | LABEL FOLLOW_LABEL
    """
    pass


def p_FOLLOW_LABEL(p: yacc.YaccProduction) -> None:
    """
    FOLLOW_LABEL : OPTIONAL_ALLOC_NUMEXPRESSION RECURSIVE_UNARYEXPR RECURSIVE_MINUS_OR_PLUS OPTIONAL_REL_OP_NUMEXPRESSION
                 | LEFT_PARENTHESIS PARAMLISTCALL RIGHT_PARENTHESIS
    """
    pass


def p_ATRIBSTAT(p: yacc.YaccProduction) -> None:
    """
    ATRIBSTAT : LVALUE ATTRIBUTION ATRIB_RIGHT
    """
    pass


def p_FUNCCALL(p: yacc.YaccProduction) -> None:
    """
    FUNCCALL : LABEL LEFT_PARENTHESIS PARAMLISTCALL RIGHT_PARENTHESIS
    """
    pass


def p_PARAMLISTCALL(p: yacc.YaccProduction) -> None:
    """
    PARAMLISTCALL : LABEL PARAMLISTCALLTMP
                  | empty
    """
    pass


def p_PARAMLISTCALLTMP(p: yacc.YaccProduction) -> None:
    """
    PARAMLISTCALLTMP : COMMA PARAMLISTCALL
                     | empty
    """
    pass


def p_PRINTSTAT(p: yacc.YaccProduction) -> None:
    """
    PRINTSTAT : PRINT EXPRESSION
    """
    pass


def p_READSTAT(p: yacc.YaccProduction) -> None:
    """
    READSTAT : READ LVALUE
    """
    pass


def p_RETURNSTAT(p: yacc.YaccProduction) -> None:
    """
    RETURNSTAT : RETURN
    """
    pass


def p_IFSTAT(p: yacc.YaccProduction) -> None:
    """
    IFSTAT : IF LEFT_PARENTHESIS EXPRESSION RIGHT_PARENTHESIS NEW_SCOPE STATEMENT OPTIONAL_ELSE
    """
    pass


def p_OPTIONAL_ELSE(p: yacc.YaccProduction) -> None:
    """
    OPTIONAL_ELSE : ELSE NEW_SCOPE LEFT_BRACKET STATELIST RIGHT_BRACKET
                  | empty
    """
    # TODO CONFERIR:
    if len(p) > 2:
        scopes.pop()
    pass


def p_FORSTAT(p: yacc.YaccProduction) -> None:
    """
    FORSTAT : FOR LEFT_PARENTHESIS ATRIBSTAT SEMICOLON EXPRESSION SEMICOLON ATRIBSTAT RIGHT_PARENTHESIS STATEMENT
    """
    pass


def p_STATELIST(p: yacc.YaccProduction) -> None:
    """
    STATELIST : STATEMENT OPTIONAL_STATELIST
    """
    pass


def p_OPTIONAL_STATELIST(p: yacc.YaccProduction) -> None:
    """
    OPTIONAL_STATELIST : STATELIST
                       | empty
    """
    pass


def p_ALLOCEXPRESSION(p: yacc.YaccProduction) -> None:
    """
    ALLOCEXPRESSION : NEW DATATYPE LEFT_SQUARE_BRACKET NUMEXPRESSION RIGHT_SQUARE_BRACKET OPTIONAL_ALLOC_NUMEXPRESSION
    """
    pass


def p_OPTIONAL_ALLOC_NUMEXPRESSION(p: yacc.YaccProduction) -> None:
    """
    OPTIONAL_ALLOC_NUMEXPRESSION : LEFT_SQUARE_BRACKET NUMEXPRESSION RIGHT_SQUARE_BRACKET OPTIONAL_ALLOC_NUMEXPRESSION
                                 | empty
    """
    pass


def p_EXPRESSION(p: yacc.YaccProduction) -> None:
    """
    EXPRESSION : NUMEXPRESSION OPTIONAL_REL_OP_NUMEXPRESSION
    """
    pass


def p_OPTIONAL_REL_OP_NUMEXPRESSION(p: yacc.YaccProduction) -> None:
    """
    OPTIONAL_REL_OP_NUMEXPRESSION : REL_OP NUMEXPRESSION
                                  | empty
    """
    pass


def p_REL_OP(p: yacc.YaccProduction) -> None:
    """
    REL_OP : LESSER_THAN
           | GREATER_THAN
           | LESS_OR_EQUAL_THAN
           | GREATER_OR_EQUAL_THAN
           | EQUAL
           | NOT_EQUAL
    """
    pass


def p_NUMEXPRESSION(p: yacc.YaccProduction) -> None:
    """
    NUMEXPRESSION : TERM RECURSIVE_MINUS_OR_PLUS
    """
    pass


def p_RECURSIVE_MINUS_OR_PLUS(p: yacc.YaccProduction) -> None:
    """
    RECURSIVE_MINUS_OR_PLUS : MINUS_OR_PLUS TERM RECURSIVE_MINUS_OR_PLUS
                            | empty
    """
    pass


# str
def p_MINUS_OR_PLUS(p: yacc.YaccProduction) -> None:
    """
    MINUS_OR_PLUS : MINUS
                  | PLUS
    """
    pass


def p_TERM(p: yacc.YaccProduction) -> None:
    """
    TERM : UNARYEXPR RECURSIVE_UNARYEXPR
    """
    pass


# Tuple(operator, term)
def p_RECURSIVE_UNARYEXPR(p: yacc.YaccProduction) -> None:
    """
    RECURSIVE_UNARYEXPR : UNARYEXPR_OPERATOR TERM
                        | empty
    """
    pass


def p_UNARYEXPR_OPERATOR(p: yacc.YaccProduction) -> None:
    """
    UNARYEXPR_OPERATOR : TIMES
                       | DIVISION
                       | MODULO
    """
    pass


def p_UNARYEXPR(p: yacc.YaccProduction) -> None:
    """
    UNARYEXPR : MINUS_OR_PLUS FACTOR
              | FACTOR
    """
    pass


def p_FACTOR(p: yacc.YaccProduction) -> None:
    """
    FACTOR : INTEGER_CONSTANT
           | FLOATING_POINT_CONSTANT
           | STRING_CONSTANT
           | NULL
           | LVALUE
           | LEFT_PARENTHESIS NUMEXPRESSION RIGHT_PARENTHESIS
    """
    pass


def p_LVALUE(p: yacc.YaccProduction) -> None:
    """
    LVALUE : LABEL OPTIONAL_ALLOC_NUMEXPRESSION
    """
    pass


def p_error(p: yacc.YaccProduction) -> None:
    print(f"Syntax error at token {p}")


# --- Semantic analysis ---


def p_empty(p: yacc.YaccProduction) -> None:
    "empty :"
    pass


def p_NEW_SCOPE(p: yacc.YaccProduction) -> None:
    """
    NEW_SCOPE :
    """
    create_scope(False)


def p_NEW_SCOPE_LOOP(p: yacc.YaccProduction) -> None:
    """
    NEW_LOOP_SCOPE :
    """
    create_scope(True)


def create_scope(loop: bool) -> None:
    pass
