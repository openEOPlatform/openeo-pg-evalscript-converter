import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def add_process_code():
    return load_process_code("add")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({'x': 1,  'y': 2}, 3),
        ({'x': None,  'y': 3}, None),
        ({'x': 1,  'y': None}, None),
        ({'x': -2,  'y': 26}, 24),
        ({'x': -3,  'y': -8}, -11),
        ({'x': 0,  'y': -6}, -6),
        ({'x': -23,  'y': 0}, -23),
        ({'x': 0,  'y': 0}, 0),
        ({'x': 2.3,  'y': -1.6}, 0.7),
        ({'x': -23.84,  'y': -4.21}, -28.05)
    ],
)
def test_add(add_process_code, example_input, expected_output):
    output = run_process(add_process_code, "add", example_input)
    output = json.loads(output)
    assert pytest.approx(output) == expected_output
