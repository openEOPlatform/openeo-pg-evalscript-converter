import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def log_process_code():
    return load_process_code("log")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 1, "base": 10}, 0),
        ({"x": 2.718281828459045, "base": 2.718281828459045}, 1),
        ({"x": None, "base": 10}, None),
        ({"x": 4, "base": None}, None),
        ({"x": 123, "base": 2.718281828459045}, 4.812184355372417),
        ({"x": 10, "base": 100}, 0.5),
        ({"x": 16, "base": 2}, 4),
        ({"x": 1234, "base": 17}, 2.512347409134643),
    ],
)
def test_log(log_process_code, example_input, expected_output):
    output = run_process(log_process_code, "log", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 1, "base": 10}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"y": 0.5}, True, "MISSING_PARAMETER"),
        ({"x": 0.5}, True, "MISSING_PARAMETER"),
        ({"base": 10}, True, "MISSING_PARAMETER"),
        ({"x": "0.5", "base": 10}, True, "WRONG_TYPE"),
        ({"x": 0.5, "base": "10"}, True, "WRONG_TYPE"),
    ],
)
def test_log_exceptions(log_process_code, example_input, raises_exception, error_message):
    run_input_validation(log_process_code, "log", example_input, raises_exception, error_message)
