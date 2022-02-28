import json

import pytest

from tests.utils import load_process_code, run_process


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
        ({}, True, "Mandatory argument `x` is not defined."),
        ({"x": True}, True, "Mandatory argument `y` is not defined."),
        ({"y": True}, True, "Mandatory argument `x` is not defined."),
        ({"x": "True", "y": "True"}, True, "Argument `x` is not a boolean or null."),
        ({"x": "True", "y": True}, True, "Argument `x` is not a boolean or null."),
        ({"x": True, "y": "True"}, True, "Argument `y` is not a boolean or null."),
    ],
)
def test_xor_exceptions(xor_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(xor_process_code, "xor", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(xor_process_code, "xor", example_input)
