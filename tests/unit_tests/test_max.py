import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def max_process_code():
    return load_process_code("max")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [1, 2]}, 2),
        ({"data": [1, 0, 3, 2]}, 3),
        ({"data": [5, 2.5, None, 4]}, 5),
        ({"data": [-1, -3, -2.5, None, -10]}, -1),
        ({"data": [-1, -3, -2.5, None, -10, 0]}, 0),
        ({"data": [-1, -3, -2.5, None, -10], "ignore_nodata": False}, None),
        ({"data": []}, None),
        ({"data": [], "ignore_nodata": False}, None),
        ({"data": [None]}, None),
        ({"data": [1.0001, 1.00001, 1, 1.0002], "ignore_nodata": False}, 1.0002),
    ],
)
def test_max(max_process_code, example_input, expected_output):
    output = run_process(max_process_code, "max", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [1, 2]}, False, None),
        ({}, True, "Mandatory argument `data` is not defined."),
        ({"data": 123}, True, "Argument `data` is not an array."),
        ({"data": [1, 2, 3], "ignore_nodata": "False"}, True, "Argument `ignore_nodata` is not a boolean."),
        ({"data": [1, 2, 3, 4, 5, True]}, True, "Element in argument `data` is not a number or null."),
    ],
)
def test_max_exceptions(max_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(max_process_code, "max", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(max_process_code, "max", example_input)
