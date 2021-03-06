import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def max_process_code():
    return load_process_code("max")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [1, 2]}, 2),
        ({"data": [1, 0, 3, 2]}, 3),
        ({"data": [5, 2.5, None, 4]}, 5),
        ({"data": [-1, -3, -2.5, None, -10]}, -1),
        ({"data": [-1, -3, -2.5, None, -10, 0]}, 0),
        ({"data": [-1, -3, -2.5, None, -10], "ignore_nodata": False}, None),
        ({"data": []}, None),
        ({"data": [], "ignore_nodata": False}, None),
        ({"data": [None]}, None),
        ({"data": [1.0001, 1.00001, 1, 1.0002], "ignore_nodata": False}, 1.0002),
    ],
)
def test_max(max_process_code, example_input, expected_output):
    output = run_process(max_process_code, "max", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [1, 2]}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"data": 123}, True, "NOT_ARRAY"),
        ({"data": [1, 2, 3], "ignore_nodata": "False"}, True, "WRONG_TYPE"),
        ({"data": [1, 2, 3], "ignore_nodata": None}, True, "NOT_NULL"),
        ({"data": [1, 2, 3, 4, 5, True]}, True, "WRONG_TYPE"),
    ],
)
def test_max_exceptions(max_process_code, example_input, raises_exception, error_message):
    run_input_validation(max_process_code, "max", example_input, raises_exception, error_message)
