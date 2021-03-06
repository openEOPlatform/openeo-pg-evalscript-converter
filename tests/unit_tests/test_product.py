import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def product_process_code():
    return load_process_code("product")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [1, 0, 3, 2]}, 0),
        ({"data": [5, 2.5, None, -0.7]}, -8.75),
        ({"data": [1, 0, 3, None, 2], "ignore_nodata": False}, None),
        ({"data": [1, 2, 3, 4, 5, 6, 7, 8, None]}, 40320),
        ({"data": [1, 2, 3, 4, 5, 6, 7, 8, None], "ignore_nodata": False}, None),
        ({"data": [-1, -2, -3, -4, -5, -6, None]}, 720),
        ({"data": [-1, -2, -3, -4, -5, -6, None], "ignore_nodata": False}, None),
        ({"data": []}, None),
        ({"data": [None], "ignore_nodata": False}, None),
        ({"data": [-1]}, -1),
        ({"data": [1, None]}, 1),
        ({"data": [-2, 4, 2.5]}, -20),
        ({"data": [5, 0]}, 0),
    ],
)
def test_product(product_process_code, example_input, expected_output):
    output = run_process(product_process_code, "product", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [1, 0, 3, 2]}, False, None),
        ({"data_fake": [1, 0, 3, 2]}, True, "MISSING_PARAMETER"),
        ({"data": "[1,0,3,2]"}, True, "NOT_ARRAY"),
        ({"data": [1, 0, 3, 2], "ignore_nodata": [1, 2, 3]}, True, "WRONG_TYPE"),
        ({"data": [1, 0, 3, 2], "ignore_nodata": None}, True, "NOT_NULL"),
        ({"data": [1, 2, 3, None, "1"]}, True, "WRONG_TYPE"),
    ],
)
def test_product_exceptions(product_process_code, example_input, raises_exception, error_message):
    run_input_validation(product_process_code, "product", example_input, raises_exception, error_message)
