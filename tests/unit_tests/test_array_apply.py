import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def array_apply_process_code():
    return load_process_code("array_apply")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        (
            {
                "data": [],
                "process": {
                    "process_graph": {
                        "add_pg": {"process_id": "add", "arguments": {"x": {"from_parameter": "x"}, "y": 10}}
                    }
                },
            },
            [],
        ),
        (
            {
                "data": [1, 2, 3, 4, 5],
                "process": {
                    "process_graph": {
                        "add_pg": {"process_id": "add", "arguments": {"x": {"from_parameter": "x"}, "y": 10}}
                    }
                },
            },
            [11, 12, 13, 14, 15],
        ),
        (
            {
                "data": [-1, 0, 1, 100],
                "process": {
                    "process_graph": {
                        "add_pg": {"process_id": "add", "arguments": {"x": {"from_parameter": "x"}, "y": 10}}
                    }
                },
            },
            [9, 10, 11, 110],
        ),
        (
            {
                "data": [1, 10, 2, 24, 23, -12],
                "process": {
                    "process_graph": {
                        "add_pg": {"process_id": "add", "arguments": {"x": {"from_parameter": "x"}, "y": 10}}
                    }
                },
            },
            [11, 20, 12, 34, 33, -2],
        ),
    ],
)
def test_array_apply(array_apply_process_code, example_input, expected_output):
    pg_js_code = f"const process = ({{x}}) => x + 10;"
    output = run_process(array_apply_process_code + pg_js_code, "array_apply", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        (
            {
                "process": {
                    "process_graph": {
                        "add_pg": {
                            "process_id": "add",
                            "arguments": {"x": {"from_parameter": "x"}, "index": {"from_parameter": "index"}, "y": 10},
                        }
                    }
                }
            },
            True,
            "MISSING_PARAMETER",
        ),
        (
            {
                "data": None,
                "process": {
                    "process_graph": {
                        "add_pg": {
                            "process_id": "add",
                            "arguments": {"x": {"from_parameter": "x"}, "index": {"from_parameter": "index"}, "y": 10},
                        }
                    }
                },
            },
            True,
            "NOT_NULL",
        ),
        ({"data": [1, 2, 3, 4, 5]}, True, "MISSING_PARAMETER"),
        ({"data": [1, 2, 3, 4, 5], "process": None}, True, "NOT_NULL"),
        (
            {
                "data": "[1,2,3,4,5]",
                "process": {
                    "process_graph": {
                        "add_pg": {
                            "process_id": "add",
                            "arguments": {"x": {"from_parameter": "x"}, "index": {"from_parameter": "index"}, "y": 10},
                        }
                    }
                },
            },
            True,
            "NOT_ARRAY",
        ),
    ],
)
def test_array_apply_inputs(array_apply_process_code, example_input, raises_exception, error_name):
    run_input_validation(array_apply_process_code, "array_apply", example_input, raises_exception, error_name)
