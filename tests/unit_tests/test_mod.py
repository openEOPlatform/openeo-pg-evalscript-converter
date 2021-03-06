import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def mod_process_code():
    return load_process_code("mod")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 27, "y": 5}, 2),
        ({"x": -27, "y": 5}, 2),
        ({"x": 3.14, "y": -2}, -1.14),
        ({"x": -27, "y": -5}, -2),
        ({"x": -3, "y": -1}, -0),
        ({"x": 3, "y": -2}, -1),
        ({"x": 3, "y": 4}, 3),
        ({"x": None, "y": 3}, None),
        ({"x": 1, "y": None}, None),
        ({"x": None, "y": None}, None),
    ],
)
def test_mod(mod_process_code, example_input, expected_output):
    output = run_process(mod_process_code, "mod", example_input)
    output = json.loads(output)
    assert pytest.approx(output) == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 1, "y": 2}, False, None),
        ({"x": 2, "y": 0}, True, "Division by zero is not supported."),
        ({"x": 1}, True, "MISSING_PARAMETER"),
        ({"y": 1}, True, "MISSING_PARAMETER"),
        ({"x": "1", "y": 2}, True, "WRONG_TYPE"),
        ({"x": 1, "y": {"name": "John", "surname": "Doe"}}, True, "WRONG_TYPE"),
    ],
)
def test_input_validation(mod_process_code, example_input, raises_exception, error_message):
    run_input_validation(mod_process_code, "mod", example_input, raises_exception, error_message)
