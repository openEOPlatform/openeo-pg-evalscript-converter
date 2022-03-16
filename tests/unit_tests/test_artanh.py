import json
import math

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def artanh_process_code():
    return load_process_code("artanh")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 0),
        ({"x": 0.5}, 0.549306144334055),
        (
            {"x": 1},
            None,
        ),  # JS returns Infinity, but Python doesn't recognize JS's Infinity
        ({"x": 2}, None),  # JS returns NaN, but Python doesn't recognize JS's NaN
        ({"x": None}, None),
    ],
)
def test_artanh(artanh_process_code, example_input, expected_output):
    output = run_process(artanh_process_code, "artanh", example_input)
    output = json.loads(output)
    assert expected_output == pytest.approx(output)


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        ({"x": 0}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"y": 0.5}, True, "MISSING_PARAMETER"),
        ({"x": "0.5"}, True, "WRONG_TYPE"),
    ],
)
def test_artanh_exceptions(artanh_process_code, example_input, raises_exception, error_name):
    run_input_validation(artanh_process_code, "artanh", example_input, raises_exception, error_name)
