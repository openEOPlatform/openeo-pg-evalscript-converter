import json

import pytest

from tests.utils import load_process_code, run_process


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
    ],
)
def test_lt(lt_code, example_input, expected_output):
    output = run_process(lt_code, "lt", example_input)
    output = json.loads(output)
    assert output == expected_output
