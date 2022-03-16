import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def array_filter_process_code():
    return load_process_code("array_filter")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [1, 2], "condition": "dummy"},  []),
        ({"data": [1, 2, 3, 4, 5], "condition": "dummy"},  [3, 4, 5]),
        ({"data": [4, 5], "condition": "dummy"},  [4, 5]),
    ],
)
def test_array_filter(array_filter_process_code, example_input, expected_output):
    condition_js_code = f"const condition = ({{ x }}) => x > 2;"
    output = run_process(array_filter_process_code + condition_js_code, "array_filter", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        ({}, True, "MISSING_PARAMETER"),
        ({"data": 1}, True, "NOT_ARRAY"),
        ({"data": [1, 2]}, True, "MISSING_PARAMETER"),
    ],
)
def test_array_filter_inputs(array_filter_process_code, example_input, raises_exception, error_name):
    run_input_validation(array_filter_process_code, "array_filter", example_input, raises_exception, error_name)
