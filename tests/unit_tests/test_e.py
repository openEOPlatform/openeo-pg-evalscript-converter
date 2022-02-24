import json
import math

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def e_process_code():
    return load_process_code("e")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({}, math.e),
    ],
)
def test_e(e_process_code, example_input, expected_output):
    output = run_process(e_process_code, "e", example_input)
    output = json.loads(output)
    assert output == expected_output
