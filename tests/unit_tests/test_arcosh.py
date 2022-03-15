import json
import math

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def arcosh_process_code():
    return load_process_code("arcosh")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 1}, 0),
        ({"x": 2}, 1.3169578969248166),
        (
            {"x": 0.999999999999},
            None,
        ),  # JS returns NaN, but Python doesn't recognize JS's NaN
        ({"x": -1}, None),  # JS returns NaN, but Python doesn't recognize JS's NaN
        ({"x": 0}, None),  # JS returns NaN, but Python doesn't recognize JS's NaN
        ({"x": None}, None),
    ],
)
def test_arcosh(arcosh_process_code, example_input, expected_output):
    output = run_process(arcosh_process_code, "arcosh", example_input)
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
def test_arcosh_exceptions(arcosh_process_code, example_input, raises_exception, error_name):
    run_input_validation(arcosh_process_code, "arcosh", example_input, raises_exception, error_name)
