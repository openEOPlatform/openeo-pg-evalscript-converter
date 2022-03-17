import json
import math

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def sinh_process_code():
    return load_process_code("sinh")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 0),
        ({"x": 1}, 1.1752011936438014),
        ({"x": -1}, -1.1752011936438014),
        ({"x": None}, None),
    ],
)
def test_sinh(sinh_process_code, example_input, expected_output):
    output = run_process(sinh_process_code, "sinh", example_input)
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
def test_sinh_exceptions(sinh_process_code, example_input, raises_exception, error_message):
    run_input_validation(sinh_process_code, "sinh", example_input, raises_exception, error_message)
