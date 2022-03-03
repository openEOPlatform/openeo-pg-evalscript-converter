import json

import pytest

from tests.utils import load_process_code, load_datacube_code, run_process_with_additional_js_code


@pytest.fixture
def drop_dimension_process_code():
    return load_process_code("drop_dimension")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        (
            {
                "data": {"B01": [1, 2, 3]},
                "name": "bands_name",
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                ],
                "data": [[1, 2, 3]],
            },
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "name": "temporal_name",
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": ["B01", "B02", "B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            },
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "name": "test_name_to_remove",
                "additional_js_code_specific_to_case": "cube.addDimension('test_name_to_remove', 'label123');",
            },
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
                "data": [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]],
            },
        ),
    ],
)
def test_drop_dimension(drop_dimension_process_code, example_input, expected_output):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube = new DataCube({example_input['data']}, 'bands_name', 'temporal_name', true);"
        + f"{example_input['additional_js_code_specific_to_case'] if 'additional_js_code_specific_to_case' in example_input else ''}"
    )
    process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube}}"
    output = run_process_with_additional_js_code(
        drop_dimension_process_code,
        "drop_dimension",
        process_arguments,
        additional_js_code_to_run,
    )
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        (
            {
                "data": {"B01": [1, 2, 3]},
                "name": "bands_name",
            },
            False,
            None,
        ),
        (
            {"data": {"B01": [1, 2, 3]}, "name": "bands_name", "additional_js_code_specific_to_case": "cube = null;"},
            True,
            "Mandatory argument `data` is either null or not defined.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3]},
                "name": "bands_name",
                "additional_js_code_specific_to_case": "cube = undefined;",
            },
            True,
            "Mandatory argument `data` is either null or not defined.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3]},
            },
            True,
            "Mandatory argument `name` is either null or not defined.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3]},
                "name": None,
            },
            True,
            "Mandatory argument `name` is either null or not defined.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3]},
                "name": True,
            },
            True,
            "Argument `name` is not a string.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3]},
                "name": "bands_fake_name",
            },
            True,
            "A dimension with the specified name does not exist.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6]},
                "name": "bands_name",
            },
            True,
            "The number of dimension labels exceeds one, which requires a reducer.",
        ),
    ],
)
def test_drop_dimension_exceptions(drop_dimension_process_code, example_input, raises_exception, error_message):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"let cube = new DataCube({example_input['data']}, 'bands_name', 'temporal_name', true);"
        + f"{example_input['additional_js_code_specific_to_case'] if 'additional_js_code_specific_to_case' in example_input else ''}"
    )
    process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube}}"
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
