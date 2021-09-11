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
from data import ScopeStack, EntryTable, DataType, Scope, TreeNode
from typecheck import check_valid_operation


lexer = Lexer()
lexer.build()
tokens = lexer.tokens

# Data structures
expressions: List[Tuple[TreeNode, int]] = []
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
    p[0] = {"scopes": scopes.pop().as_dict(), "expressions": expressions}
    # Stack must be empty otherwise we have a missing scope error
    assert scopes.is_empty() == True


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

    # save variable as entry table
    variable = EntryTable(
        label=variable_label,
        datatype=variable_type,
        values=variable_values,
        lineno=variable_lineno,
    )
    # get current scope
    current_scope = scopes.seek()
    # add variable to current scope
    current_scope.add_entry(variable)
    pass


def p_OPTIONAL_VECTOR(p: yacc.YaccProduction) -> None:
    """
    OPTIONAL_VECTOR : LEFT_SQUARE_BRACKET INTEGER_CONSTANT RIGHT_SQUARE_BRACKET OPTIONAL_VECTOR
                    | empty
    """
    if len(p) > 2:
        p[0] = [p[2], *p[4]]
    else:
        p[0] = []
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


# TODO: remove this?
# def p_FUNCCALL(p: yacc.YaccProduction) -> None:
#     """
#     FUNCCALL : LABEL LEFT_PARENTHESIS PARAMLISTCALL RIGHT_PARENTHESIS
#     """
#     pass


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
    scopes.pop()


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
    FORSTAT : FOR LEFT_PARENTHESIS ATRIBSTAT SEMICOLON EXPRESSION SEMICOLON ATRIBSTAT RIGHT_PARENTHESIS NEW_LOOP_SCOPE STATEMENT
    """
    scopes.pop()


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
    numexpr = p[4]
    expressions.append((numexpr["node"], p.lineno(1)))
    pass


def p_OPTIONAL_ALLOC_NUMEXPRESSION(p: yacc.YaccProduction) -> None:
    """
    OPTIONAL_ALLOC_NUMEXPRESSION : LEFT_SQUARE_BRACKET NUMEXPRESSION RIGHT_SQUARE_BRACKET OPTIONAL_ALLOC_NUMEXPRESSION
                                 | empty
    """
    numexpr = p[2]
    numexpr_node = numexpr["node"]
    optional_numexpr = p[4]
    if len(p) < 3:
        p[0] = ""
    else:
        expressions.append((numexpr_node, p.lineno(1)))
        p[0] = f"[{str(numexpr)}]{optional_numexpr}"


def p_EXPRESSION(p: yacc.YaccProduction) -> None:
    """
    EXPRESSION : NUMEXPRESSION OPTIONAL_REL_OP_NUMEXPRESSION
    """
    numexpr = p[1]
    expressions.append((numexpr["node"], p.lineno(1)))


def p_OPTIONAL_REL_OP_NUMEXPRESSION(p: yacc.YaccProduction) -> None:
    """
    OPTIONAL_REL_OP_NUMEXPRESSION : REL_OP NUMEXPRESSION
                                  | empty
    """
    numexpr = p[2]
    numexpr_node = numexpr["node"]
    if len(p) < 3:
        pass
    else:
        expressions.append((numexpr_node, p.lineno(1)))


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
    term = p[1]
    recursive = p[2]
    if recursive is None:
        p[0] = term
    else:
        result_type = check_valid_operation(
            p[1]["node"], p[2]["node"], p[2]["operation"], p.lineno(1)
        )
        p[0] = {
            "node": TreeNode(p[1]["node"], p[2]["node"], p[2]["operation"], result_type)
        }


def p_RECURSIVE_MINUS_OR_PLUS(p: yacc.YaccProduction) -> None:
    """
    RECURSIVE_MINUS_OR_PLUS : MINUS_OR_PLUS TERM RECURSIVE_MINUS_OR_PLUS
                            | empty
    """
    if len(p) < 3:
        p[0] = None  # no recursion
    elif p[3]:
        # more recursions
        result_type = check_type(
            p[2]["node"], p[3]["node"], p[3]["operation"], p.lineno(1)
        )
        p[0] = {
            "node": TreeNode(
                p[2]["node"], p[3]["node"], p[3]["operation"], result_type
            ),
            "operation": p[1]["operation"],
        }
    else:
        # last recursion
        p[0] = {"node": p[2]["node"], "operation": p[1]["operation"]}


def p_MINUS_OR_PLUS(p: yacc.YaccProduction) -> None:
    """
    MINUS_OR_PLUS : MINUS
                  | PLUS
    """
    p[0] = {"operation": p[1]}


def p_TERM(p: yacc.YaccProduction) -> None:
    """
    TERM : UNARYEXPR RECURSIVE_UNARYEXPR
    """
    recursion = p[2]
    if recursion:
        pass
    else:
        pass


# Tuple(operator, term)
def p_RECURSIVE_UNARYEXPR(p: yacc.YaccProduction) -> None:
    """
    RECURSIVE_UNARYEXPR : UNARYEXPR_OPERATOR TERM
                        | empty
    """
    if len(p) > 2:
        term_node = p[2]["node"]
        unaryexpr_op = p[1]
        p[0] = {"node": term_node, "operation": unaryexpr_op["operation"]}
    else:
        p[0] = None


def p_UNARYEXPR_OPERATOR(p: yacc.YaccProduction) -> None:
    """
    UNARYEXPR_OPERATOR : TIMES
                       | DIVISION
                       | MODULO
    """
    p[0] = {"operation": p[1]}


def p_UNARYEXPR_MINUS_PLUS(p: yacc.YaccProduction) -> None:
    """
    UNARYEXPR : MINUS_OR_PLUS FACTOR
    """
    operation = p[1]
    factor = p[2]
    if operation["operation"] == "-":
        p[2]["node"].value = -p[2]["node"].value
    p[0] = factor


def p_UNARYEXPR_FACTOR(p: yacc.YaccProduction) -> None:
    """
    UNARYEXPR : FACTOR
    """
    p[0] = p[1]


def p_FACTOR_INT_CONST(p: yacc.YaccProduction) -> None:
    """
    FACTOR : INTEGER_CONSTANT
    """
    p[0] = {"node": TreeNode(None, None, p[1], "int")}


def p_FACTOR_FLOAT_CONST(p: yacc.YaccProduction) -> None:
    """
    FACTOR : FLOATING_POINT_CONSTANT
    """
    p[0] = {"node": TreeNode(None, None, p[1], "float")}


def p_FACTOR_STRING_CONSTANT(p: yacc.YaccProduction) -> None:
    """
    FACTOR : STRING_CONSTANT
    """
    p[0] = {"node": TreeNode(None, None, p[1], "string")}


def p_FACTOR_NULL(p: yacc.YaccProduction) -> None:
    """
    FACTOR : NULL
    """
    p[0] = {"node": TreeNode(None, None, None, "null")}


def p_FACTOR_LVALUE(p: yacc.YaccProduction) -> None:
    """
    FACTOR : LVALUE
    """
    p[0] = p[1]


def p_FACTOR_EXPR(p: yacc.YaccProduction) -> None:
    """
    FACTOR : LEFT_PARENTHESIS NUMEXPRESSION RIGHT_PARENTHESIS
    """
    p[0] = p[2]

    expressions.append((p[2]["node"], p.lineno(1)))


def p_LVALUE(p: yacc.YaccProduction) -> None:
    """
    LVALUE : LABEL OPTIONAL_ALLOC_NUMEXPRESSION
    """
    label = p[1]
    optional_alloc_numexpr = p[2]
    p[0] = {
        "node": TreeNode(
            None,
            None,
            label + optional_alloc_numexpr,
            result_type=get_variable_type(label, p.lineno(1)),
        )
    }


# --- Extra productions ---


def p_error(p: yacc.YaccProduction) -> None:
    print(f"Syntax error at token {p}")


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


# --- Util functions ---


def create_scope(loop: bool) -> None:
    """
    Scope management list
    """
    top = scopes.seek()
    new = Scope(outer_scope=top, loop=loop)
    if top:
        top.add_inner_scope(new)
    scopes.push(new)


def get_variable_type(label, lineno) -> Any:
    """
    Get variable type
    Used during TreeNode construction in LVALUEs"""
    pass
