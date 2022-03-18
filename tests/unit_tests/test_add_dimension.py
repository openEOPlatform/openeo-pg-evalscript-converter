import json

import pytest
import subprocess

from tests.utils import load_process_code, load_datacube_code, run_process


@pytest.fixture
def add_dimension_process_code():
    return load_process_code("add_dimension")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "name": "test_new_dimension",
                "label": "test_new_label",
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": ["test_new_label"], "name": "test_new_dimension", "type": "other"},
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B01", "B02", "B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]],
            },
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "name": "test_bands_name",
                "label": "test_new_label",
                "type": "bands",
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": ["test_new_label"], "name": "test_bands_name", "type": "bands"},
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B01", "B02", "B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]],
            },
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "name": "test_spatial_name",
                "label": 23,
                "type": "spatial",
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": [23], "name": "test_spatial_name", "type": "spatial"},
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B01", "B02", "B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]],
            },
        ),
    ],
)
def test_add_dimension(add_dimension_process_code, example_input, expected_output):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube = new DataCube({example_input['data']}, 'bands_name', 'temporal_name', true);"
    )
    process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube}}"
    output = run_process(
        add_dimension_process_code + additional_js_code_to_run,
        "add_dimension",
        process_arguments,
    )
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "name": "test_spatial_name",
                "label": 23,
                "type": "spatial",
            },
            False,
            None,
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "name": "temporal_name",
                "label": 23,
            },
            True,
            "A dimension with the specified name already exists.",
        ),
        (
            {"data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]}, "label": 23},
            True,
            "Process add_dimension requires parameter name.",
        ),
        (
            {"data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]}, "name": "temporal_name"},
            True,
            "Process add_dimension requires parameter label.",
        ),
        ({"data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]}, "name": 23, "label": 23}, True, "WRONG_TYPE"),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "name": "temporal_name",
                "label": [1, 2, 3],
            },
            True,
            "Value for label is not a string or a number.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "name": "temporal_name",
                "label": 23,
                "type": 123,
            },
            True,
            "Value for type is not a string",
        ),
    ],
)
def test_add_dimension_exceptions(add_dimension_process_code, example_input, raises_exception, error_message):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube = new DataCube({example_input['data']}, 'bands_name', 'temporal_name', true);"
    )
    process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube}}"
    if raises_exception:
        try:
            run_process(
                add_dimension_process_code + additional_js_code_to_run,
                "add_dimension",
                process_arguments,
            )
        except subprocess.CalledProcessError as exc:
            assert error_message in str(exc.stderr)

    else:
        run_process(
            add_dimension_process_code + additional_js_code_to_run,
            "add_dimension",
            process_arguments,
        )
        