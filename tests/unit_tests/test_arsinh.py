import json
import math

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def arsinh_process_code():
    return load_process_code("arsinh")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 0),
        ({"x": 1}, 0.881373587019543),
        ({"x": -1}, -0.881373587019543),
        ({"x": None}, None),
    ],
)
def test_arsinh(arsinh_process_code, example_input, expected_output):
    output = run_process(arsinh_process_code, "arsinh", example_input)
    output = json.loads(output)
    assert pytest.approx(output) == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        ({"x": 0}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"y": 0.5}, True, "MISSING_PARAMETER"),
        ({"x": "0.5"}, True, "WRONG_TYPE"),
    ],
)
def test_arsinh_exceptions(arsinh_process_code, example_input, raises_exception, error_name):
    run_input_validation(arsinh_process_code, "arsinh", example_input, raises_exception, error_name)
