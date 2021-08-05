#
# lexer.py
#
# Authors: Artur Barichello
#          Lucas Verdade
#          Lucas Zacchi

# Comments with 'updated' indicate where the grammar
# has been modified to mirror operators used in the
# Lua language (https://www.lua.org/)

import ply.lex as lex
from ply.lex import LexToken
from typing import List
from output import InvalidTokenError

RESERVED = {
    "def": "FUNCTION_DECLARATION",
    "int": "INTEGER",
    "float": "FLOATING_POINT",
    "string": "STRING",
    "break": "BREAK",
    "print": "PRINT",
    "read": "READ",
    "return": "RETURN",
    "if": "IF",
    "else": "ELSE",
    "for": "FOR",
    "new": "NEW",
}

TOKENS = list(RESERVED.values()) + [
    # boolean operators
    "LESSER_THAN",
    "GREATER_THAN",
    "LESS_OR_EQUAL_THAN",
    "GREATER_OR_EQUAL_THAN",
    "EQUAL",
    "NOT_EQUAL",
    # math operators
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVISION",
    "MODULO",
    # limits
    "COMMA",
    "SEMICOLON",
    "LEFT_BRACKET",
    "RIGHT_BRACKET",
    "LEFT_PARENTHESIS",
    "RIGHT_PARENTHESIS",
    "LEFT_SQUARE_BRACKET",
    "RIGHT_SQUARE_BRACKET",
    # etc
    "NULL",
    "COMMENT",
    "ATTRIBUTION",
    "STRING_CONSTANT",
    "LABEL",  # 'ident'
    "FLOATING_POINT_CONSTANT",
    "INTEGER_CONSTANT",
]


class Lexer(object):
    reserved = RESERVED
    tokens = TOKENS

    # Tokens regular expression
    t_LESSER_THAN = r"<"
    t_GREATER_THAN = r">"
    t_LESS_OR_EQUAL_THAN = r"<="
    t_GREATER_OR_EQUAL_THAN = r">="
    t_EQUAL = r"=="
    t_NOT_EQUAL = r"~="  # updated

    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_TIMES = r"\*"
    t_DIVISION = r"\/"
    t_MODULO = r"%"

    t_COMMA = r","
    t_SEMICOLON = r";"
    t_LEFT_BRACKET = r"{"
    t_RIGHT_BRACKET = r"}"
    t_LEFT_PARENTHESIS = r"\("
    t_RIGHT_PARENTHESIS = r"\)"
    t_LEFT_SQUARE_BRACKET = r"\["
    t_RIGHT_SQUARE_BRACKET = r"\]"

    t_ignore_COMMENT = r"--.*"  # updated
    t_ignore = " \t"  # updated
    t_NULL = r"nil"  # updated
    t_ATTRIBUTION = r"="
    t_STRING_CONSTANT = r'".*"'

    def t_LABEL(self, t: LexToken) -> LexToken:
        r"[a-zA-Z][A-Za-z0-9_]*"
        t.type = self.reserved.get(t.value, "LABEL")
        t.value = t.value
        return t

    def t_FLOATING_POINT_CONSTANT(self, t: LexToken) -> LexToken:
        r"\d+\.\d+"
        t.value = float(t.value)
        return t

    def t_INTEGER_CONSTANT(self, t: LexToken) -> LexToken:
        r"\d+"
        t.value = int(t.value)
        return t

    def t_newline(self, t: LexToken) -> LexToken:
        r"\n+"
        t.lexer.lineno += len(t.value)

    # ---

    def find_column(self, t: LexToken) -> int:
        line_start = self.src.rfind("\n", 0, t.lexpos) + 1
        return (t.lexpos - line_start) + 1

    def t_error(self, t: LexToken) -> None:
        # Simulating a Lua error message
        print(
            f"Input file({t.lineno}:{self.find_column(t)}) '{t.value[0]}' is an invalid character"
        )
        t.lexer.skip(1)
        raise InvalidTokenError()

    def build(self, **kwargs: dict) -> None:
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, src: str, **kwargs: int) -> None:
        self.src = src
        self.lexer.input(src)

    def token_list(self) -> List:
        result: List = []
        while True:
            token = self.lexer.token()
            if not token:
                break
            result.append(token)
        return result
