import json
import math

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def sin_process_code():
    return load_process_code("sin")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 0),  # sin(0°)
        ({"x": math.pi / 6}, 0.5),  # sin(30°)
        ({"x": math.pi / 4}, math.sqrt(2) / 2),  # sin(45°)
        ({"x": math.pi / 3}, math.sqrt(3) / 2),  # sin(60°)
        ({"x": math.pi / 2}, 1),  # sin(90°)
        ({"x": math.pi}, 0),  # sin(180°)
        ({"x": 3 * math.pi / 2}, -1),  # sin(270°)
        ({"x": 2 * math.pi}, 0),  # sin(360°)
        ({"x": -math.pi / 2}, -1),  # sin(-90°)
        ({"x": None}, None),
    ],
)
def test_sin(sin_process_code, example_input, expected_output):
    output = run_process(sin_process_code, "sin", example_input)
    output = json.loads(output)
    assert pytest.approx(output) == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 0}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"y": 0.5}, True, "MISSING_PARAMETER"),
        ({"x": "0.5"}, True, "WRONG_TYPE"),
    ],
)
def test_sin_exceptions(sin_process_code, example_input, raises_exception, error_message):
    run_input_validation(sin_process_code, "sin", example_input, raises_exception, error_message)
