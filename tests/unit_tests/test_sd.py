import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def sd_process_code():
    return load_process_code("sd")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [-1, 1, 3, None]}, 2),
        ({"data": [-1, 1, 3, None], "ignore_nodata": False}, None),
        ({"data": [1]}, 0),
        ({"data": [1, -1]}, 1.4142136),
        ({"data": [1.21, 3.4, 2, 4.66, 1.5, 5.61, 7.22]}, 2.2718327),
        ({"data": []}, None),
        ({"data": [], "ignore_nodata": False}, None),
        ({"data": [0, 1, 1, 2, 2, 3, 4, 5, 6, 6]}, 2.1602469),
        ({"data": [0, 1, 1, None, 2, 2, 3, 4, 5, 6, 6]}, 2.1602469),
        ({"data": [0, 1, 1, 2, 2, 3, 4, 5, None, 6, 6], "ignore_nodata": False}, None),
        ({"data": [None]}, None),
        ({"data": [None, None, None]}, None),
        ({"data": [None, None, None], "ignore_nodata": False}, None),
    ],
)
def test_sd(sd_process_code, example_input, expected_output):
    output = run_process(sd_process_code, "sd", example_input)
    output = json.loads(output)
    assert pytest.approx(output) == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [-1, 1, 3, None]}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"data": None}, True, "NOT_NULL"),
        ({"data": 2}, True, "NOT_ARRAY"),
        ({"data": [1, 2, 3], "ignore_nodata": 12}, True, "WRONG_TYPE"),
        ({"data": [1, 2, 3, 4, "5"]}, True, "WRONG_TYPE"),
    ],
)
def test_sd_exceptions(sd_process_code, example_input, raises_exception, error_message):
    run_input_validation(sd_process_code, "sd", example_input, raises_exception, error_message)
