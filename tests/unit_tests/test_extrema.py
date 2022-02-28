import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def extrema_process_code():
    return load_process_code("extrema")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [1, 0, 3, 2]}, [0, 3]),
        ({"data": [5, 2.5, None, -0.7]}, [-0.7, 5]),
        ({"data": [1, 0, 3, None, 2], "ignore_nodata": False}, [None, None]),
        ({"data": [1, 2, 3, 4, 5, 6, 7, 8, None]}, [1, 8]),
        ({"data": [1, 2, 3, 4, 5, 6, 7, 8, None], "ignore_nodata": False}, [None, None]),
        ({"data": [-1, -2, -3, -4, -5, -6, None]}, [-6, -1]),
        ({"data": [-1, -2, -3, -4, -5, -6, None], "ignore_nodata": False}, [None, None]),
        ({"data": []}, [None, None]),
    ],
)
def test_extrema(extrema_process_code, example_input, expected_output):
    output = run_process(extrema_process_code, "extrema", example_input)
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
def test_extrema_exceptions(extrema_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(extrema_process_code, "extrema", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(extrema_process_code, "extrema", example_input)
