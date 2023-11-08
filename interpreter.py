from error import LoxRuntimeError, runtime_error
from lox_token import Token
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

    def _check_number_operand(self, operator: Token, operand):
        if isinstance(operand, float):
            return
        raise RuntimeError(operator, "Operand must be a number.")

    def _check_number_operands(self, operator: Token, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise RuntimeError(operator, "Operands must be numbers.")

    def _stringify(self, value):
        if value is None:
            return "nil"

        if isinstance(value, float):
            text = str(value)

            if text.endswith(".0"):
                text = text[0: len(text) - 2]

            return text

        return str(value)

    def evaluate(self, expr: expr_n.Expr):
        return expr.accept(self)

    def visit_literal_expr(self, expr: expr_n.Literal):
        return expr.value

    def visit_grouping_expr(self, expr: expr_n.Grouping):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: expr_n.Unary):
        right = self.evaluate(expr.right)

        if expr.operator.ttype == TokenType.MINUS:
            self._check_number_operand(expr.operator, right)
            return -1 * right
        if expr.operator.ttype == TokenType.BANG:
            return not self._is_truthy(right)

        return None

    def visit_binary_expr(self, expr: expr_n.Binary):
        left = self.evaluate(expr.left)
        operator_type = expr.operator.ttype
        right = self.evaluate(expr.right)

        if operator_type == TokenType.GREATER:
            self._check_number_operands(expr.operator, left, right)
            return left > right
        if operator_type == TokenType.GREATER_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            return left >= right
        if operator_type == TokenType.LESS:
            self._check_number_operands(expr.operator, left, right)
            return left < right
        if operator_type == TokenType.LESS_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            return left <= right
        if operator_type == TokenType.MINUS:
            self._check_number_operands(expr.operator, left, right)
            return left - right
        if operator_type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right

            raise RuntimeError(expr.operator, "Operands must both be numbers / strings.")
        if operator_type == TokenType.SLASH:
            self._check_number_operands(expr.operator, left, right)
            return left / right
        if operator_type == TokenType.STAR:
            self._check_number_operands(expr.operator, left, right)
            return left * right
        if operator_type == TokenType.BANG_EQUAL:
            return not self._is_equal(left, right)
        if operator_type == TokenType.EQUAL_EQUAL:
            return self._is_equal(left, right)

        return None

    def interpret(self, expr):
        try:
            value = self.evaluate(expr)
            print(self._stringify(value))
        except LoxRuntimeError as e:
            runtime_error(e)
