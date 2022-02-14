import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def absolute_process_code():
    return load_process_code("absolute")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 0),
        ({"x": 3.5}, 3.5),
        ({"x": -0.4}, 0.4),
        ({"x": -3.5}, 3.5),
        ({"x": None}, None),
    ],
)
def test_absolute(absolute_process_code, example_input, expected_output):
    output = run_process(absolute_process_code, "absolute", example_input)
    output = json.loads(output)
    assert output == expected_output
