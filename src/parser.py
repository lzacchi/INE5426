#
# parser.py
#
# Authors: Artur Barichello
#          Lucas Verdade
#          Lucas Zacchi
#
# Arquivo utilizado para análise sintática

import re
from ply import yacc
from dataclasses import dataclass
from collections import namedtuple
from typing import Any, Dict, List, Tuple
from output import VariableAlreadyDeclared, InvalidBreakError, InvalidSyntaxError
from lexer import Lexer
from data import ScopeStack, EntryTable, DataType, Scope, TreeNode
from typecheck import check_valid_operation


syntax_lexer = Lexer()
syntax_lexer.build()
tokens = syntax_lexer.tokens

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
#
#
# --- Yacc rules ---


def p_PROGRAM(p: yacc.YaccProduction) -> None:
    """
    PROGRAM : STATEMENT
            | FUNCLIST
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
    FUNCDEF : FUNCTION_DECLARATION LABEL LEFT_PARENTHESIS PARAMLIST RIGHT_PARENTHESIS LEFT_BRACKET STATELIST RIGHT_BRACKET
    """
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
    pass


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
    STATELIST_STATEMENT : LEFT_BRACKET STATELIST RIGHT_BRACKET
    """
    pass


def p_BREAK_STATEMENT(p: yacc.YaccProduction) -> None:
    """
    BREAK_STATEMENT : BREAK SEMICOLON
    """
    pass


def p_VARDECL(p: yacc.YaccProduction) -> None:
    """
    VARDECL : DATATYPE LABEL OPTIONAL_VECTOR
    """
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
    IFSTAT : IF LEFT_PARENTHESIS EXPRESSION RIGHT_PARENTHESIS STATEMENT OPTIONAL_ELSE
    """
    pass


def p_OPTIONAL_ELSE(p: yacc.YaccProduction) -> None:
    """
    OPTIONAL_ELSE : ELSE LEFT_BRACKET STATELIST RIGHT_BRACKET
                  | empty
    """
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


def p_REL_OP_LESSER_THAN(p: yacc.YaccProduction) -> None:
    """
    REL_OP : LESSER_THAN
    """
    pass


def p_REL_OP_GREATER_THAN(p: yacc.YaccProduction) -> None:
    """REL_OP : GREATER_THAN"""
    pass


def p_REL_OP_LOWER_OR_EQUAL_THAN(p: yacc.YaccProduction) -> None:
    """REL_OP : LESS_OR_EQUAL_THAN"""
    pass


def p_REL_OP_GREATER_OR_EQUAL_THAN(p: yacc.YaccProduction) -> None:
    """REL_OP : GREATER_OR_EQUAL_THAN"""
    pass


def p_REL_OP_EQUAL(p: yacc.YaccProduction) -> None:
    """REL_OP : EQUAL"""
    pass


def p_REL_OP_NOT_EQUAL(p: yacc.YaccProduction) -> None:
    """REL_OP : NOT_EQUAL"""
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


def p_UNARYEXPR_MINUS_PLUS(p: yacc.YaccProduction) -> None:
    """
    UNARYEXPR : MINUS_OR_PLUS FACTOR
    """
    pass


def p_UNARYEXPR_FACTOR(p: yacc.YaccProduction) -> None:
    """
    UNARYEXPR : FACTOR
    """
    pass


def p_FACTOR_INT_CONST(p: yacc.YaccProduction) -> None:
    """
    FACTOR : INTEGER_CONSTANT
    """
    pass


def p_FACTOR_FLOAT_CONST(p: yacc.YaccProduction) -> None:
    """
    FACTOR : FLOATING_POINT_CONSTANT
    """
    pass


def p_FACTOR_STRING_CONSTANT(p: yacc.YaccProduction) -> None:
    """
    FACTOR : STRING_CONSTANT
    """
    pass


def p_FACTOR_NULL(p: yacc.YaccProduction) -> None:
    """
    FACTOR : NULL
    """
    pass


def p_FACTOR_LVALUE(p: yacc.YaccProduction) -> None:
    """
    FACTOR : LVALUE
    """
    pass


def p_FACTOR_EXPR(p: yacc.YaccProduction) -> None:
    """
    FACTOR : LEFT_PARENTHESIS NUMEXPRESSION RIGHT_PARENTHESIS
    """
    pass


def p_LVALUE(p: yacc.YaccProduction) -> None:
    """
    LVALUE : LABEL OPTIONAL_ALLOC_NUMEXPRESSION
    """
    pass


# --- Extra productions ---


def p_error(p: yacc.YaccProduction) -> None:
    print(f"Erro sintático no token: {p}")
    raise InvalidSyntaxError(f"Erro sintático no token: {p}")


def p_empty(p: yacc.YaccProduction) -> None:
    "empty :"
    pass
