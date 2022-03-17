import json

import pytest

from tests.utils import load_process_code, run_input_validation


@pytest.fixture
def array_apply_process_code():
    return load_process_code("array_apply")


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        ({"process": {"process_graph": {"add_pg": {"process_id": "add", "arguments": {"x": {"from_parameter": "x"}, "index": {"from_parameter": "index"}, "y": 10}}}}}, True, "MISSING_PARAMETER"),
        ({"data": None, "process": {"process_graph": {"add_pg": {"process_id": "add", "arguments": {"x": {"from_parameter": "x"}, "index": {"from_parameter": "index"}, "y": 10}}}}}, True, "NOT_NULL"),
        ({"data": [1,2,3,4,5]}, True, "MISSING_PARAMETER"),
        ({"data": [1,2,3,4,5], "process": None}, True, "NOT_NULL"),
        ({"data": "[1,2,3,4,5]", "process": {"process_graph": {"add_pg": {"process_id": "add", "arguments": {"x": {"from_parameter": "x"}, "index": {"from_parameter": "index"}, "y": 10}}}}}, True, "NOT_ARRAY"),
    ],
)
def test_array_apply_inputs(array_apply_process_code, example_input, raises_exception, error_name):
    run_input_validation(array_apply_process_code, "array_apply", example_input, raises_exception, error_name)