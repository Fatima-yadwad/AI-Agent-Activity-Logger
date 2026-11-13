
import pytest

from tools.calculator import CalculatorTool
from tools.tool_registry import ToolRegistry


def test_calculator_basic_operations():

    calculator = CalculatorTool()

    assert calculator.calculate("10 + 5") == 15
    assert calculator.calculate("10 - 5") == 5
    assert calculator.calculate("10 * 5") == 50
    assert calculator.calculate("10 / 5") == 2
    assert calculator.calculate("2 ** 3") == 8


def test_calculator_rejects_unsafe_expressions():

    calculator = CalculatorTool()

    with pytest.raises(ValueError):
        calculator.calculate("__import__('os').system('whoami')")


def test_calculator_rejects_division_by_zero():

    calculator = CalculatorTool()

    with pytest.raises(ValueError):
        calculator.calculate("10 / 0")


def test_tool_registry_execution():

    registry = ToolRegistry()
    registry.register("calculator", CalculatorTool())

    result = registry.execute(
        "calculator",
        expression="20 + 22"
    )

    assert result == 42


def test_tool_registry_rejects_unknown_tool():

    registry = ToolRegistry()

    with pytest.raises(ValueError):
        registry.execute("unknown_tool", expression="1 + 1")
