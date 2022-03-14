import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def xor_process_code():
    return load_process_code("xor")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": True, "y": True}, False),
        ({"x": True, "y": False}, True),
        ({"x": False, "y": True}, True),
        ({"x": False, "y": False}, False),
        ({"x": False, "y": None}, None),
        ({"x": None, "y": False}, None),
        ({"x": True, "y": None}, None),
        ({"x": None, "y": True}, None),
        ({"x": None, "y": None}, None),
    ],
)
def test_xor(xor_process_code, example_input, expected_output):
    output = run_process(xor_process_code, "xor", example_input)
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
def test_xor_exceptions(xor_process_code, example_input, raises_exception, error_message):
    run_input_validation(xor_process_code, "xor", example_input, raises_exception, error_message)
