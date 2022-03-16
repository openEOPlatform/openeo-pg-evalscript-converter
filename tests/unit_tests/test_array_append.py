import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def array_append_process_code():
    return load_process_code("array_append")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [], "value": None}, [None]),
        ({"data": [1, 2], "value": 3}, [1, 2, 3]),
        ({"data": ["a"], "value": "b"}, ["a", "b"]),
        (
            {"data": [True], "value": "2020-01-01T00:00:00Z"},
            [True, "2020-01-01T00:00:00Z"],
        ),
    ],
)
def test_array_append(array_append_process_code, example_input, expected_output):
    output = run_process(array_append_process_code, "array_append", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        ({"data": [1, 2], "value": [3]}, False, None),
        ({"value": 1}, True, "MISSING_PARAMETER"),
        ({"data": [1]}, True, "MISSING_PARAMETER"),
        ({"data": None, "value": 1}, True, "NOT_NULL"),
        ({"data": "[0]", "value": 1}, True, "NOT_ARRAY"),
    ],
)
def test_array_append_exceptions(array_append_process_code, example_input, raises_exception, error_name):
    run_input_validation(array_append_process_code, "array_append", example_input, raises_exception, error_name)
