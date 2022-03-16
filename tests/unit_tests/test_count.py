import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def count_process_code():
    return load_process_code("count")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": []}, 0),
        ({"data": [False, None, 12, "string", {"name": "John"}], "condition": True}, 5),
    ],
)
def test_count(count_process_code, example_input, expected_output):
    output = run_process(count_process_code, "count", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        ({"data": [False, None, 12, "string", {"name": "John"}], "condition": True}, False, None),
        ({"data_fake": [1, 0, 3, 2]}, True, "MISSING_PARAMETER"),
        ({"data": "[1,0,3,2]"}, True, "NOT_ARRAY"),
        (
            {"data": [1, 0, 3, 2], "condition": [1, 2, 3]},
            True,
            "WRONG_TYPE",
        ),
        (
            {"data": [1, 0, 3, 2], "condition": 12},
            True,
            "WRONG_TYPE",
        ),
    ],
)
def test_count_exceptions(count_process_code, example_input, raises_exception, error_name):
    run_input_validation(count_process_code, "count", example_input, raises_exception, error_name)
