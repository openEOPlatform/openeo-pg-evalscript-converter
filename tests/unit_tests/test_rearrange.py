import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def rearrange_process_code():
    return load_process_code("rearrange")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [], "order": []}, []),
        ({"data": [None, None, None], "order": [0, 1, 2]}, [None, None, None]),
        ({"data": [1, None, None], "order": [1, 0]}, [None, 1]),
        ({"data": [5, 4, 3], "order": [2, 1, 0]}, [3, 4, 5]),
        ({"data": [5, 4, 3, 2], "order": [1, 3]}, [4, 2]),
        ({"data": [5, 4, 3, 2], "order": [0, 2, 1, 3]}, [5, 3, 4, 2]),
        (
            {"data": [False, "c", "b", "a", True], "order": [4, 3, 2, 1, 0]},
            [True, "a", "b", "c", False],
        ),
    ],
)
def test_rearrange(rearrange_process_code, example_input, expected_output):
    output = run_process(rearrange_process_code, "rearrange", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [1, 2], "order": [0, 1]}, False, None),
        ({"order": [0]}, True, "MISSING_PARAMETER"),
        ({"data": None, "order": [0, 1]}, True, "NOT_NULL"),
        ({"data": 1, "order": [0, 1]}, True, "NOT_ARRAY"),
        ({"data": [0]}, True, "MISSING_PARAMETER"),
        ({"data": [0], "order": None}, True, "NOT_NULL"),
        ({"data": [0], "order": 1}, True, "NOT_ARRAY"),
        ({"data": [1, 2], "order": [0, -1]}, True, "MIN_VALUE"),
        (
            {"data": [1], "order": [1]},
            True,
            "Argument `order` contains an index which does not exist in argument `data`.",
        ),
    ],
)
def test_rearrange_exceptions(rearrange_process_code, example_input, raises_exception, error_message):
    run_input_validation(rearrange_process_code, "rearrange", example_input, raises_exception, error_message)
