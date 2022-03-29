import json
from queue import Empty

import pytest

from tests.utils import (
    load_process_code,
    load_datacube_code,
    run_process,
    run_input_validation,
)


@pytest.fixture
def apply_dimension_process_code():
    return load_process_code("apply_dimension")


@pytest.mark.parametrize(
    "example_input,expected_result",
    [
        (
            {
                "data": [
                    {"B01": 1, "B02": 2},
                    {"B01": 3, "B02": 4},
                    {"B01": 5, "B02": 6},
                ],
                "process": "({data}) => data",
                "dimension": "temporal",
            },
            [1, 2, 3, 4, 5, 6],
        ),
        (
            {
                "data": [
                    {"B01": 1, "B02": 2},
                    {"B01": 3, "B02": 4},
                    {"B01": 5, "B02": 6},
                ],
                "process": "({data}) => data.map(el => el * 3)",
                "dimension": "temporal",
            },
            [3, 6, 9, 12, 15, 18],
        ),
        (
            {
                "data": [
                    {"B01": 1, "B02": 2},
                    {"B01": 3, "B02": 4},
                    {"B01": 5, "B02": 6},
                ],
                "process": "({data}) => {const sum = data.reduce((a, b) => a + b, 0); return data.map(el => el * sum)}",
                "dimension": "temporal",
            },
            [9, 24, 27, 48, 45, 72]
        ),
        (
            {
                "data": [
                    {"B01": 1, "B02": 2},
                    {"B01": 3, "B02": 4},
                    {"B01": 5, "B02": 6},
                ],
                "process": "({data}) => data",
                "dimension": "bands",
            },
            [1, 2, 3, 4, 5, 6],
        ),
        (
            {
                "data": [
                    {"B01": 1, "B02": 2},
                    {"B01": 3, "B02": 4},
                    {"B01": 5, "B02": 6},
                ],
                "process": "({data}) => data.map(el => el * 3)",
                "dimension": "bands",
            },
            [3, 6, 9, 12, 15, 18],
        ),
        (
            {
                "data": [
                    {"B01": 1, "B02": 2},
                    {"B01": 3, "B02": 4},
                    {"B01": 5, "B02": 6},
                ],
                "process": "({data}) => {const sum = data.reduce((a, b) => a + b, 0); return data.map(el => el * sum)}",
                "dimension": "bands",
            },
            [3, 6, 21, 28, 55, 66]
        ),
    ],
)
def test_apply_dimension(apply_dimension_process_code, example_input, expected_result):
    additional_js_code_to_run = (
        load_datacube_code() + f"const cube = new DataCube({example_input['data']}, 'bands', 'temporal', true);"
    )
    process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube, 'process':{example_input['process']}}}"
    output = run_process(
        apply_dimension_process_code + additional_js_code_to_run,
        "apply_dimension",
        process_arguments,
    )
    output = json.loads(output)

    assert output["data"]["data"] == expected_result


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        (
            {
                "data": [{ "B01": 1, "B02": 2, "B03": 3}],
                "process": "({data})=>1",
                "dimension": "bands",
            },
            False,
            None,
        ),
        (
            {
                "process": "({data})=>1",
                "dimension": "bands",
            },
            True,
            "MISSING_PARAMETER",
        ),
        (
            {
                "data": [{ "B01": 1, "B02": 2, "B03": 3}],
                "dimension": "bands",
            },
            True,
            "MISSING_PARAMETER",
        ),
        (
            {
                "data": [{ "B01": 1, "B02": 2, "B03": 3}],
                "process": "({data})=>1",
            },
            True,
            "MISSING_PARAMETER",
        ),
        (
            {
                "data": [{ "B01": 1, "B02": 2, "B03": 3}],
                "process": "({data})=>1",
                "dimension": True,
            },
            True,
            "WRONG_TYPE",
        ),
        (
            {
                "data": [{ "B01": 1, "B02": 2, "B03": 3}],
                "process": "({data})=>1",
                "dimension": "bands",
                "target_dimension": True,
            },
            True,
            "WRONG_TYPE",
        ),
    ],
)
def test_input_validation(apply_dimension_process_code, example_input, raises_exception, error_name):

    data = example_input.get("data")
    process = example_input.get("process")

    cube = f"const cube = new DataCube({data}, 'bands', 'temporal', true);" if data else f"const cube=undefined;"
    additional_js_code_to_run = load_datacube_code() + cube
    if process:
        process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube, 'process':{process}}}"
    else:
        process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube }}"

    run_input_validation(
        apply_dimension_process_code + additional_js_code_to_run,
        "apply_dimension",
        process_arguments,
        raises_exception,
        error_name,
    )
