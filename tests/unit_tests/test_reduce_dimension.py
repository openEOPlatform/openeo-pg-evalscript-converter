import json

import pytest

from tests.utils import (
    load_process_code,
    load_datacube_code,
    run_process,
    run_input_validation,
)


@pytest.fixture
def reduce_dimension_process_code():
    return load_process_code("reduce_dimension")


@pytest.mark.parametrize(
    "example_input,expected_result",
    [
        (
            {
                "data": [
                    {"B01": 1, "B02": 2, "B03": 3},
                    {"B01": 6, "B02": 5, "B03": 4},
                    {"B01": 7, "B02": 0, "B03": -1},
                ],
                "bands": ["B01", "B02", "B03"],
                "reducer": "({data})=>0",
                "dimension": "temporal",
            },
            [0, 0, 0],
        ),
        (
            {
                "data": [{"B01": 1, "B02": 2, "B03": 3}],
                "bands": ["B01", "B02", "B03"],
                "reducer": "({data})=>{return Math.min(...data)}",
                "dimension": "temporal",
            },
            [1, 2, 3],
        ),
        (
            {
                "data": [{"B01": 1, "B02": 2, "B03": 3}],
                "bands": ["B01", "B02", "B03"],
                "reducer": "({data})=>{return Math.min(...data)}",
                "dimension": "bands",
            },
            [1],
        ),
        (
            {
                "data": [
                    {"B01": 1, "B02": 2, "B03": 3},
                    {"B01": 4, "B02": -5, "B03": 6},
                ],
                "bands": ["B01", "B02", "B03"],
                "reducer": "({data})=>{return Math.min(...data)}",
                "dimension": "temporal",
            },
            [1, -5, 3],
        ),
        (
            {
                "data": [
                    {"B01": 1, "B02": 2, "B03": 3},
                    {"B01": 4, "B02": -5, "B03": 6},
                ],
                "bands": ["B01", "B02", "B03"],
                "reducer": "({data})=>{return Math.min(...data)}",
                "dimension": "bands",
            },
            [1, -5],
        ),
    ],
)
def test_reduce_dimension(reduce_dimension_process_code, example_input, expected_result):
    additional_js_code_to_run = (
        load_datacube_code() + f"const cube = new DataCube({example_input['data']}, 'bands', 'temporal', true);"
    )
    process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube, 'reducer':{example_input['reducer']}}}"
    output = run_process(
        reduce_dimension_process_code + additional_js_code_to_run,
        "reduce_dimension",
        process_arguments,
    )
    output = json.loads(output)

    assert output["data"]["data"] == expected_result


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        (
            {
                "data": [
                    {"B01": 1, "B02": 2, "B03": 3},
                    {"B01": 6, "B02": 5, "B03": 4},
                    {"B01": 7, "B02": 0, "B03": -1},
                ],
                "dimension": "bands",
                "reducer": "({data})=>1",
            },
            False,
            None,
        ),
        (
            {
                "data": [
                    {"B01": 1, "B02": 2, "B03": 3},
                    {"B01": 6, "B02": 5, "B03": 4},
                    {"B01": 7, "B02": 0, "B03": -1},
                ],
                "bands": ["B01", "B02", "B03"],
                "dimension": "bands",
            },
            True,
            "MISSING_PARAMETER",
        ),
        (
            {
                "data": [
                    {"B01": 1, "B02": 2, "B03": 3},
                    {"B01": 6, "B02": 5, "B03": 4},
                    {"B01": 7, "B02": 0, "B03": -1},
                ],
                "bands": ["B01", "B02", "B03"],
                "reducer": "({data})=>1",
            },
            True,
            "MISSING_PARAMETER",
        ),
        (
            {"reducer": "({data})=>1", "dimension": "bands"},
            True,
            "MISSING_PARAMETER",
        ),
        (
            {
                "data": [{"B01": 1, "B02": 2, "B03": 3}],
                "dimension": 1,
                "reducer": "({data})=>1",
            },
            True,
            "WRONG_TYPE",
        ),
    ],
)
def test_input_validation(reduce_dimension_process_code, example_input, raises_exception, error_name):

    data = example_input["data"] if "data" in example_input else None
    reducer = example_input["reducer"] if "reducer" in example_input else None

    cube = f"const cube = new DataCube({data}, 'bands', 'temporal', true);" if data else f"const cube=undefined;"
    additional_js_code_to_run = load_datacube_code() + cube
    if reducer:
        process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube, 'reducer':{reducer}}}"
    else:
        process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube }}"

    run_input_validation(
        reduce_dimension_process_code + additional_js_code_to_run,
        "reduce_dimension",
        process_arguments,
        raises_exception,
        error_name,
    )
