import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def mean_process_code():
    return load_process_code("min")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [1, 0, 3, 2]}, 0),
        ({"data": [5, 2.5, None, -0.7]}, -0.7),
        ({"data": [1, 0, 3, None, 2], "ignore_nodata": False}, None),
        ({"data": [1, 0, 3, None, 2], "ignore_nodata": True}, 0),
        ({"data": [1, 0, 3, None, 2]}, 0),
        ({"data": [100]}, 100),
        ({"data": []}, None),
        ({"data": None}, None),
        ({}, None),
    ],
)
def test_mean(mean_process_code, example_input, expected_output):
    output = run_process(mean_process_code, "min", example_input)
    output = json.loads(output)
    assert output == expected_output
