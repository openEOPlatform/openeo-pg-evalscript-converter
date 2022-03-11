import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def and_process_code():
    return load_process_code("and")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": True, "y": True}, True),
        ({"x": True, "y": False}, False),
        ({"x": False, "y": True}, False),
        ({"x": False, "y": False}, False),
        ({"x": False, "y": None}, False),
        ({"x": None, "y": False}, False),
        ({"x": True, "y": None}, None),
        ({"x": None, "y": True}, None),
        ({"x": None, "y": None}, None),
    ],
)
def test_and(and_process_code, example_input, expected_output):
    output = run_process(and_process_code, "and", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        ({"x": True, "y": True}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"x": True}, True, "MISSING_PARAMETER"),
        ({"y": True}, True, "MISSING_PARAMETER"),
        ({"x": "True", "y": "True"}, True, "NOT_BOOLEAN"),
        ({"x": "True", "y": True}, True, "NOT_BOOLEAN"),
        ({"x": True, "y": "True"}, True, "NOT_BOOLEAN"),
    ],
)
def test_and_exceptions(and_process_code, example_input, raises_exception, error_name):
    run_input_validation(and_process_code, "and", example_input, raises_exception, error_name)
