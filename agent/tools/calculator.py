import ast
import operator as op

from .base import Tool

# Only these operators are allowed -> makes this safe, unlike raw eval()
_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}


def _eval_node(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed")
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_eval_node(node.operand))
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")


class CalculatorTool(Tool):
    name = "calculator"
    description = (
        "Evaluates a math expression and returns the numeric result. "
        "Input should be a plain expression like '23 * (4 + 2) / 3'. "
        "Supports + - * / // % ** and parentheses. No variables or functions."
    )

    def run(self, tool_input: str) -> str:
        try:
            tree = ast.parse(tool_input.strip(), mode="eval")
            result = _eval_node(tree.body)
            return str(result)
        except Exception as e:
            return f"Error evaluating expression: {e}"
