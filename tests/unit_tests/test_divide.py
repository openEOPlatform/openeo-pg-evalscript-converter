import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def divide_process_code():
    return load_process_code("divide")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({'x': 1, 'y': 2}, 0.5),
        ({'x': None, 'y': 3}, None),
        ({'x': 1, 'y': None}, None),
        ({'x': 0, 'y':1}, 0),
        ({'x': -1, 'y':8}, -0.125),
        ({'x': 23, 'y':-26}, -0.88461538461),
        ({'x': -3, 'y':-11}, 0.27272727272),
        ({'x': 2, 'y': 0}, 'Division by zero is not supported.')
    ],
)
def test_divide(divide_process_code, example_input, expected_output):
    output = run_process(divide_process_code, "_divide", example_input)
    output = json.loads(output)
    assert pytest.approx(output) == expected_output
