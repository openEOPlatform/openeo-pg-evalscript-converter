import json

import pytest

from tests.utils import load_process_code, load_datacube_code, run_process_with_additional_js_code


@pytest.fixture
def filter_bands_process_code():
    return load_process_code("filter_bands")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        (
            {
                "data": [{"B01": 1, "B02": 2, "B03": 3}],
                "bands": ["abc", "def"],
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": [], "name": "bands_name", "type": "bands"},
                ],
                "data": {'data': [], 'offset': 0, 'shape': [1, 0], 'stride': [0, 1]}
            },
        ),
        (
            {
                "data": [{"B01": 1, "B02": 2, "B03": 3}],
                "bands": ["B01", "B02", "B03"],
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
                "data": {'data': [1, 2, 3], 'offset': 0, 'shape': [1, 3], 'stride': [3, 1]},
            },
        ),
        (
            {
                "data": [{"B01": 1, "B02": 2, "B03": 3}],
                "bands": ["B03"],
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": {'data': [3], 'offset': 0, 'shape': [1, 1], 'stride': [1, 1]},
            },
        ),
    ],
)
def test_filter_bands(filter_bands_process_code, example_input, expected_output):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube = new DataCube({example_input['data']}, 'bands_name', 'temporal_name', true);"
    )
    process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube}}"
    output = run_process_with_additional_js_code(
        filter_bands_process_code,
        "filter_bands",
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
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "bands": ["B01", "B02"],
            },
            False,
            None,
        ),
        (
            {"data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]}, "bands": []},
            True,
            "The process `filter_bands` requires any of the parameters `bands`, `common_names` or `wavelengths` to be set.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
            },
            True,
            "The process `filter_bands` requires any of the parameters `bands`, `common_names` or `wavelengths` to be set.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "bands": "[1,2,3]",
            },
            True,
            "Argument `bands` is not an array.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "bands": [1, 2, 3],
            },
            True,
            "Element in argument `bands` is not a string.",
        ),
    ],
)
def test_filter_bands_exceptions(filter_bands_process_code, example_input, raises_exception, error_message):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube = new DataCube({example_input['data']}, 'bands_name', 'temporal_name', true);"
    )
    process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube}}"
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process_with_additional_js_code(
                filter_bands_process_code,
                "filter_bands",
                process_arguments,
                additional_js_code_to_run,
            )
        assert error_message in str(exc.value)

    else:
        run_process_with_additional_js_code(
            filter_bands_process_code,
            "filter_bands",
            process_arguments,
            additional_js_code_to_run,
        )
