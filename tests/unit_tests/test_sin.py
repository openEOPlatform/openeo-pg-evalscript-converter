import json
import math

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def sin_process_code():
    return load_process_code("sin")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 0),  # sin(0°)
        ({"x": math.pi / 6}, pytest.approx(0.5)),  # sin(30°)
        ({"x": math.pi / 4}, pytest.approx(math.sqrt(2) / 2)),  # sin(45°)
        ({"x": math.pi / 3}, pytest.approx(math.sqrt(3) / 2)),  # sin(60°)
        ({"x": math.pi / 2}, 1),  # sin(90°)
        ({"x": math.pi}, pytest.approx(0)),  # sin(180°)
        ({"x": 3 * math.pi / 2}, -1),  # sin(270°)
        ({"x": 2 * math.pi}, pytest.approx(0)),  # sin(360°)
        ({"x": -math.pi / 2}, -1),  # sin(-90°)
        ({"x": None}, None),
    ],
)
def test_sin(sin_process_code, example_input, expected_output):
    output = run_process(sin_process_code, "sin", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 0}, False, None),
        ({}, True, "Mandatory argument `x` is not defined."),
        ({"y": 0.5}, True, "Mandatory argument `x` is not defined."),
        ({"x": "0.5"}, True, "Argument `x` is not a number."),
    ],
)
def test_sin_exceptions(
    sin_process_code, example_input, raises_exception, error_message
):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(sin_process_code, "sin", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(sin_process_code, "sin", example_input)
