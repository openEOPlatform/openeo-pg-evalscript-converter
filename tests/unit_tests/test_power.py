import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def power_process_code():
    return load_process_code("power")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"p": 1, "base": 2}, 2),
        ({"p": 0, "base": 1234}, 1),
        ({"p": 2.718281828459045, "base": 2}, 6.5808859910179205),
        ({"p": None, "base": 2}, None),
        ({"p": 12, "base": None}, None),
        ({"p": 12, "base": 2}, 4096),
        ({"p": 0.5, "base": 4}, 2),
        ({"p": 7.54, "base": 0.5}, 0.0053732102271083736),
        ({"p": 29, "base": -1}, -1),
        ({"p": 30, "base": -1}, 1),
        ({"p": 2, "base": 0}, 0),
    ],
)
def test_power(power_process_code, example_input, expected_output):
    output = run_process(power_process_code, "power", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"p": 1, "base": 2}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"p": 2}, True, "MISSING_PARAMETER"),
        ({"base": 3}, True, "MISSING_PARAMETER"),
        ({"q": 0.5, "base": 12}, True, "MISSING_PARAMETER"),
        ({"p": "0.5", "base": 1}, True, "WRONG_TYPE"),
        ({"p": {"p": 0.5}, "base": 4}, True, "WRONG_TYPE"),
        ({"p": 12, "base": "3"}, True, "WRONG_TYPE"),
        ({"p": 2, "base": {"base": 4}}, True, "WRONG_TYPE"),
    ],
)
def test_power_exceptions(power_process_code, example_input, raises_exception, error_message):
    run_input_validation(power_process_code, "power", example_input, raises_exception, error_message)
