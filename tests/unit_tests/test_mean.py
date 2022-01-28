import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def mean_process_code():
    return load_process_code("mean")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [([1, 3, 5, 7], 4), ([6, 6], 6), ([1, 0, 3, 2], 1.5)],
)
def test_mean(mean_process_code, example_input, expected_output):
    output = run_process(mean_process_code, "mean", {"data": example_input})
    output = json.loads(output)
    assert output == expected_output
