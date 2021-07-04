# Comments with 'updated' indicate where the grammar
# has been modified to mirror operators used in the
# Lua language (https://www.lua.org/)

import ply.lex as lex
from ply.lex import LexToken


class Lexer(object):
    reserved = {
        "def": "DEF",
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

    tokens = list(reserved.values()) + [
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
        "MODULUS",
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
    t_MODULUS = r"%"

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
        r"[a-zA-Z][A-Za-z0-9]*"
        t.type = self.reserved.get(t.value, "LABEL")
        return t

    def t_FLOATING_POINT_CONSTANT(self, t: LexToken) -> LexToken:
        r"\d+\.d+"
        t.value = float(t.value)
        return t

    def t_INTEGER_CONSTANT(self, t: LexToken) -> LexToken:
        r"\d+"
        t.value = int(t.value)
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t: LexToken) -> LexToken:
        r"\n+"
        t.lexer.lineno += len(t.value)

    # ---

    # Compute column
    # token is a token instance
    def find_column(self, token: LexToken) -> LexToken:
        pass
        # TODO
        # line_start = self._input.rfind("\n", 0, token.lexpos) + 1
        # return (token.lexpos - line_start) + 1

    # Error handling rule
    def t_error(self, t: LexToken) -> None:
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def build(self, **kwargs: dict) -> None:
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, src: str, **kwargs: int) -> None:
        self.src = src
        self.lexer.input(src)

    # Test it output
    def test(self, data: str) -> None:
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

    def token(self) -> LexToken:
        return self.lexer.token()
