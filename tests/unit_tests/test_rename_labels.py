import json

import pytest

from tests.utils import load_process_code, run_process_with_datacube


@pytest.fixture
def rename_labels_process_code():
    return load_process_code("rename_labels")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
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
                "data": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            },
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
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
                "data": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            },
        ),
    ],
)
def test_rename_labels(rename_labels_process_code, example_input, expected_output):
    output = run_process_with_datacube(rename_labels_process_code, "rename_labels", example_input)
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
                "target": ["A123"],
                "source": [],
            },
            True,
            "The number of labels in the parameters `source` and `target` do not match.",
        ),
    ],
)
def test_rename_labels_exceptions(rename_labels_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process_with_datacube(rename_labels_process_code, "rename_labels", example_input)
        assert error_message in str(exc.value)

    else:
        run_process_with_datacube(rename_labels_process_code, "rename_labels", example_input)
