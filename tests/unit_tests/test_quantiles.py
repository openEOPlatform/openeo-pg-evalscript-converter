import json

import pytest

from tests.utils import load_process_code, run_process


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
        ({"q": 2}, True, "Mandatory argument `data` is either null or not defined"),
        (
            {"data": None, "q": 2},
            True,
            "Mandatory argument `data` is either null or not defined",
        ),
        ({"data": "1", "q": 2}, True, "Argument `data` is not an array."),
        (
            {"data": [1, 2], "q": 2, "ignore_nodata": 1},
            True,
            "Argument `ignore_nodata` is not a boolean.",
        ),
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
        ({"data": [1, 2], "q": "1"}, True, "Argument `q` is not an integer."),
        (
            {"data": [1, 2], "probabilities": "1"},
            True,
            "Argument `probabilities` is not an array.",
        ),
        (
            {"data": [1, 2], "probabilities": ["1"]},
            True,
            "Element in argument `probabilities` is not a number.",
        ),
        (
            {"data": [1, 2], "probabilities": [-1, 5]},
            True,
            "Elements in argument `probabilities` must be between 0 and 1 (both inclusive).",
        ),
    ],
)
def test_quantiles_exceptions(
    quantiles_process_code, example_input, raises_exception, error_message
):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(quantiles_process_code, "quantiles", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(quantiles_process_code, "quantiles", example_input)
