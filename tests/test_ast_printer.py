from ast_printer import AstPrinter
from lox_token import Token
from  nodes import expr
from token_type import TokenType
def test_ast_printer1():
    expr1 = expr.Binary(
        expr.Unary(Token(TokenType.MINUS, "-", None, 1), expr.Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        expr.Grouping(expr.Literal(45.67))
    )

    p = AstPrinter()
    assert p.print(expr1) == "(* (- 123) (group 45.67))"
