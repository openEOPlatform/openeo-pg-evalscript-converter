import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def min_process_code():
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
    ],
)
def test_min(min_process_code, example_input, expected_output):
    output = run_process(min_process_code, "min", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [1, 2]}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"data": 123}, True, "NOT_ARRAY"),
        ({"data": [1, 2, 3], "ignore_nodata": "False"}, True, "WRONG_TYPE"),
        ({"data": [1, 0, 3, 2], "ignore_nodata": None}, True, "NOT_NULL"),
        ({"data": [1, 2, 3, 4, 5, True]}, True, "WRONG_TYPE"),
    ],
)
def test_input_validation(min_process_code, example_input, raises_exception, error_message):
    run_input_validation(min_process_code, "min", example_input, raises_exception, error_message)
