import json

import pytest

from tests.utils import load_process_code, load_datacube_code, run_process, run_input_validation


@pytest.fixture
def reduce_dimension_process_code():
    return load_process_code("reduce_dimension")


@pytest.mark.parametrize(
    "example_input,expected_result",
    [
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [6, 5, 4], "B03": [7, 0, 9]},
                "reducer": "({data})=>0",
                "dimension": "bands",
            },
            [0, 0, 0],
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [6, 5, 4], "B03": [7, 0, 9]},
                "reducer": "({data})=>{return Math.min(...data)}",
                "dimension": "bands",
            },
            [1, 4, 0],
        ),
    ],
)
def test_apply(reduce_dimension_process_code, example_input, expected_result):
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

    assert output["data"] == expected_result


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "dimension": "bands",
                "reducer": "({data})=>1",
            },
            False,
            None,
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "dimension": "bands",
            },
            True,
            "MISSING_PARAMETER",
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
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
