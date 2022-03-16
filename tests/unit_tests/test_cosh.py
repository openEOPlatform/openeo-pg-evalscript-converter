import json
import math

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def cosh_process_code():
    return load_process_code("cosh")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 1),
        ({"x": 1}, 1.5430806348152437),
        ({"x": -1}, 1.5430806348152437),
        ({"x": None}, None),
    ],
)
def test_cosh(cosh_process_code, example_input, expected_output):
    output = run_process(cosh_process_code, "cosh", example_input)
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
def test_cosh_exceptions(cosh_process_code, example_input, raises_exception, error_name):
    run_input_validation(cosh_process_code, "cosh", example_input, raises_exception, error_name)
