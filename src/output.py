from ply.lex import LexToken

def print_tokens(lexer:):
    while True:
        token = lexer.token()
        if not token:
            break
        print(f"{token.}token")
