import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def eq_code():
    return load_process_code("eq")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 1, "y": None}, None),
        ({"x": None, "y": None}, None),
        ({"x": 1, "y": 1}, True),
        ({"x": 1, "y": "1"}, False),
        ({"x": 0, "y": False}, False),
        ({"x": 1.02, "y": 1, "delta": 0.01}, False),
        ({"x": -1, "y": -1.001, "delta": 0.01}, True),
        ({"x": 115, "y": 110, "delta": 10}, True),
        ({"x": "Test", "y": "test"}, False),
        ({"x": "Test", "y": "test", "case_sensitive": False}, True),
        ({"x": "Ä", "y": "ä", "case_sensitive": False}, True),
        # TODO handle time-strings
        # ({"x": "00:00:00+00:00", "y": "00:00:00Z"}, True),
        ({"x": "2018-01-01T12:00:00Z", "y": "2018-01-01T12:00:00"}, False),
        ({"x": "2018-01-01T00:00:00Z", "y": "2018-01-01T01:00:00+01:00"}, True),
        ({"x": "2018-01-01T00:00:00Z", "y": "2017-12-31T23:00:00-01:00"}, True),
        ({"x": "2018-01-01T01:00:00+01:00", "y": "2017-12-31T23:00:00-01:00"}, True),
        ({"x": "2018-01-01T00:00:00Z", "y": "2018-01-01"}, True),
        ({"x": [1, 2, 3], "y": [1, 2, 3]}, False),
        ({"x": [], "y": []}, False),
        ({"x": {}, "y": {}}, False),
        ({"x": True, "y": True}, True),
        ({"x": True, "y": False}, False),
    ],
)
def test_eq(eq_code, example_input, expected_output):
    output = run_process(eq_code, "eq", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        ({"x": 1, "y": 1}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"y": 0.5}, True, "MISSING_PARAMETER"),
        ({"x": "0.5"}, True, "MISSING_PARAMETER"),
    ],
)
def test_ceil_exceptions(eq_code, example_input, raises_exception, error_name):
    run_input_validation(eq_code, "eq", example_input, raises_exception, error_name)