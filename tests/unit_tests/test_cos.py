import json
import math

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def cos_process_code():
    return load_process_code("cos")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 1),  # cos(0°)
        ({"x": math.pi / 6}, pytest.approx(math.sqrt(3) / 2)),  # cos(30°)
        ({"x": math.pi / 4}, pytest.approx(math.sqrt(2) / 2)),  # cos(45°)
        ({"x": math.pi / 3}, pytest.approx(0.5)),  # cos(60°)
        ({"x": math.pi / 2}, pytest.approx(0)),  # cos(90°)
        ({"x": math.pi}, -1),  # cos(180°)
        ({"x": 3 * math.pi / 2}, pytest.approx(0)),  # cos(270°)
        ({"x": 2 * math.pi}, 1),  # cos(360°)
        ({"x": -math.pi / 2}, pytest.approx(0)),  # cos(-90°)
        ({"x": None}, None),
    ],
)
def test_cos(cos_process_code, example_input, expected_output):
    output = run_process(cos_process_code, "cos", example_input)
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
def test_cos_exceptions(
    cos_process_code, example_input, raises_exception, error_message
):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(cos_process_code, "cos", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(cos_process_code, "cos", example_input)
