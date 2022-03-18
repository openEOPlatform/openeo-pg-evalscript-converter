import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def lt_code():
    return load_process_code("lt")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 1, "y": None}, None),
        ({"x": 0, "y": 0}, False),
        ({"x": 1, "y": 2}, True),
        ({"x": -0.5, "y": -0.6}, False),
        # TODO handle time-strings
        # ({"x": "00:00:00+01:00", "y": "00:00:00Z"}, True),
        ({"x": "1950-01-01T00:00:00Z", "y": "2018-01-01T12:00:00Z"}, True),
        ({"x": "2018-01-01T12:00:00+00:00", "y": "2018-01-01T12:00:00Z"}, False),
        ({"x": 0, "y": True}, False),
        ({"x": False, "y": True}, False),
        ({"x": "a", "y": "b"}, False),
        ({"x": "b", "y": "a"}, False),
        ({"x": "c", "y": "c"}, False),
    ],
)
def test_lt(lt_code, example_input, expected_output):
    output = run_process(lt_code, "lt", example_input)
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
def test_input_validation(lt_code, example_input, raises_exception, error_name):
    run_input_validation(lt_code, "lt", example_input, raises_exception, error_name)
