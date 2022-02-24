import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def sqrt_process_code():
    return load_process_code("sqrt")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 0),
        ({"x": 1}, 1),
        ({"x": 9}, 3),
        ({"x": 144}, 12),
        ({"x": 0.81}, 0.9),
        ({"x": None}, None),
    ],
)
def test_sqrt(sqrt_process_code, example_input, expected_output):
    output = run_process(sqrt_process_code, "sqrt", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 1}, False, None),
        ({}, True, "Mandatory argument `x` is not defined."),
        ({"y": 0.5}, True, "Mandatory argument `x` is not defined."),
        ({"x": "0.5"}, True, "Argument `x` is not a number."),
        ({"x": -4}, True, "Argument `x` is not a non-negative number."),
    ],
)
def test_sqrt_exceptions(sqrt_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(sqrt_process_code, "sqrt", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(sqrt_process_code, "sqrt", example_input)
