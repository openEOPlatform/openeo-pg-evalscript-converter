import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def array_create_process_code():
    return load_process_code("array_create")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({}, []),
        ({"data": ["this", "is", "a", "test"]}, ["this", "is", "a", "test"]),
        ({"data": [None], "repeat": 3}, [None, None, None]),
        ({"data": [1, 2, 3], "repeat": 2}, [1, 2, 3, 1, 2, 3]),
        (
            {"data": [True, False, None], "repeat": 4},
            [
                True,
                False,
                None,
                True,
                False,
                None,
                True,
                False,
                None,
                True,
                False,
                None,
            ],
        ),
        (
            {"data": [[1, 2, 3], [4, 5, 6]], "repeat": 3},
            [[1, 2, 3], [4, 5, 6], [1, 2, 3], [4, 5, 6], [1, 2, 3], [4, 5, 6]],
        ),
        (
            {"data": [{"name": "John", "surname": "Doe", "age": 23}], "repeat": 5},
            [
                {"name": "John", "surname": "Doe", "age": 23},
                {"name": "John", "surname": "Doe", "age": 23},
                {"name": "John", "surname": "Doe", "age": 23},
                {"name": "John", "surname": "Doe", "age": 23},
                {"name": "John", "surname": "Doe", "age": 23},
            ],
        ),
    ],
)
def test_array_create(array_create_process_code, example_input, expected_output):
    output = run_process(array_create_process_code, "array_create", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        ({"data": [1, 2, 3], "repeat": 2}, False, None),
        ({"data": {"1": 2, "3": 4}, "repeat": 1}, True, "NOT_ARRAY"),
        ({"data": [1, 2, 3], "repeat": "2"}, True, "NOT_INTEGER"),
        (
            {"data": [1, 2, 3], "repeat": -1},
            True,
            "MIN_VALUE",
        ),
    ],
)
def test_array_create_exceptions(array_create_process_code, example_input, raises_exception, error_name):
    run_input_validation(array_create_process_code, "array_create", example_input, raises_exception, error_name)
