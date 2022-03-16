import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def array_filter_process_code():
    return load_process_code("array_filter")


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        ({}, True, "MISSING_PARAMETER"),
        ({"data": 1}, True, "NOT_ARRAY"),
        ({"data": [1, 2]}, True, "MISSING_PARAMETER"),
        ({"data": [1, 2], "condition": True}, True, "WRONG_TYPE"),
    ],
)
def test_array_filter_inputs(array_filter_process_code, example_input, raises_exception, error_name):
    run_input_validation(array_filter_process_code, "array_filter", example_input, raises_exception, error_name)
