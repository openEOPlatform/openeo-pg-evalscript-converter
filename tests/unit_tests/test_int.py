import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def int_process_code():
    return load_process_code("int")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 0),
        ({"x": 3.5}, 3),
        ({"x": 0.4}, 0),
        ({"x": -0.4}, 0),
        ({"x": -3.5}, -3),
        ({"x": 0.00001}, 0),
        ({"x": -0.00001}, 0),
        ({"x": 0.99999}, 0),
        ({"x": -0.99999}, 0),
        ({'x': 2.4}, 2),
        ({'x': 13.0001}, 13),
        ({'x': 12.9999}, 12),
        ({'x': None}, None)
    ],
)
def test_int(int_process_code, example_input, expected_output):
    output = run_process(int_process_code, "int", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 1}, False, None),
        ({}, True, "Mandatory argument `x` is not defined."),
        ({"y": 0.5}, True, "Mandatory argument `x` is not defined."),
        ({"x": "0.5"}, True, "Argument `x` is not a number."),
    ],
)
def test_int_exceptions(int_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(int_process_code, "int", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(int_process_code, "int", example_input)
