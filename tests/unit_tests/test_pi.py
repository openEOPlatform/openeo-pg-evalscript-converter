import json
import math

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def pi_process_code():
    return load_process_code("pi")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({}, math.pi),
    ],
)
def test_pi(pi_process_code, example_input, expected_output):
    output = run_process(pi_process_code, "pi", example_input)
    output = json.loads(output)
    assert output == expected_output
