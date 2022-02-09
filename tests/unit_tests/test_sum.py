import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def mean_process_code():
    return load_process_code("sum")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [5, 1]}, 6),
        ({"data": [-2, 4, 2.5]}, 4.5),
        ({"data": [1, None], "ignore_nodata": True}, 1),
        ({"data": [1, None], "ignore_nodata": False}, None),
        ({"data": [1, None]}, 1),
        ({"data": [100]}, 100),
        ({"data": [None], "ignore_nodata": True}, None),
        ({"data": [None], "ignore_nodata": False}, None),
        ({"data": []}, None),
        ({"data": None}, None),
        ({}, None),
    ],
)
def test_mean(mean_process_code, example_input, expected_output):
    output = run_process(mean_process_code, "sum", example_input)
    output = json.loads(output)
    assert output == expected_output
