import json

import pytest

from tests.utils import load_process_code, run_process


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
def test_and_exceptions(and_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(and_process_code, "and", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(and_process_code, "and", example_input)
