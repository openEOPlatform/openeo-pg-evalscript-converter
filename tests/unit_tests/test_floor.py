import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def floor_process_code():
    return load_process_code("floor")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 0),
        ({"x": 3.5}, 3),
        ({"x": 0.4}, 0),
        ({"x": -0.4}, -1),
        ({"x": -3.5}, -4),
        ({"x": 0.00001}, 0),
        ({"x": -0.00001}, -1),
        ({"x": 0.99999}, 0),
        ({"x": -0.99999}, -1),
    ],
)
def test_floor(floor_process_code, example_input, expected_output):
    output = run_process(floor_process_code, "floor", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 1}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"y": 0.5}, True, "MISSING_PARAMETER"),
        ({"x": "0.5"}, True, "WRONG_TYPE"),
    ],
)
def test_floor_exceptions(floor_process_code, example_input, raises_exception, error_message):
    run_input_validation(floor_process_code, "floor", example_input, raises_exception, error_message)
