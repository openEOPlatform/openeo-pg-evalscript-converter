import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def add_process_code():
    return load_process_code("add")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 1, "y": 2}, 3),
        ({"x": None, "y": 3}, None),
        ({"x": 1, "y": None}, None),
        ({"x": None, "y": None}, None),
        ({"x": -2, "y": 26}, 24),
        ({"x": -3, "y": -8}, -11),
        ({"x": 0, "y": -6}, -6),
        ({"x": -23, "y": 0}, -23),
        ({"x": 0, "y": 0}, 0),
        ({"x": 2.3, "y": -1.6}, 0.7),
        ({"x": -23.84, "y": -4.21}, -28.05),
    ],
)
def test_add(add_process_code, example_input, expected_output):
    output = run_process(add_process_code, "add", example_input)
    output = json.loads(output)
    assert pytest.approx(output) == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        ({"x": 1, "y": 2}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"y": 2}, True, "MISSING_PARAMETER"),
        ({"x": 1}, True, "MISSING_PARAMETER"),
        ({"x": False, "y": 2}, True, "WRONG_TYPE"),
        ({"x": 1, "y": False}, True, "WRONG_TYPE"),
    ],
)
def test_add_exceptions(add_process_code, example_input, raises_exception, error_name):
    run_input_validation(add_process_code, "add", example_input, raises_exception, error_name)
