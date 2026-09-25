import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.tools.calculator import CalculatorTool


def test_calculator_basic_addition():
    tool = CalculatorTool()
    assert tool.run("2 + 2") == "4"


def test_calculator_expression_with_parentheses():
    tool = CalculatorTool()
    assert tool.run("(3 + 5) * 2") == "16"


def test_calculator_division():
    tool = CalculatorTool()
    assert tool.run("10 / 4") == "2.5"


def test_calculator_rejects_invalid_input():
    tool = CalculatorTool()
    result = tool.run("import os")
    assert "Error" in result
