import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def or_process_code():
    return load_process_code("or")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": True, "y": True}, True),
        ({"x": True, "y": False}, True),
        ({"x": False, "y": True}, True),
        ({"x": False, "y": False}, False),
        ({"x": False, "y": None}, None),
        ({"x": None, "y": False}, None),
        ({"x": True, "y": None}, True),
        ({"x": None, "y": True}, True),
        ({"x": None, "y": None}, None),
    ],
)
def test_or(or_process_code, example_input, expected_output):
    output = run_process(or_process_code, "or", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": True, "y": True}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"x": True}, True, "MISSING_PARAMETER"),
        ({"y": True}, True, "MISSING_PARAMETER"),
        ({"x": "True", "y": "True"}, True, "WRONG_TYPE"),
        ({"x": "True", "y": True}, True, "WRONG_TYPE"),
        ({"x": True, "y": "True"}, True, "WRONG_TYPE"),
    ],
)
def test_or_exceptions(or_process_code, example_input, raises_exception, error_message):
    run_input_validation(or_process_code, "or", example_input, raises_exception, error_message)
