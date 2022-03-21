import json

import pytest
import subprocess

from tests.utils import load_process_code, load_datacube_code, run_process, run_input_validation


@pytest.fixture
def apply_process_code():
    return load_process_code("apply")


@pytest.mark.parametrize(
    "example_input,process,expected_output",
    [
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "name": "test_apply",
            },
            "({x})=>x",
            {
                "TEMPORAL": "temporal",
                "BANDS": "bands",
                "OTHER": "other",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"name": "temporal_name", "labels": [], "type": "temporal"},
                    {"name": "bands_name", "labels": ["B01", "B02", "B03"], "type": "bands"},
                ],
                "data": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            },
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "name": "test_apply",
            },
            "({x})=>-x",
            {
                "TEMPORAL": "temporal",
                "BANDS": "bands",
                "OTHER": "other",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"name": "temporal_name", "labels": [], "type": "temporal"},
                    {"name": "bands_name", "labels": ["B01", "B02", "B03"], "type": "bands"},
                ],
                "data": [[-1, -2, -3], [-4, -5, -6], [-7, -8, -9]],
            },
        ),
        (
            {
                "data": {"B01": [1, -2, 3], "B02": [-4, 5, -6], "B03": [7, -8, 9]},
                "name": "test_apply",
            },
            "function abs(args){return Math.abs(args.x);}",
            {
                "TEMPORAL": "temporal",
                "BANDS": "bands",
                "OTHER": "other",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"name": "temporal_name", "labels": [], "type": "temporal"},
                    {"name": "bands_name", "labels": ["B01", "B02", "B03"], "type": "bands"},
                ],
                "data": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            },
        ),
    ],
)
def test_apply(apply_process_code, example_input, process, expected_output):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube = new DataCube({example_input['data']}, 'bands_name', 'temporal_name', true);"
    )
    process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube, 'process':{process}}}"
    output = run_process(
        apply_process_code + additional_js_code_to_run,
        "apply",
        process_arguments,
    )
    output = json.loads(output)

    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        (
            {"data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]}, "process": None},
            True,
            "MISSING_PARAMETER",
        ),
        (
            {"data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]}, "process": "()=>{}"},
            False,
            None,
        ),
        (
            {"data": None, "process": "x=>x"},
            True,
            "MISSING_PARAMETER",
        ),
    ],
)
def test_input_validation(apply_process_code, example_input, raises_exception, error_name):

    data = example_input["data"]
    process = example_input["process"]
    cube = (
        f"const cube = new DataCube({data}, 'bands_name', 'temporal_name', true);" if data else f"const cube=undefined;"
    )
    additional_js_code_to_run = load_datacube_code() + cube
    if process:
        process_arguments = f"{{'data': cube, 'process':{process}}}"
    else:
        process_arguments = f"{{'data': cube }}"

    run_input_validation(
        apply_process_code + additional_js_code_to_run, "apply", process_arguments, raises_exception, error_name
    )
