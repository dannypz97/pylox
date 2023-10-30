from lox_token import Token
from token_type import TokenType

_had_error = False


def error(token: Token, msg):
    if token.ttype == TokenType.EOF:
        report_error(token.line, msg, " at end")
    else:
        report_error(token.lexeme, msg, f"at {token.lexeme}")

def report_error(line, msg, where=""):
    global _had_error
    print("Error: " + msg + "\n\t on line " + str(line) + "; " + where)
    _had_error = True


def clear_error():
    global _had_error
    _had_error = False


def had_error():
    return _had_error
