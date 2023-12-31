from enum import Enum, auto


class TokenType:
    # Single-character tokens
    LEFT_PAREN = 0
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # One or two character tokens
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUNC = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    EOF = auto()


# TokenType = Enum(
#     "TokenType",
#     [
#         # Single-character tokens
#         "LEFT_PAREN", "RIGHT_PAREN", "LEFT_BRACE", "RIGHT_BRACE", "COMMA", "DOT", "MINUS", "PLUS", "SEMICOLON", "SLASH", "STAR",
#
#         # One or two character tokens
#         "BANG", "BANG_EQUAL", "EQUAL", "EQUAL_EQUAL", "GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL",
#
#         # Literals
#         "IDENTIFIER", "STRING", "NUMBER",
#
#         # Keywords
#         "AND", "CLASS", "ELSE", "FALSE", "FUNC", "FOR", "IF", "NIL", "OR",
#         "PRINT", "RETURN", "SUPER", "THIS", "TRUE", "VAR", "WHILE",
#
#         # EOF
#         "EOF"
#     ],
#     start=0
# )
