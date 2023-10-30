from nodes import expr as expr_n
from token_type import TokenType

class Interpreter:
    def _is_truthy(self, val):
        # Note: original Lox implementation considers 0 to be truthy.
        if val is None or val == 0:
            return False
        if isinstance(val, bool):
            return val

        return True

    def _is_equal(self, val1, val2):
        return val1 == val2

    def evaluate(self, expr: expr_n.Expr):
        return expr.accept(self)

    def visit_literal_expr(self, expr: expr_n.Literal):
        return expr.value

    def visit_grouping_expr(self, expr: expr_n.Grouping):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: expr_n.Unary):
        right = self.evaluate(expr.right)

        if expr.operator.ttype == TokenType.MINUS:
            return -1 * right
        if expr.operator.ttype == TokenType.BANG:
            return not self._is_truthy(right)

        return None

    def visit_binary_expr(self, expr: expr_n.Binary):
        left = self.evaluate(expr.left)
        operator_type = expr.operator.ttype
        right = self.evaluate(expr.right)

        if operator_type == TokenType.GREATER:
            return left > right
        if operator_type == TokenType.GREATER_EQUAL:
            return left >= right
        if operator_type == TokenType.LESS:
            return left < right
        if operator_type == TokenType.LESS_EQUAL:
            return left <= right
        if operator_type == TokenType.MINUS:
            return left - right
        if operator_type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right
        if operator_type == TokenType.SLASH:
            return left / right
        if operator_type == TokenType.STAR:
            return left * right
        if operator_type == TokenType.BANG_EQUAL:
            return not self._is_equal(left, right)
        if operator_type == TokenType.EQUAL_EQUAL:
            return self._is_equal(left, right)

        return None

