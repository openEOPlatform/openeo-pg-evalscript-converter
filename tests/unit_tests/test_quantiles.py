import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def quantiles_process_code():
    return load_process_code("quantiles")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        (
            {
                "data": [2, 4, 4, 4, 5, 5, 7, 9],
                "probabilities": [0.005, 0.01, 0.02, 0.05, 0.1, 0.5],
            },
            [2.07, 2.14, 2.28, 2.7, 3.4, 4.5],
        ),
        ({"data": [2, 4, 4, 4, 5, 5, 7, 9], "q": 4}, [4, 4.5, 5.5]),
        ({"data": [-1, -0.5, None, 1], "q": 2}, [-0.5]),
        (
            {"data": [-1, -0.5, None, 1], "q": 4, "ignore_nodata": False},
            [None, None, None],
        ),
        ({"data": [], "probabilities": [0.1, 0.5]}, [None, None]),
        ({"data": [None, None, None], "probabilities": [0.1, 0.5]}, [None, None]),
    ],
)
def test_quantiles(quantiles_process_code, example_input, expected_output):
    output = run_process(quantiles_process_code, "quantiles", example_input)
    output = json.loads(output)
    assert pytest.approx(output) == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [1, 2, 3, 4], "q": 2}, False, None),
        ({"q": 2}, True, "MISSING_PARAMETER"),
        ({"data": None, "q": 2}, True, "NOT_NULL"),
        ({"data": "1", "q": 2}, True, "NOT_ARRAY"),
        ({"data": [1, 2], "q": 2, "ignore_nodata": 1}, True, "WRONG_TYPE"),
        ({"data": [1, 2], "q": 2, "ignore_nodata": None}, True, "NOT_NULL"),
        (
            {"data": [1, 2]},
            True,
            "The process `quantiles` requires either the `probabilities` or `q` parameter to be set.",
        ),
        (
            {"data": [1, 2], "q": 2, "probabilities": [1]},
            True,
            "The process `quantiles` only allows that either the `probabilities` or the `q` parameter is set.",
        ),
        ({"data": [1, 2], "q": "1"}, True, "NOT_INTEGER"),
        ({"data": [1, 2], "q": 1}, True, "MIN_VALUE"),
        ({"data": [1, 2], "probabilities": "1"}, True, "NOT_ARRAY"),
        ({"data": [1, 2], "probabilities": ["1"]}, True, "WRONG_TYPE"),
        ({"data": [1, 2], "probabilities": [-1, 5]}, True, "MIN_VALUE"),
        ({"data": [1, 2], "probabilities": [1, 5]}, True, "MAX_VALUE"),
        ({"data": [1, 2], "probabilities": [1, 0]}, False, None),
    ],
)
def test_quantiles_exceptions(quantiles_process_code, example_input, raises_exception, error_message):
    run_input_validation(quantiles_process_code, "quantiles", example_input, raises_exception, error_message)
