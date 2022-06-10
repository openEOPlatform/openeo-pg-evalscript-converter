import json

import pytest

from tests.utils import load_process_code, load_datacube_code, run_process, run_input_validation


@pytest.fixture
def rename_labels_process_code():
    return load_process_code("rename_labels")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        (
            {
                "data": [{"B01": 1, "B02": 2, "B03": 3}],
                "dimension": "bands_name",
                "label": "B01",
                "target": ["A123"],
                "source": ["B01"],
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["A123", "B02", "B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": {"data": [1, 2, 3], "offset": 0, "shape": [1, 3], "stride": [3, 1]},
            },
        ),
        (
            {
                "data": [{"B01": 1, "B02": 2, "B03": 3}],
                "dimension": "bands_name",
                "label": "B03",
                "target": ["A123456"],
                "source": ["B03"],
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B01", "B02", "A123456"], "name": "bands_name", "type": "bands"},
                ],
                "data": {"data": [1, 2, 3], "offset": 0, "shape": [1, 3], "stride": [3, 1]},
            },
        ),
        (
            {
                "data": [{"B01": 1, "B02": 2, "B03": 3}],
                "dimension": "bands_name",
                "label": "B03",
                "target": ["A2", "A3"],
                "source": ["B02", "B03"],
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B01", "A2", "A3"], "name": "bands_name", "type": "bands"},
                ],
                "data": {"data": [1, 2, 3], "offset": 0, "shape": [1, 3], "stride": [3, 1]},
            },
        ),
        (
            {
                "data": [{"B01": 1, "B02": 2, "B03": 3}],
                "dimension": "bands_name",
                "label": "B03",
                "target": ["A123456"],
                "source": [],
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["A123456"], "name": "bands_name", "type": "bands"},
                ],
                "data": {"data": [1, 2, 3], "offset": 0, "shape": [1, 3], "stride": [3, 1]},
            },
        ),
    ],
)
def test_rename_labels(rename_labels_process_code, example_input, expected_output):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube = new DataCube({example_input['data']}, 'bands_name', 'temporal_name', true);"
    )
    process_arguments = f"Object.assign({json.dumps(example_input)}, {{'data': cube}})"
    output = run_process(
        rename_labels_process_code + additional_js_code_to_run,
        "rename_labels",
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
                "dimension": "bands_name",
                "label": "B01",
                "target": ["A123"],
                "source": ["B01"],
            },
            False,
            None,
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "dimension": "bands_name",
                "label": "B01",
                "target": ["A123", "A234"],
                "source": ["B01"],
            },
            True,
            "The number of labels in the parameters `source` and `target` do not match.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "label": "B01",
                "target": ["A123"],
                "source": ["B01"],
            },
            True,
            "Mandatory argument `dimension` is not defined.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "dimension": "bands_name",
                "label": "B01",
                "source": ["B01"],
            },
            True,
            "Mandatory argument `target` is not defined.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "dimension": 123,
                "label": "B01",
                "target": ["A123"],
                "source": ["B01"],
            },
            True,
            "Argument `dimension` is not a string.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "dimension": "bands_name",
                "label": "B01",
                "target": "A123",
                "source": ["B01"],
            },
            True,
            "Argument `target` is not an array.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "dimension": "bands_name",
                "label": "B01",
                "target": ["A123"],
                "source": "B01",
            },
            True,
            "Argument `source` is not an array.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "dimension": "bands_name",
                "label": "B01",
                "target": [{"name": "John"}],
                "source": ["B01"],
            },
            True,
            "Element in argument `target` is not a number or a string.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "dimension": "bands_name",
                "label": "B01",
                "target": ["A123"],
                "source": [{"name": "John"}],
            },
            True,
            "Element in argument `source` is not a number or a string.",
        ),
    ],
)
def test_rename_labels_exceptions(rename_labels_process_code, example_input, raises_exception, error_message):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube = new DataCube({example_input['data']}, 'bands_name', 'temporal_name', true);"
    )
    process_arguments = f"Object.assign({json.dumps(example_input)}, {{'data': cube}})"
    run_input_validation(
        rename_labels_process_code + additional_js_code_to_run,
        "rename_labels",
        process_arguments,
        raises_exception,
        error_message=error_message,
    )
