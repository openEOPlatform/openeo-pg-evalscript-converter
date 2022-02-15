import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def subtract_process_code():
    return load_process_code("subtract")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 1, "y": 2}, -1),
        ({"x": None, "y": 3}, None),
        ({"x": 1, "y": None}, None),
        ({"x": -2, "y": 26}, -28),
        ({"x": -3, "y": -8}, 5),
        ({"x": 0, "y": -6}, 6),
        ({"x": -23, "y": 0}, -23),
        ({"x": 0, "y": 0}, 0),
        ({"x": 2.3, "y": -4.233}, 6.533),
        ({"x": -23.84, "y": -4.21}, -19.63),
    ],
)
def test_subtract(subtract_process_code, example_input, expected_output):
    output = run_process(subtract_process_code, "subtract", example_input)
    output = json.loads(output)
    assert pytest.approx(output) == expected_output
