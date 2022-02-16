import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def is_nodata_code():
    return load_process_code("is_nodata")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 1}, False),
        ({"x": "Test"}, False),
        ({"x": None}, True),
        ({"x": float("nan")}, False),
        ({"x": [None, None]}, False),
        ({"x": {}}, False),
    ],
)
def test_is_nodata(is_nodata_code, example_input, expected_output):
    output = run_process(is_nodata_code, "is_nodata", example_input)
    output = json.loads(output)
    assert output == expected_output
