import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def normalized_difference_process_code():
    return load_process_code("normalized_difference")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 1, "y": 1}, 0),
        ({"x": 1, "y": 0}, 1),
        ({"x": 0, "y": 1}, -1),
        ({"x": 0, "y": 27}, -1),
        ({"x": 17, "y": 29}, -0.26086956521),
        ({"x": 1.7, "y": -2.4}, -5.85714285714),
        ({"x": 17, "y": 0.2}, 0.97674418604),
    ],
)
def test_normalized_difference(normalized_difference_process_code, example_input, expected_output):
    output = run_process(normalized_difference_process_code, "normalized_difference", example_input)
    output = json.loads(output)
    assert pytest.approx(output) == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 1, "y": 1}, False, None),
        ({"x": 1, "y": -1}, True, "Division by zero is not supported."),
        ({}, True, "MISSING_PARAMETER"),
        ({"y": -1}, True, "MISSING_PARAMETER"),
        ({"x": None, "y": -1}, True, "NOT_NULL"),
        ({"x": 1}, True, "MISSING_PARAMETER"),
        ({"x": 1, "y": None}, True, "NOT_NULL"),
        ({"x": "1", "y": -1}, True, "WRONG_TYPE"),
        ({"x": 1, "y": "-1"}, True, "WRONG_TYPE"),
    ],
)
def test_normalized_difference_exceptions(
    normalized_difference_process_code, example_input, raises_exception, error_message
):
    run_input_validation(
        normalized_difference_process_code, "normalized_difference", example_input, raises_exception, error_message
    )
