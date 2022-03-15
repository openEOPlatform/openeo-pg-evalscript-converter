import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def array_filter_process_code():
    return load_process_code("array_filter")


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 1}, True, "Mandatory argument `data` is not defined."),
        ({"data": 1}, True, "Argument `data` is not an array."),
        ({"data": [1, 2]}, True, "Mandatory argument `condition` is not defined."),
    ],
)
def test_array_filter_exceptions(array_filter_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(array_filter_process_code, "array_filter", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(array_filter_process_code, "array_filter", example_input)
