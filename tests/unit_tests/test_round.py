import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def round_process_code():
    return load_process_code("round")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 0),
        ({"x": 3.5}, 4),
        ({"x": 0.4}, 0),
        ({"x": -0.4}, 0),
        ({"x": -3.5}, -4),
        ({"x": 0.00001}, 0),
        ({"x": -0.00001}, 0),
        ({"x": 0.99999}, 1),
        ({"x": -0.99999}, -1),
        ({"x": 1.5, "p": 0}, 2),
        ({"x": 3.2421, "p": 1}, 3.2),
        ({"x": 3.2421, "p": 3}, 3.242),
        ({"x": 3.2425, "p": 3}, 3.243),
        ({"x": 3.2435, "p": 3}, 3.244),
        ({"x": 1234, "p": -1}, 1230),
        ({"x": 12345, "p": -1}, 12350),
        ({"x": 12345, "p": -3}, 12000),
        ({"x": None, "p": 3}, None),
        ({"x": None}, None),
    ],
)
def test_round(round_process_code, example_input, expected_output):
    output = run_process(round_process_code, "round", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 1}, False, None),
        ({}, True, "Mandatory argument `x` is not defined."),
        ({"y": 0.5}, True, "Mandatory argument `x` is not defined."),
        ({"x": "0.5"}, True, "Argument `x` is not a number."),
        ({"x": 0.2, "p": "2"}, True, "Argument `p` is not a number."),
    ],
)
def test_round_exceptions(round_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(round_process_code, "round", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(round_process_code, "round", example_input)
