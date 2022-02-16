import json

import pytest

from tests.utils import load_process_code, run_process


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
        # TODO Temporal strings MUST be compared differently than other strings and MUST NOT be compared based on their string representation due to different possible representations
        # ({"x": "00:00:00+00:00", "y": "00:00:00Z"}, False),
        # ({"x": "2018-01-01T12:00:00Z", "y": "2018-01-01T12:00:00"}, True),
        # ({"x": "2018-01-01T00:00:00Z", "y": "2018-01-01T01:00:00+01:00"}, False),
        #
        ({"x": [1, 2, 3], "y": [1, 2, 3]}, False),
        ({"x": [], "y": []}, False),
        ({"x": {}, "y": {}}, False),
        ({"x": None, "y": None}, None),
    ],
)
def test_neq(neq_code, example_input, expected_output):
    output = run_process(neq_code, "neq", example_input)
    output = json.loads(output)
    assert output == expected_output
