import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def floor_process_code():
    return load_process_code("floor")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 0),
        ({"x": 3.5}, 3),
        ({"x": 0.4}, 0),
        ({"x": -0.4}, -1),
        ({"x": -3.5}, -4),
        ({"x": 0.00001}, 0),
        ({"x": -0.00001}, -1),
        ({"x": 0.99999}, 0),
        ({"x": -0.99999}, -1),
    ],
)
def test_floor(floor_process_code, example_input, expected_output):
    output = run_process(floor_process_code, "floor", example_input)
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
def test_floor_exceptions(floor_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(floor_process_code, "floor", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(floor_process_code, "floor", example_input)
