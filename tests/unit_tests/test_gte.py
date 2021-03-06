import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def gte_code():
    return load_process_code("gte")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 1, "y": None}, None),
        ({"x": 0, "y": 0}, True),
        ({"x": 1, "y": 2}, False),
        ({"x": -0.5, "y": -0.6}, True),
        # TODO handle time-strings
        # ({"x": "00:00:00Z", "y": "00:00:00+01:00"}, True),
        ({"x": "1950-01-01T00:00:00Z", "y": "2018-01-01T12:00:00Z"}, False),
        ({"x": "2018-01-01T12:00:00+00:00", "y": "2018-01-01T12:00:00Z"}, True),
        ({"x": True, "y": False}, False),
        ({"x": True, "y": True}, True),
        ({"x": True, "y": 1}, False),
        ({"x": 0, "y": False}, False),
        ({"x": [1, 2, 3], "y": [1, 2, 3]}, False),
        ({"x": [], "y": []}, False),
        ({"x": {}, "y": {}}, False),
        ({"x": None, "y": None}, None),
        ({"x": "b", "y": "a"}, False),
        ({"x": "a", "y": "a"}, True),
    ],
)
def test_gte(gte_code, example_input, expected_output):
    output = run_process(gte_code, "gte", example_input)
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
def test_input_validation(gte_code, example_input, raises_exception, error_name):
    run_input_validation(gte_code, "gte", example_input, raises_exception, error_name)
