import json
import math

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def tan_process_code():
    return load_process_code("tan")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 0),  # tan(0°)
        ({"x": math.pi / 6}, math.sqrt(3) / 3),  # tan(30°)
        ({"x": math.pi / 4}, 1),  # tan(45°)
        ({"x": math.pi / 3}, math.sqrt(3)),  # tan(60°)
        ({"x": math.pi / 2}, 16331239353195370),  # tan(90°) = infinity
        ({"x": math.pi}, 0),  # tan(180°)
        ({"x": 3 * math.pi / 2}, 5443746451065123),  # tan(270°) = infinity
        ({"x": 2 * math.pi}, 0),  # tan(360°)
        ({"x": -math.pi / 2}, -16331239353195370),  # tan(-90°) = -infinity
        ({"x": None}, None),
    ],
)
def test_tan(tan_process_code, example_input, expected_output):
    output = run_process(tan_process_code, "tan", example_input)
    output = json.loads(output)
    assert pytest.approx(output) == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 0}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"y": 0.5}, True, "MISSING_PARAMETER"),
        ({"x": "0.5"}, True, "WRONG_TYPE"),
    ],
)
def test_tan_exceptions(tan_process_code, example_input, raises_exception, error_message):
    run_input_validation(tan_process_code, "tan", example_input, raises_exception, error_message)
