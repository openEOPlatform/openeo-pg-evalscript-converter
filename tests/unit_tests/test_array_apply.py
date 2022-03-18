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
                "process": f"({{x}}) => x + 10",
            },
            [],
        ),
        (
            {
                "data": [1, 2, 3, 4, 5],
                "process": f"({{x}}) => x + 10",
            },
            [11, 12, 13, 14, 15],
        ),
        (
            {
                "data": [-1, 0, 1, 100],
                "process": f"({{x}}) => x * 10",
            },
            [-10, 0, 10, 1000],
        ),
        (
            {
                "data": [1, 10, 2, 24, 23, -12],
                "process": f"({{x}}) => (x - 10) / 2",
            },
            [-4.5, 0, -4, 7, 6.5, -11],
        ),
    ],
)
def test_array_apply(array_apply_process_code, example_input, expected_output):
    process_js_code = f"const process = eval({example_input['process']});"
    process_arguments = f"{{'data': {example_input['data']}, 'process': process}}"
    output = run_process(
        array_apply_process_code + process_js_code,
        "array_apply",
        process_arguments,
    )
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        (
            {"process": f"({{x}}) => x + 10;"},
            True,
            "MISSING_PARAMETER",
        ),
        (
            {"data": None, "process": f"({{x}}) => x + 10;"},
            True,
            "NOT_NULL",
        ),
        ({"data": [1, 2, 3, 4, 5]}, True, "MISSING_PARAMETER"),
        ({"data": [1, 2, 3, 4, 5], "process": None}, True, "NOT_NULL"),
        (
            {"data": "[1,2,3,4,5]", "process": f"({{x}}) => x + 10;"},
            True,
            "NOT_ARRAY",
        ),
        ({"data": [1, 2, 3, 4, 5], "process": 23}, True, "WRONG_TYPE"),
    ],
)
def test_array_apply_inputs(array_apply_process_code, example_input, raises_exception, error_name):
    process_js_code = (
        f"const process = eval({json.dumps(example_input['process']) if 'process' in example_input else 'undefined'});"
    )
    process_arguments = f"{{'data': {json.dumps(example_input['data']) if 'data' in example_input else 'undefined'}, 'process': process}}"
    run_input_validation(
        array_apply_process_code + process_js_code, "array_apply", process_arguments, raises_exception, error_name
    )
