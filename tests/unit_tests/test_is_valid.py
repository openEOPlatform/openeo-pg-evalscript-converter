import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def is_valid_code():
    return load_process_code("is_valid")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 1}, True),
        ({"x": "Test"}, True),
        ({"x": None}, False),
        ({"x": float("nan")}, False),
        ({"x": float("inf")}, False),
        ({"x": [None, None]}, True),
        ({"x": {}}, True),
    ],
)
def test_is_valid(is_valid_code, example_input, expected_output):
    output = run_process(is_valid_code, "is_valid", example_input)
    output = json.loads(output)
    assert output == expected_output
