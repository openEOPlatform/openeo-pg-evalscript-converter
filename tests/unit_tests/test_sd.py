import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def sd_process_code():
    return load_process_code("sd")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [-1, 1, 3, None]}, 2),
        ({"data": [-1, 1, 3, None], "ignore_nodata": False}, None),
        ({"data": []}, None),
        ({"data": [], "ignore_nodata": False}, None),
        ({"data": [0, 1, 1, 2, 2, 3, 4, 5, 6, 6]}, 2.1602469),
        ({"data": [0, 1, 1, None, 2, 2, 3, 4, 5, 6, 6]}, 2.1602469),
        ({"data": [0, 1, 1, 2, 2, 3, 4, 5, None, 6, 6], "ignore_nodata": False}, None),
        ({"data": [None]}, None),
        ({"data": [None, None, None]}, None),
        ({"data": [None, None, None], "ignore_nodata": False}, None),
    ],
)
def test_sd(sd_process_code, example_input, expected_output):
    output = run_process(sd_process_code, "sd", example_input)
    output = json.loads(output)
    assert pytest.approx(output) == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [-1, 1, 3, None]}, False, None),
        ({}, True, "Mandatory argument `data` is not defined."),
        ({"data": 2}, True, "Argument `data` is not an array."),
        ({"data": [1, 2, 3], "ignore_nodata": 12}, True, "Argument `ignore_nodata` is not a boolean."),
        ({"data": [1, 2, 3, 4, "5"]}, True, "Value in argument `data` is not a number or null."),
    ],
)
def test_sd_exceptions(sd_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(sd_process_code, "sd", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(sd_process_code, "sd", example_input)
