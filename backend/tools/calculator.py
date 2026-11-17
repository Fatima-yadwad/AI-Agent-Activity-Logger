
import ast
import operator


class CalculatorTool:

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos
    }

    def calculate(self, expression: str):

        if not expression or len(expression) > 100:
            raise ValueError("Invalid expression length.")

        try:
            tree = ast.parse(expression, mode="eval")
            result = self._evaluate(tree.body)

            if isinstance(result, bool) or not isinstance(
                result, (int, float)
            ):
                raise ValueError("Expression must produce a number.")

            if abs(result) > 1e100:
                raise ValueError("Result exceeds allowed limits.")

            return result

        except (SyntaxError, ZeroDivisionError, OverflowError) as exc:
            raise ValueError("Invalid mathematical expression.") from exc

    def _evaluate(self, node):

        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool) or not isinstance(
                node.value, (int, float)
            ):
                raise ValueError("Only numeric constants are allowed.")

            return node.value

        if isinstance(node, ast.BinOp):
            operator_function = self.OPERATORS.get(type(node.op))

            if operator_function is None:
                raise ValueError("Unsupported operator.")

            left = self._evaluate(node.left)
            right = self._evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ValueError("Exponent exceeds allowed limits.")

            result = operator_function(left, right)

            if isinstance(result, (int, float)) and abs(result) > 1e100:
                raise ValueError("Intermediate result exceeds allowed limits.")

            return result

        if isinstance(node, ast.UnaryOp):
            operator_function = self.OPERATORS.get(type(node.op))

            if operator_function is None:
                raise ValueError("Unsupported unary operator.")

            return operator_function(self._evaluate(node.operand))

        raise ValueError("Unsupported expression.")
