import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def array_concat_process_code():
    return load_process_code("array_concat")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"array1": [], "array2": []}, []),
        ({"array1": [1, 2, 3], "array2": []}, [1, 2, 3]),
        ({"array1": [], "array2": [4, 5, 6]}, [4, 5, 6]),
        ({"array1": [1, 2, 3], "array2": [4, 5, 6]}, [1, 2, 3, 4, 5, 6]),
        ({"array1": [1, 2, 3], "array2": ["a", "b", "c"]}, [1, 2, 3, "a", "b", "c"]),
        (
            {"array1": [1, True, None], "array2": [False, {"name": "John", "surname": "Doe"}, ["one", "two", "three"]]},
            [1, True, None, False, {"name": "John", "surname": "Doe"}, ["one", "two", "three"]],
        ),
    ],
)
def test_array_concat(array_concat_process_code, example_input, expected_output):
    output = run_process(array_concat_process_code, "array_concat", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        ({"array1": [1, 2, 3], "array2": [4, 5, 6]}, False, None),
        ({"array2": [1, 2, 3]}, True, "MISSING_PARAMETER"),
        ({"array1": None, "array2": [1, 2, 3]}, True, "NOT_NULL"),
        ({"array1": [1, 2, 3]}, True, "MISSING_PARAMETER"),
        ({"array1": [1, 2, 3], "array2": None}, True, "NOT_NULL"),
        ({"array1": [1, 2, 3], "array2": "[4,5,6]"}, True, "NOT_ARRAY"),
        ({"array1": "[1,2,3]", "array2": [4, 5, 6]}, True, "NOT_ARRAY"),
    ],
)
def test_array_concat_exceptions(array_concat_process_code, example_input, raises_exception, error_name):
    run_input_validation(array_concat_process_code, "array_concat", example_input, raises_exception, error_name)
