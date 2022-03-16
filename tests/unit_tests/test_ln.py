import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def ln_process_code():
    return load_process_code("ln")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 1}, 0),
        ({"x": 2.718281828459045}, 1),
        ({"x": None}, None),
        ({"x": 123}, 4.812184355372417),
        ({"x": 1234}, 7.1180162044653335),
        ({"x": 29.3}, 3.3775875160230218),
    ],
)
def test_ln(ln_process_code, example_input, expected_output):
    output = run_process(ln_process_code, "ln", example_input)
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
def test_ln_exceptions(ln_process_code, example_input, raises_exception, error_message):
    run_input_validation(ln_process_code, "ln", example_input, raises_exception, error_message)
