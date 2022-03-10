import json

import pytest

from tests.utils import load_process_code, load_datacube_code, run_process_with_additional_js_code


@pytest.fixture
def drop_dimension_process_code():
    return load_process_code("drop_dimension")


@pytest.mark.parametrize(
    "data,name,additional_js_code_specific_to_case,expected_output",
    [
        (
            {"B01": [1, 2, 3]},
            "temporal_name",
            None,
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": ["B01"], "name": "bands_name", "type": "bands"},
                ],
                "data": [1, 2, 3],
            },
        ),
        (
            {"B01": [1, 2, 3, 4], "B02": [5, 6, 7, 8], "B03": [9, 10, 11, 12], "B04": [13, 14, 15, 16]},
            "temporal_name",
            "cube.addDimension('x', 'x_label', 'spatial');"
            + "cube.addDimension('y', 'y_label', 'spatial');"
            + "cube.data = [[[[1,2,3,4]], [[5,6,7,8]]], [[[9,10,11,12]], [[13,14,15,16]]]];",
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": ["y_label"], "name": "y", "type": "spatial"},
                    {"labels": ["x_label"], "name": "x", "type": "spatial"},
                    {"labels": ["B01", "B02", "B03", "B04"], "name": "bands_name", "type": "bands"},
                ],
                "data": [[[1, 2, 3, 4], [5, 6, 7, 8]], [[9, 10, 11, 12], [13, 14, 15, 16]]],
            },
        ),
        (
            {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
            "test_name_to_remove",
            "cube.addDimension('test_name_to_remove', 'label123', 'other');",
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B01", "B02", "B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            },
        ),
    ],
)
def test_drop_dimension(drop_dimension_process_code, data, name, additional_js_code_specific_to_case, expected_output):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube = new DataCube({data}, 'bands_name', 'temporal_name', true);"
        + (additional_js_code_specific_to_case or "")
    )
    process_arguments = f"{{'data': cube, 'name': '{name}'}}"
    output = run_process_with_additional_js_code(
        drop_dimension_process_code,
        "drop_dimension",
        process_arguments,
        additional_js_code_to_run,
    )
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "data,name,additional_js_code_specific_to_case,raises_exception,error_message",
    [
        (
            {"B01": [1, 2, 3]},
            "bands_name",
            None,
            False,
            None,
        ),
        (
            {"B01": [1, 2, 3]},
            "bands_name",
            "cube = null;",
            True,
            "Mandatory argument `data` is either null or not defined.",
        ),
        (
            {"B01": [1, 2, 3]},
            "bands_name",
            "cube = undefined;",
            True,
            "Mandatory argument `data` is either null or not defined.",
        ),
        (
            {"B01": [1, 2, 3]},
            None,
            None,
            True,
            "Mandatory argument `name` is either null or not defined.",
        ),
        (
            {"B01": [1, 2, 3]},
            None,
            None,
            True,
            "Mandatory argument `name` is either null or not defined.",
        ),
        (
            {"B01": [1, 2, 3]},
            True,
            None,
            True,
            "Argument `name` is not a string.",
        ),
        (
            {"B01": [1, 2, 3]},
            "bands_fake_name",
            None,
            True,
            "A dimension with the specified name does not exist.",
        ),
        (
            {"B01": [1, 2, 3], "B02": [4, 5, 6]},
            "bands_name",
            None,
            True,
            "The number of dimension labels exceeds one, which requires a reducer.",
        ),
    ],
)
def test_drop_dimension_exceptions(
    drop_dimension_process_code, data, name, additional_js_code_specific_to_case, raises_exception, error_message
):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"let cube = new DataCube({data}, 'bands_name', 'temporal_name', true);"
        + (additional_js_code_specific_to_case or "")
    )
    process_arguments = f"{{'data': cube, 'name': '{name}'}}"
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process_with_additional_js_code(
                drop_dimension_process_code,
                "drop_dimension",
                process_arguments,
                additional_js_code_to_run,
            )
        assert error_message in str(exc.value)

    else:
        run_process_with_additional_js_code(
            drop_dimension_process_code,
            "drop_dimension",
            process_arguments,
            additional_js_code_to_run,
        )
