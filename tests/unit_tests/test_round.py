import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def round_process_code():
    return load_process_code("round")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 0),
        ({"x": -2.5}, -2),
        ({"x": 3.5}, 4),
        ({"x": 0.4}, 0),
        ({"x": -0.4}, 0),
        ({"x": -3.5}, -4),
        ({"x": 0.00001}, 0),
        ({"x": -0.00001}, 0),
        ({"x": 0.99999}, 1),
        ({"x": -0.99999}, -1),
        ({"x": 2.6}, 3),
        ({"x": 1234.5, "p": -2}, 1200),
        ({"x": 1.5, "p": 0}, 2),
        ({"x": -2.5, "p": 0}, -2),
        ({"x": 3.2421, "p": 1}, 3.2),
        ({"x": 3.2421, "p": 3}, 3.242),
        ({"x": 3.2425, "p": 3}, 3.242),
        ({"x": 3.2435, "p": 3}, 3.244),
        ({"x": 1234, "p": -1}, 1230),
        ({"x": 1235, "p": -1}, 1240),
        ({"x": 12345, "p": -1}, 12340),
        ({"x": 12345, "p": -3}, 12000),
        ({"x": 3.56, "p": 1}, 3.6),
        ({"x": -0.4444444, "p": 2}, -0.44),
        ({"x": None, "p": 3}, None),
        ({"x": None}, None),
    ],
)
def test_round(round_process_code, example_input, expected_output):
    output = run_process(round_process_code, "round", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 1}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"y": 0.5}, True, "MISSING_PARAMETER"),
        ({"x": "0.5"}, True, "WRONG_TYPE"),
        ({"x": 0.2, "p": "2"}, True, "NOT_INTEGER"),
        ({"x": 0.3, "p": 1.3}, True, "NOT_INTEGER"),
    ],
)
def test_round_exceptions(round_process_code, example_input, raises_exception, error_message):
    run_input_validation(round_process_code, "round", example_input, raises_exception, error_message)
