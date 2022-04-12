import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def order_process_code():
    return load_process_code("order")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [1, 2, 3]}, [0, 1, 2]),
        ({"data": [1, 4, 3]}, [0, 2, 1]),
        ({"data": [6, -1, 2, 7, 4, 8, 3, 9, 9]}, [1, 2, 6, 4, 0, 3, 5, 7, 8]),
        ({"data": [6, -1, 2, 7, 4, 8, 3, 9, 9], "asc": False}, [7, 8, 5, 3, 0, 4, 6, 2, 1]),
        ({"data": [6, -1, 2, None, 7, 4, None, 8, 3, 9, 9]}, [1, 2, 8, 5, 0, 4, 7, 9, 10]),
        ({"data": [6, -1, 2, None, 7, 4, None, 8, 3, 9, 9], "nodata": True}, [1, 2, 8, 5, 0, 4, 7, 9, 10, 3, 6]),
        (
            {"data": [6, -1, 2, None, 7, 4, None, 8, 3, 9, 9], "asc": False, "nodata": True},
            [9, 10, 7, 4, 0, 5, 8, 2, 1, 3, 6],
        ),
        (
            {"data": [6, -1, 2, None, 7, 4, None, 8, 3, 9, 9], "asc": False, "nodata": False},
            [3, 6, 9, 10, 7, 4, 0, 5, 8, 2, 1],
        ),
        ({"data": ["2020-01-01T12:00:00Z", "2021-01-01T12:00:00Z", "2022-01-01T12:00:00Z"]}, [0, 1, 2]),
        ({"data": ["2022-01-01T12:00:00Z", "2021-01-01T12:00:00Z", "2020-01-01T12:00:00Z"]}, [2, 1, 0]),
    ],
)
def test_order(order_process_code, example_input, expected_output):
    output = run_process(order_process_code, "order", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        ({"data": [1, 2, 3]}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"data": False}, True, "NOT_ARRAY"),
        ({"data": None}, True, "NOT_NULL"),
        ({"data": [1, 2, 3], "asc": True}, False, None),
        ({"data": [1, 2, 3], "asc": None}, True, "NOT_NULL"),
        ({"data": [1, 2, 3], "nodata": False}, False, None),
        ({"data": [1, 2, 3], "nodata": None}, False, None),
        ({"data": [1, 2, 3], "nodata": []}, True, "WRONG_TYPE"),
        (
            {"data": [1, True, 2, 3]},
            True,
            "Element in argument `data` is not a number, null or a valid ISO date string.",
        ),
        (
            {"data": [1, "random string", 2, 3]},
            True,
            "Element in argument `data` is not a number, null or a valid ISO date string.",
        ),
    ],
)
def test_order_inputs(order_process_code, example_input, raises_exception, error_name):
    run_input_validation(order_process_code, "order", example_input, raises_exception, error_name)
