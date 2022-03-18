import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def sum_process_code():
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
    ],
)
def test_sum(sum_process_code, example_input, expected_output):
    output = run_process(sum_process_code, "sum", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [1, 2]}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"data": None}, True, "NOT_NULL"),
        ({"data": 123}, True, "NOT_ARRAY"),
        ({"data": [1, 2, 3], "ignore_nodata": "False"}, True, "WRONG_TYPE"),
        ({"data": [1, 2, 3], "ignore_nodata": None}, True, "NOT_NULL"),
        ({"data": [1, 2, 3, 4, 5, True]}, True, "WRONG_TYPE"),
    ],
)
def test_input_validatio(sum_process_code, example_input, raises_exception, error_message):
    run_input_validation(sum_process_code, "sum", example_input, raises_exception, error_message)
