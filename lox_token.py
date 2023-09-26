class Token:
    def __init__(self, ttype, lexeme, literal, line):
        self.ttype = ttype
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return "Token{" + f" type={self.ttype}, lexeme={self.lexeme}, literal={self.literal}, line={self.line} " + "}"
