import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def all_process_code():
    return load_process_code("all")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [False, None]}, False),
        ({"data": [True, None]}, True),
        ({"data": [False, None], "ignore_nodata": False}, False),
        ({"data": [True, None], "ignore_nodata": False}, None),
        ({"data": [True, False, True, False]}, False),
        ({"data": [True, False]}, False),
        ({"data": [True, True, True]}, True),
        ({"data": [True]}, True),
        ({"data": [None], "ignore_nodata": False}, None),
        ({"data": []}, None),
        ({"data": [True, 1 < 3, 3 < 1], "ignore_nodata": False}, False),
        ({"data": [True, 1 < 3, 3 < 1]}, False),
        ({"data": [True, None, True, 1 < 3, 2 * 2 < 10, True]}, True),
        ({"data": [True, None, True, 1 < 3, 2 * 2 < 10, True], "ignore_nodata": False}, None),
        ({"data": [True, None, True, 1 < 3, 2 * 2 < 10, True, False], "ignore_nodata": False}, False),
    ],
)
def test_all(all_process_code, example_input, expected_output):
    output = run_process(all_process_code, "all", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [True, True, True]}, False, None),
        ({"data": "['array']"}, True, "Argument `data` is not an array."),
        ({"data_array": [True, True]}, True, "Mandatory argument `data` is not defined."),
        ({}, True, "Mandatory argument `data` is not defined."),
        (
            {"data": [True, True, False, 1 < 3, "true"]},
            True,
            "Values in argument `data` can only be of type boolean or null.",
        ),
    ],
)
def test_all_exceptions(all_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(all_process_code, "all", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(all_process_code, "all", example_input)
