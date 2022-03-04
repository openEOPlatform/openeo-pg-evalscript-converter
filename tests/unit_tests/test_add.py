import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def add_process_code():
    return load_process_code("add")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 1, "y": 2}, 3),
        ({"x": None, "y": 3}, None),
        ({"x": 1, "y": None}, None),
        ({"x": None, "y": None}, None),
        ({"x": -2, "y": 26}, 24),
        ({"x": -3, "y": -8}, -11),
        ({"x": 0, "y": -6}, -6),
        ({"x": -23, "y": 0}, -23),
        ({"x": 0, "y": 0}, 0),
        ({"x": 2.3, "y": -1.6}, 0.7),
        ({"x": -23.84, "y": -4.21}, -28.05),
    ],
)
def test_add(add_process_code, example_input, expected_output):
    output = run_process(add_process_code, "add", example_input)
    output = json.loads(output)
    assert pytest.approx(output) == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 1, "y": 2}, False, None),
        ({}, True, "Mandatory argument `x` is not defined."),
        ({"y": 2}, True, "Mandatory argument `x` is not defined."),
        ({"x": 1}, True, "Mandatory argument `y` is not defined."),
        ({"x": False, "y": 2}, True, "Argument `x` is not a number."),
        ({"x": 1, "y": False}, True, "Argument `y` is not a number."),
    ],
)
def test_add_exceptions(add_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(add_process_code, "add", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(add_process_code, "add", example_input)
