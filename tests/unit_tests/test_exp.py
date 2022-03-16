import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def exp_process_code():
    return load_process_code("exp")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"p": 1}, 2.718281828459045),
        ({"p": 2.718281828459045}, 15.154262241479262),
        ({"p": None}, None),
        ({"p": 2.3}, 9.974182454814718),
        ({"p": -1.2}, 0.3011942119122021),
        ({"p": -6.9}, 0.0010077854290485105),
        ({"p": 0}, 1),
    ],
)
def test_exp(exp_process_code, example_input, expected_output):
    output = run_process(exp_process_code, "exp", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"p": 1}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"q": 0.5}, True, "MISSING_PARAMETER"),
        ({"p": "0.5"}, True, "WRONG_TYPE"),
        ({"p": {"p": 0.5}}, True, "WRONG_TYPE"),
    ],
)
def test_exp_exceptions(exp_process_code, example_input, raises_exception, error_message):
    run_input_validation(exp_process_code, "exp", example_input, raises_exception, error_message)
