import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def all_process_code():
    return load_process_code("all")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [False, None]}, False),
        ({"data": [True, None]}, True),
        ({"data": [False, None], "ignore_nodata": False}, False),
        ({"data": [True, None], "ignore_nodata": False}, None),
        ({"data": [True, False, True, False]}, False),
        ({"data": [True, False]}, False),
        ({"data": [True, True, True]}, True),
        ({"data": [True]}, True),
        ({"data": [None], "ignore_nodata": False}, None),
        ({"data": []}, None),
        ({"data": [], "ignore_nodata": False}, None),
        ({"data": [True], "ignore_nodata": False}, True),
        ({"data": [None, None, None]}, None),
        ({"data": [True, 1 < 3, 3 < 1], "ignore_nodata": False}, False),
        ({"data": [True, 1 < 3, 3 < 1]}, False),
        ({"data": [True, None, True, 1 < 3, 2 * 2 < 10, True]}, True),
        ({"data": [True, None, True, 1 < 3, 2 * 2 < 10, True], "ignore_nodata": False}, None),
        ({"data": [True, None, True, 1 < 3, 2 * 2 < 10, True, False], "ignore_nodata": False}, False),
    ],
)
def test_all(all_process_code, example_input, expected_output):
    output = run_process(all_process_code, "all", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        ({"data": [True, True, True]}, False, None),
        ({"data": "['array']"}, True, "NOT_ARRAY"),
        ({"data_array": [True, True]}, True, "MISSING_PARAMETER"),
        ({}, True, "MISSING_PARAMETER"),
        (
            {
                "data": [
                    "True",
                    True,
                    True,
                    False,
                    1 < 3,
                ]
            },
            True,
            "WRONG_TYPE",
        ),
    ],
)
def test_all_exceptions(all_process_code, example_input, raises_exception, error_name):
    run_input_validation(all_process_code, "all", example_input, raises_exception, error_name)
