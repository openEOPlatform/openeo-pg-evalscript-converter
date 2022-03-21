import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def median_process_code():
    return load_process_code("median")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [1, 3, 3, 6, 7, 8, 9]}, 6),
        ({"data": [3, 7, 6, 8, 7, 1, 3]}, 6),
        ({"data": [1, 2, 3, 4, 5, 6, 8, 9]}, 4.5),
        ({"data": [8, 6, 1, 4, 3, 9, 5, 2]}, 4.5),
        ({"data": [1, 2, 3]}, 2),
        ({"data": [1, 3, 2]}, 2),
        ({"data": [1, 2, 3, 4]}, 2.5),
        ({"data": [2, 1, 3, 4]}, 2.5),
        ({"data": [-1, -0.5, None, 1]}, -0.5),
        ({"data": [-1, 0, None, 1], "ignore_nodata": False}, None),
        ({"data": []}, None),
        ({"data": [], "ignore_nodata": False}, None),
        ({"data": [None, None, None, None]}, None),
        ({"data": [None, None, None, None], "ignore_nodata": False}, None),
    ],
)
def test_median(median_process_code, example_input, expected_output):
    output = run_process(median_process_code, "median", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [1, 0, 3, 2]}, False, None),
        ({"data_fake": [1, 0, 3, 2]}, True, "MISSING_PARAMETER"),
        ({"data": "[1,0,3,2]"}, True, "NOT_ARRAY"),
        ({"data": [1, 0, 3, 2], "ignore_nodata": [1, 2, 3]}, True, "WRONG_TYPE"),
        ({"data": [1, 0, 3, 2], "ignore_nodata": None}, True, "NOT_NULL"),
        ({"data": [1, 2, 3, None, "1"]}, True, "WRONG_TYPE"),
    ],
)
def test_median_exceptions(median_process_code, example_input, raises_exception, error_message):
    run_input_validation(median_process_code, "median", example_input, raises_exception, error_message)
