import json

import pytest

from tests.utils import load_process_code, run_process


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
        ({}, True, "Mandatory argument `x` is not defined."),
        ({"x": True}, True, "Mandatory argument `y` is not defined."),
        ({"y": True}, True, "Mandatory argument `x` is not defined."),
        ({"x": "True", "y": "True"}, True, "Argument `x` is not a boolean."),
        ({"x": "True", "y": True}, True, "Argument `x` is not a boolean."),
        ({"x": True, "y": "True"}, True, "Argument `y` is not a boolean."),
    ],
)
def test_or_exceptions(or_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(or_process_code, "or", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(or_process_code, "or", example_input)
