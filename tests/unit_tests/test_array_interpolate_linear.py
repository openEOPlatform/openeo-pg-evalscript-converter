import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def array_interpolate_linear_process_code():
    return load_process_code("array_interpolate_linear")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [1, 2, 3]}, [1, 2, 3]),
        ({"data": [1, None, None, 4]}, [1, 2, 3, 4]),
        ({"data": [None, 1, None, 6, None, -8, None]}, [None, 1, 3.5, 6, -1, -8, None]),
        ({"data": [None, None, None]}, [None, None, None]),
        ({"data": [1, None, None]}, [1, None, None]),
        ({"data": [None, None, 1]}, [None, None, 1]),
        ({"data": [None, 1, None]}, [None, 1, None]),
        ({"data": []}, []),
    ],
)
def test_array_interpolate_linear(array_interpolate_linear_process_code, example_input, expected_output):
    output = run_process(array_interpolate_linear_process_code, "array_interpolate_linear", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        ({"data": [1, None, 3]}, False, None),
        (
            {"data": None},
            True,
            "NOT_NULL",
        ),
        ({}, True, "MISSING_PARAMETER"),
        ({"data": "[1]"}, True, "NOT_ARRAY"),
        ({"data": [1, 2, "3"]}, True, "WRONG_TYPE"),
    ],
)
def test_array_interpolate_linear_exceptions(
    array_interpolate_linear_process_code,
    example_input,
    raises_exception,
    error_name,
):
    run_input_validation(
        array_interpolate_linear_process_code, "array_interpolate_linear", example_input, raises_exception, error_name
    )
