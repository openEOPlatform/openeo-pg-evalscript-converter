import json
import math

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def tanh_process_code():
    return load_process_code("tanh")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 0),
        ({"x": 1}, 0.7615941559557649),
        ({"x": -1}, -0.7615941559557649),
        ({"x": math.inf}, 1),
        ({"x": None}, None),
    ],
)
def test_tanh(tanh_process_code, example_input, expected_output):
    output = run_process(tanh_process_code, "tanh", example_input)
    output = json.loads(output)
    assert pytest.approx(output) == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 0}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"y": 0.5}, True, "MISSING_PARAMETER"),
        ({"x": "0.5"}, True, "WRONG_TYPE"),
    ],
)
def test_tanh_exceptions(tanh_process_code, example_input, raises_exception, error_message):
    run_input_validation(tanh_process_code, "tanh", example_input, raises_exception, error_message)
