import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def is_nan_code():
    return load_process_code("is_nan")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 1}, False),
        ({"x": "Test"}, True),
        ({"x": None}, True),
        ({"x": float("nan")}, True),
    ],
)
def test_is_nan(is_nan_code, example_input, expected_output):
    output = run_process(is_nan_code, "is_nan", example_input)
    output = json.loads(output)
    assert output == expected_output
