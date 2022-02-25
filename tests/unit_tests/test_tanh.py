import json
import math

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def tanh_process_code():
    return load_process_code("tanh")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 0),
        ({"x": 1}, 0.7615941559557649),
        ({"x": -1}, -0.7615941559557649),
        ({"x": math.inf}, 1),
        ({"x": None}, None),
    ],
)
def test_tanh(tanh_process_code, example_input, expected_output):
    output = run_process(tanh_process_code, "tanh", example_input)
    output = json.loads(output)
    assert pytest.approx(output) == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 0}, False, None),
        ({}, True, "Mandatory argument `x` is not defined."),
        ({"y": 0.5}, True, "Mandatory argument `x` is not defined."),
        ({"x": "0.5"}, True, "Argument `x` is not a number."),
    ],
)
def test_tanh_exceptions(
    tanh_process_code, example_input, raises_exception, error_message
):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(tanh_process_code, "tanh", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(tanh_process_code, "tanh", example_input)
