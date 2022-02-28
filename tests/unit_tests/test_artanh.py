import json
import math

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def artanh_process_code():
    return load_process_code("artanh")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 0),
        ({"x": 0.5}, 0.549306144334055),
        (
            {"x": 1},
            None,
        ),  # JS returns Infinity, but Python doesn't recognize JS's Infinity
        ({"x": 2}, None),  # JS returns NaN, but Python doesn't recognize JS's NaN
        ({"x": None}, None),
    ],
)
def test_artanh(artanh_process_code, example_input, expected_output):
    output = run_process(artanh_process_code, "artanh", example_input)
    output = json.loads(output)
    assert expected_output == pytest.approx(output)


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 0}, False, None),
        ({}, True, "Mandatory argument `x` is not defined."),
        ({"y": 0.5}, True, "Mandatory argument `x` is not defined."),
        ({"x": "0.5"}, True, "Argument `x` is not a number."),
    ],
)
def test_artanh_exceptions(
    artanh_process_code, example_input, raises_exception, error_message
):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(artanh_process_code, "artanh", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(artanh_process_code, "artanh", example_input)
