import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def mean_process_code():
    return load_process_code("mean")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [1, 3, 5, 7]}, 4),
        ({"data": [6, 6, 6]}, 6),
        ({"data": [1, 0, 3, 2]}, 1.5),
        ({"data": [1, 3, 5, 7], "ignore_nodata": False}, 4),
        ({"data": [0, 0, 0, 0, 0], "ignore_nodata": False}, 0),
        ({"data": [0, 0, 0, 0, 0]}, 0),
        ({"data": [1, None], "ignore_nodata": False}, None),
        ({"data": [1, None]}, 1),
        ({"data": [9, 2.5, None, -2.5]}, 3),
        ({"data": [9, 2.5, None, -2.5], "ignore_nodata": False}, None),
        ({"data": []}, None),
        ({"data": [], "ignore_nodata": False}, None),
        ({"data": [None]}, None),
        ({"data": [None], "ignore_nodata": False}, None),
        ({"data": [None, None, None]}, None),
        ({"data": [1, None, -3, -18, None, None, 27, 3]}, 2),
    ],
)
def test_mean(mean_process_code, example_input, expected_output):
    output = run_process(mean_process_code, "mean", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [1, 2]}, False, None),
        ({}, True, "Mandatory argument `data` is not defined."),
        ({"data": 123}, True, "Argument `data` is not an array."),
        ({"data": [1, 2, 3], "ignore_nodata": "False"}, True, "Argument `ignore_nodata` is not a boolean."),
        ({"data": [1, 2, 3, 4, 5, True]}, True, "Element in argument `data` is not a number or null."),
    ],
)
def test_mean_exceptions(mean_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(mean_process_code, "mean", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(mean_process_code, "mean", example_input)
