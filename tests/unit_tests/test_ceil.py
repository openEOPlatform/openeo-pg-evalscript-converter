import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def ceil_process_code():
    return load_process_code("ceil")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 0),
        ({"x": 3.5}, 4),
        ({"x": -0.4}, 0),
        ({"x": -3.5}, -3),
        ({"x": 0.00001}, 1),
        ({"x": -0.00001}, 0),
        ({"x": 0.99999}, 1),
        ({"x": -0.99999}, 0),
    ],
)
def test_ceil(ceil_process_code, example_input, expected_output):
    output = run_process(ceil_process_code, "ceil", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        ({"x": 1}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"y": 0.5}, True, "MISSING_PARAMETER"),
        ({"x": "0.5"}, True, "WRONG_TYPE"),
    ],
)
def test_ceil_exceptions(ceil_process_code, example_input, raises_exception, error_name):
    run_input_validation(ceil_process_code, "ceil", example_input, raises_exception, error_name)
