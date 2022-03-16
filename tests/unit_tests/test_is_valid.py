import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def is_valid_code():
    return load_process_code("is_valid")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 1}, True),
        ({"x": "Test"}, True),
        ({"x": None}, False),
        ({"x": float("nan")}, False),
        ({"x": float("inf")}, False),
        ({"x": [None, None]}, True),
        ({"x": {}}, True),
    ],
)
def test_is_valid(is_valid_code, example_input, expected_output):
    output = run_process(is_valid_code, "is_valid", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        ({"x": 1}, False, None),
        ({}, True, "MISSING_PARAMETER"),
    ],
)
def test_input_validation(is_valid_code, example_input, raises_exception, error_name):
    run_input_validation(is_valid_code, "is_valid", example_input, raises_exception, error_name)
