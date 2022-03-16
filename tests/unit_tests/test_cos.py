import json
import math

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def cos_process_code():
    return load_process_code("cos")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 1),  # cos(0°)
        ({"x": math.pi / 6}, math.sqrt(3) / 2),  # cos(30°)
        ({"x": math.pi / 4}, math.sqrt(2) / 2),  # cos(45°)
        ({"x": math.pi / 3}, 0.5),  # cos(60°)
        ({"x": math.pi / 2}, 0),  # cos(90°)
        ({"x": math.pi}, -1),  # cos(180°)
        ({"x": 3 * math.pi / 2}, 0),  # cos(270°)
        ({"x": 2 * math.pi}, 1),  # cos(360°)
        ({"x": -math.pi / 2}, 0),  # cos(-90°)
        ({"x": None}, None),
    ],
)
def test_cos(cos_process_code, example_input, expected_output):
    output = run_process(cos_process_code, "cos", example_input)
    output = json.loads(output)
    assert pytest.approx(output) == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        ({"x": 0}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"y": 0.5}, True, "MISSING_PARAMETER"),
        ({"x": "0.5"}, True, "WRONG_TYPE"),
    ],
)
def test_cos_exceptions(cos_process_code, example_input, raises_exception, error_name):
    run_input_validation(cos_process_code, "cos", example_input, raises_exception, error_name)
