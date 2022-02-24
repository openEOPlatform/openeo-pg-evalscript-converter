import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def median_process_code():
    return load_process_code("median")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [1, 3, 3, 6, 7, 8, 9]}, 6),
        ({"data": [1, 2, 3, 4, 5, 6, 8, 9]}, 4.5),
        ({"data": [-1, -0.5, None, 1]}, -0.5),
        ({"data": [-1, 0, None, 1], "ignore_nodata": False}, None),
        ({"data": []}, None),
        ({"data": [], "ignore_nodata": False}, None),
        ({"data": [None, None, None, None]}, None),
        ({"data": [None, None, None, None], "ignore_nodata": False}, None),
    ],
)
def test_median(median_process_code, example_input, expected_output):
    output = run_process(median_process_code, "median", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [1, 0, 3, 2]}, False, None),
        ({"data_fake": [1, 0, 3, 2]}, True, "Mandatory argument `data` is not defined."),
        ({"data": "[1,0,3,2]"}, True, "Argument `data` is not an array."),
        ({"data": [1, 0, 3, 2], "ignore_nodata": [1, 2, 3]}, True, "Argument `ignore_nodata` is not a boolean."),
        ({"data": [1, 2, 3, None, "1"]}, True, "Value in argument `data` is not a number or null."),
    ],
)
def test_median_exceptions(median_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(median_process_code, "median", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(median_process_code, "median", example_input)
