import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def multiply_process_code():
    return load_process_code("multiply")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 5, "y": 2.5}, 12.5),
        ({"x": -2, "y": -4}, 8),
        ({"x": 1, "y": None}, None),
        ({"x": None, "y": 3}, None),
        ({"x": None, "y": None}, None),
        ({"x": 0, "y": 1}, 0),
        ({"x": 0, "y": 0}, 0),
        ({"x": 1, "y": 1}, 1),
        ({"x": 1, "y": 4}, 4),
    ],
)
def test_multiply(multiply_process_code, example_input, expected_output):
    output = run_process(multiply_process_code, "multiply", example_input)
    output = json.loads(output)
    assert pytest.approx(output) == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 1, "y": 2}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"y": 2}, True, "MISSING_PARAMETER"),
        ({"x": 1}, True, "MISSING_PARAMETER"),
        ({"x": "2", "y": 2}, True, "WRONG_TYPE"),
        ({"x": 2, "y": "2"}, True, "WRONG_TYPE"),
    ],
)
def test_input_validation(multiply_process_code, example_input, raises_exception, error_message):
    run_input_validation(multiply_process_code, "multiply", example_input, raises_exception, error_message)