from error import report_error
from lox_token import Token
from token_type import TokenType


class Scanner:
    def __init__(self, source):
        self.source = source
        self.line = 1

        # start points to start of current lexeme. current points to current character in current lexeme.
        self.current = self.start = 0

        self.tokens = []

        self.keywords = {
            'and': TokenType.AND,
            'class': TokenType.CLASS,
            'else': TokenType.ELSE,
            'false': TokenType.FALSE,
            'for': TokenType.FOR,
            'func': TokenType.FUNC,
            'if': TokenType.IF,
            'nil': TokenType.NIL,
            'or': TokenType.OR,
            'print': TokenType.PRINT,
            'return': TokenType.RETURN,
            'super': TokenType.SUPER,
            'this': TokenType.THIS,
            'true': TokenType.TRUE,
            'var': TokenType.VAR,
            'while': TokenType.WHILE
        }

    def _is_at_end(self):
        return self.current >= len(self.source)

    # This will advance char pointer only on a successful match.
    def _match(self, expected_char):
        if self._is_at_end():
            return False

        if self.source[self.current] != expected_char:
            return False

        self.current += 1
        return True

    # This will advance the char pointer.
    def _advance(self):
        self.current += 1
        return self.source[self.current - 1]

    # This will return the current char (or None) without advancement.
    # It basically enables a 1 character lookahead.
    def _peek(self):
        if self._is_at_end():
            return None
        return self.source[self.current]

    # Enables a 2 character lookahead.
    def _peek_next(self):
        if self.current + 1 >= len(self.source):
            return None

        return self.source[self.current + 1]

    def _add_token(self, ttype, literal=None):
        self.tokens.append(Token(
            ttype,
            self.source[self.start:self.current],
            literal,
            self.line
        ))

    def _string(self, quote_char):
        while (self._peek() != quote_char) and not self._is_at_end():
            # Clearly, pylox supports multi-line strings.
            if self._peek() == '\n':
                self.line += 1
            self._advance()

        # This can't be true unless quote_char was missing. If quote_char was present,
        # self.current would be referring to quote_char instead.
        if self._is_at_end():
            report_error(self.line, "Unterminated string.")
            return

        # String is syntactically correct. Move past the quote_char.
        self._advance()

        # If pylox supported escape sequences, we'd need to unescape them here??
        value = self.source[self.start + 1: self.current - 1]
        self._add_token(TokenType.STRING, value)

    def _number(self):
        while self._peek() and self._peek().isdigit():
            self._advance()

        # In case we just have a '.' without a fractional part, we won't be raising an error.
        # This is because it could represent the dot operator.
        if self._peek() == '.' and self._peek_next().isdigit():
            self._advance()

            while self._peek() and self._peek().isdigit():
                self._advance()

        # Every number in pylox is a floating-point number.
        value = float(self.source[self.start: self.current])

        self._add_token(TokenType.NUMBER, value)

    def _identifier(self):
        while self._peek() and (self._peek().isalnum() or self._peek() == '_'):
            self._advance()

        text = self.source[self.start: self.current]
        ttype = self.keywords.get(text, TokenType.IDENTIFIER)
        self._add_token(ttype)

    def _scan_token(self):
        c = self._advance()

        if c == '(':
            self._add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self._add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self._add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self._add_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            self._add_token(TokenType.COMMA)
        elif c == '.':
            self._add_token(TokenType.DOT)
        elif c == '-':
            self._add_token(TokenType.MINUS)
        elif c == '+':
            self._add_token(TokenType.PLUS)
        elif c == '*':
            self._add_token(TokenType.STAR)
        elif c == '/':
            if self._match('/'):
                # Using _peek() here allows us to find the '\n', and wait to increment the line variable.
                while self._peek() != '\n' and not self._is_at_end():
                    self._advance()

                if c == '\n':
                    self.line += 1
            else:
                self._add_token(TokenType.SLASH)
        elif c == '=':
            self._add_token(TokenType.EQUAL_EQUAL) if self._match('=') else self._add_token(TokenType.EQUAL)
        elif c == '"' or c == '\'':
            self._string(c)
        elif c.isdigit():
            self._number()
        elif c.isalpha() or c == '_':
            self._identifier()
        elif c == ';':
            self._add_token(TokenType.SEMICOLON)
        elif c == ' ' or c == '\r':
            pass
        elif c == '\n':
            self.line += 1
        else:
            report_error(self.line, "Unexpected character.")

    def scan_tokens(self):
        while not self._is_at_end():
            self.start = self.current
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

