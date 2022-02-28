import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def lte_code():
    return load_process_code("lte")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 1, "y": None}, None),
        ({"x": 0, "y": 0}, True),
        ({"x": 1, "y": 2}, True),
        ({"x": -0.5, "y": -0.6}, False),
        # TODO handle time-strings
        # ({"x": "00:00:00+01:00", "y": "00:00:00Z"}, True),
        ({"x": "1950-01-01T00:00:00Z", "y": "2018-01-01T12:00:00Z"}, True),
        ({"x": "2018-01-01T12:00:00+00:00", "y": "2018-01-01T12:00:00Z"}, True),
        ({"x": False, "y": True}, False),
        ({"x": False, "y": False}, True),
        ({"x": [1, 2, 3], "y": [1, 2, 3]}, False),
        ({"x": "b", "y": "a"}, False),
        ({"x": "a", "y": "a"}, True),
    ],
)
def test_lte(lte_code, example_input, expected_output):
    output = run_process(lte_code, "lte", example_input)
    output = json.loads(output)
    assert output == expected_output
