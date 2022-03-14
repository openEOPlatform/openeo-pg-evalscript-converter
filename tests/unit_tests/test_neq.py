import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def neq_code():
    return load_process_code("neq")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 1, "y": None}, None),
        ({"x": 1, "y": 1}, False),
        ({"x": 1, "y": "1"}, True),
        ({"x": 0, "y": False}, True),
        ({"x": 1.02, "y": 1, "delta": 0.01}, True),
        ({"x": -1, "y": -1.001, "delta": 0.01}, False),
        ({"x": 115, "y": 110, "delta": 10}, False),
        ({"x": "Test", "y": "test"}, True),
        ({"x": "Test", "y": "test", "case_sensitive": False}, False),
        ({"x": "Ä", "y": "ä", "case_sensitive": False}, False),
        # TODO handle time-strings
        # ({"x": "00:00:00+00:00", "y": "00:00:00Z"}, False),
        ({"x": "2018-01-01T12:00:00Z", "y": "2018-01-01T12:00:00"}, True),
        ({"x": "2018-01-01T00:00:00Z", "y": "2018-01-01T01:00:00+01:00"}, False),
        ({"x": [1, 2, 3], "y": [1, 2, 3]}, False),
        ({"x": [], "y": []}, False),
        ({"x": {}, "y": {}}, False),
        ({"x": None, "y": None}, None),
        ({"x": True, "y": True}, False),
        ({"x": True, "y": False}, True),
    ],
)
def test_neq(neq_code, example_input, expected_output):
    output = run_process(neq_code, "neq", example_input)
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
def test_input_validation(neq_code, example_input, raises_exception, error_name):
    run_input_validation(neq_code, "neq", example_input, raises_exception, error_name)