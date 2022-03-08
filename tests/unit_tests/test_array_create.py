import json

import pytest

from tests.utils import load_process_code, run_process


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
    "example_input,raises_exception,error_message",
    [
        ({"data": [1, 2, 3], "repeat": 2}, False, None),
        ({"data": {"1": 2, "3": 4}, "repeat": 1}, True, "Argument `data` is not an array."),
        ({"data": [1, 2, 3], "repeat": "2"}, True, "Argument `repeat` is not an integer."),
        ({"data": [1, 2, 3], "repeat": -1}, True, "Argument `repeat` must contain only values greater than or equal to 1."),
    ],
)
def test_array_create_exceptions(array_create_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(array_create_process_code, "array_create", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(array_create_process_code, "array_create", example_input)
