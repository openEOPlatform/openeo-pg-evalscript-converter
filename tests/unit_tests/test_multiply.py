import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def divide_process_code():
    return load_process_code("multiply")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 5, "y": 2.5}, 12.5),
        ({"x": -2, "y": -4}, 8),
        ({"x": 1, "y": None}, None),
        ({"x": None, "y": 3}, None),
        ({"x": None, "y": None}, None),
        ({"x": 0, "y": 1}, 0),
        ({"x": 0, "y": 0}, 0),
        ({"x": 1, "y": 1}, 1),
        ({"x": 1, "y": 4}, 4),
    ],
)
def test_multiply(divide_process_code, example_input, expected_output):
    output = run_process(divide_process_code, "multiply", example_input)
    output = json.loads(output)
    assert pytest.approx(output) == expected_output
