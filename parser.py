from typing import List

from error import error
from lox_token import Token
from nodes.expr import *
from token_type import TokenType

# expression → equality ;
# equality → comparison ( ( "!=" | "==" ) comparison )* ;
# comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
# term → factor ( ( "-" | "+" ) factor )* ;
# factor → unary ( ( "/" | "*" ) unary )* ;
# unary → ( "!" | "-" ) unary | primary ;
# primary → NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" ;


class Parser:
    class ParseException(Exception):
        pass

    def __init__(self, tokens):
        self.tokens: List[Token] = tokens
        self.current = 0

    def _match(self, *token_types):
        for token_type in token_types:
            if self._check(token_type):
                self._advance()
                return True

        return False

    def _check(self, token_type):
        if self._is_at_end():
            return False
        return self._peek().ttype == token_type

    def _advance(self):
        if not self._is_at_end():
            self.current += 1

        return self._previous()

    def _is_at_end(self):
        return self._peek() == TokenType.EOF

    def _peek(self):
        return self.tokens[self.current]

    def _previous(self):
        return self.tokens[self.current - 1]

    def _consume(self, token_type, msg):
        if self._check(token_type):
            return self._advance()

        raise self.error(self._peek(), msg)

    # Discard tokens that can potentially cause cascaded errors. Discard until we reach the statement boundary.
    def _synchronize(self):
        self._advance()

        while not self._is_at_end():
            if self._previous().ttype == TokenType.SEMICOLON:
                return

            if self._peek().ttype in [TokenType.CLASS, TokenType.FUNC, TokenType.VAR, TokenType.FOR, TokenType.IF, TokenType.WHILE,
                                      TokenType.PRINT, TokenType.RETURN]:
                return

            self._advance()

    @staticmethod
    def error(token: Token, msg):
        error(token, msg)

        # Throwing an error instead of reporting it lets us unwind. This helps in synchronization?
        return Parser.ParseException()

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()

        while self._match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            operator = self._previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self):
        expr = self.term()

        while self._match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self._previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self._match(TokenType.MINUS, TokenType.PLUS):
            operator = self._previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self._match(TokenType.SLASH, TokenType.STAR):
            operator = self._previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self):
        if self._match(TokenType.FALSE):
            return Literal(False)
        if self._match(TokenType.TRUE):
            return Literal(True)
        if self._match(TokenType.NIL):
            return Literal(None)

        if self._match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self._previous().literal)

        if self._match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self._consume(TokenType.RIGHT_PAREN, "')' expected after expression.")
            return Grouping(expr)

        raise self.error(self._peek(), "Expect expression.")

    def parse(self):
        try:
            return self.expression()
        except Parser.ParseException:
            return None
