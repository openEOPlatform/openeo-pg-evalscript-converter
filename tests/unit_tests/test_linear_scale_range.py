import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def linear_scale_range_process_code():
    return load_process_code("linear_scale_range")


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({}, True, "MISSING_PARAMETER"),
        ({"x": None}, False, None),
        ({"x": 0.3, "inputMin": 0, "inputMax": 1}, False, None),
        ({"x": 0.3}, True, "MISSING_PARAMETER"),
        ({"x": 0.3, "inputMax": 1}, True, "MISSING_PARAMETER"),
        ({"x": 0.3, "inputMin": 0}, True, "MISSING_PARAMETER"),
        ({"x": 0.3, "inputMin": None, "inputMax": 1}, True, "NOT_NULL"),
        ({"x": 0.3, "inputMin": 1, "inputMax": None}, True, "NOT_NULL"),
    ],
)
def test_linear_scale_range_inputs(linear_scale_range_process_code, example_input, raises_exception, error_message):
    run_input_validation(
        linear_scale_range_process_code, "linear_scale_range", example_input, raises_exception, error_message
    )


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0.3, "inputMin": -1, "inputMax": 1, "outputMin": 0, "outputMax": 255}, 165.75),
        ({"x": 25.5, "inputMin": 0, "inputMax": 255}, 0.1),
        ({"x": None, "inputMin": 0, "inputMax": 100}, None),
        ({"x": 1.12, "inputMin": 0, "inputMax": 1, "outputMin": 0, "outputMax": 255}, 255),
    ],
)
def test_linear_scale_range(linear_scale_range_process_code, example_input, expected_output):
    output = run_process(linear_scale_range_process_code, "linear_scale_range", example_input)
    output = json.loads(output)
    assert output == expected_output
