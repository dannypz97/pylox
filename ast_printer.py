from nodes import expr


class AstPrinter:
    def print(self, expression):
        return expression.accept(self)

    def _parenthesize(self, name, *expressions: expr.Expr):
        result = "(" + name

        for expression in expressions:
            result += f" {expression.accept(self)}"

        result += ")"

        return result

    def visit_binary_expr(self, expression: expr.Binary):
        return self._parenthesize(expression.operator.lexeme, expression.left, expression.right)

    def visit_grouping_expr(self, expression: expr.Grouping):
        return  self._parenthesize("group", expression.expression)

    def visit_literal_expr(self, expression: expr.Literal):
        if expression is None:
            return "nil"

        return expression.value

    def visit_unary_expr(self, expression: expr.Unary):
        return self._parenthesize(expression.operator.lexeme, expression.right)


