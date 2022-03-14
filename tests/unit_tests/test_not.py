import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def not_process_code():
    return load_process_code("not")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [({"x": None}, None), ({"x": True}, False), ({"x": False}, True)],
)
def test_not(not_process_code, example_input, expected_output):
    output = run_process(not_process_code, "not", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": True}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"y": True}, True, "MISSING_PARAMETER"),
        ({"x": "True"}, True, "WRONG_TYPE"),
    ],
)
def test_not_exceptions(not_process_code, example_input, raises_exception, error_message):
    run_input_validation(not_process_code, "not", example_input, raises_exception, error_message)
