import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def order_process_code():
    return load_process_code("order")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [1, 2, 3]}, [0, 1, 2]),
        ({"data": [1, 4, 3]}, [0, 2, 1]),
        ({"data": [6, -1, 2, 7, 4, 8, 3, 9, 9]}, [1, 2, 6, 4, 0, 3, 5, 7, 8]),
        ({"data": [6, -1, 2, 7, 4, 8, 3, 9, 9], "asc": False}, [7, 8, 5, 3, 0, 4, 6, 2, 1]),
        ({"data": [6, -1, 2, None, 7, 4, None, 8, 3, 9, 9]}, [1, 2, 8, 5, 0, 4, 7, 9, 10]),
        ({"data": [6, -1, 2, None, 7, 4, None, 8, 3, 9, 9], "nodata": True}, [1, 2, 8, 5, 0, 4, 7, 9, 10, 3, 6]),
        ({"data": [6, -1, 2, None, 7, 4, None, 8, 3, 9, 9], "asc": False, "nodata": True}, [9, 10, 7, 4, 0, 5, 8, 2, 1, 3, 6]),
        ({"data": [6, -1, 2, None, 7, 4, None, 8, 3, 9, 9], "asc": False, "nodata": False}, [3, 6, 9, 10, 7, 4, 0, 5, 8, 2, 1]),
    ],
)
def test_order(order_process_code, example_input, expected_output):
    output = run_process(order_process_code, "order", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [1, 2, 3]}, False, None),
        ({"asc": False}, True, "Mandatory argument `data` is either null or not defined."),
        ({"data": False}, True, "Argument `data` is not an array."),
        ({"data": [1, 2, 3], "asc": True}, False, None),
        ({"data": [1, 2, 3], "asc": None}, True, "Argument `asc` is not a boolean."),
        ({"data": [1, 2, 3], "nodata": False}, False, None),
        ({"data": [1, 2, 3], "nodata": None}, False, None),
        ({"data": [1, 2, 3], "nodata": []}, True, "Argument `asc` is not a boolean or null."),
    ],
)
def test_order_exceptions(
    order_process_code, example_input, raises_exception, error_message
):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(order_process_code, "order", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(order_process_code, "order", example_input)
