import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def gt_code():
    return load_process_code("gt")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 1, "y": None}, None),
        ({"x": 0, "y": 0}, False),
        ({"x": 2, "y": 1}, True),
        ({"x": -0.5, "y": -0.6}, True),
        # TODO handle time-strings
        # ({"x": "00:00:00Z", "y": "00:00:00+01:00"}, True),
        ({"x": "1950-01-01T00:00:00Z", "y": "2018-01-01T12:00:00Z"}, False),
        ({"x": "2018-01-01T12:00:00+00:00", "y": "2018-01-01T12:00:00Z"}, False),
        ({"x": True, "y": 0}, False),
        ({"x": True, "y": False}, False),
        ({"x": "b", "y": "a"}, False),
        ({"x": "a", "y": "b"}, False),
        ({"x": "c", "y": "c"}, False),
 



    ],
)
def test_gt(gt_code, example_input, expected_output):
    output = run_process(gt_code, "gt", example_input)
    output = json.loads(output)
    assert output == expected_output
