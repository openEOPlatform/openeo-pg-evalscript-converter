import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def absolute_process_code():
    return load_process_code("absolute")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 0),
        ({"x": 3.5}, 3.5),
        ({"x": -0.4}, 0.4),
        ({"x": -3.5}, 3.5),
        ({"x": None}, None),
    ],
)
def test_absolute(absolute_process_code, example_input, expected_output):
    output = run_process(absolute_process_code, "absolute", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_code",
    [
        ({}, True, "MISSING_PARAMETER"),
        ({"x": None}, False, None),
        ({"x": 0.3}, False, None),
        ({"x": "0.3"}, True, "WRONG_TYPE"),
    ],
)
def test_absolute_inputs(absolute_process_code, example_input, raises_exception, error_code):
    run_input_validation(absolute_process_code, "absolute", example_input, raises_exception, error_code)
