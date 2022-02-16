import json

import pytest

from tests.utils import load_process_code, run_process


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
        #  TODO: Temporal strings can not be compared based on their string representation due to the time zone / time-offset representations.
        ({"x": "00:00:00Z", "y": "00:00:00+01:00"}, True),
        ({"x": "1950-01-01T00:00:00Z", "y": "2018-01-01T12:00:00Z"}, False),
        # ({"x": "2018-01-01T12:00:00+00:00", "y": "2018-01-01T12:00:00Z"}, True),
        #
        ({"x": True, "y": False}, False),
        ({"x": True, "y": 1}, False),
        ({"x": 0, "y": False}, False),
        ({"x": [1, 2, 3], "y": [1, 2, 3]}, False),
        ({"x": [], "y": []}, False),
        ({"x": {}, "y": {}}, False),
        ({"x": None, "y": None}, None),
    ],
)
def test_gte(gte_code, example_input, expected_output):
    output = run_process(gte_code, "gte", example_input)
    output = json.loads(output)
    assert output == expected_output
