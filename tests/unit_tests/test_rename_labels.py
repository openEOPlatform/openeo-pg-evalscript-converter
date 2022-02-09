import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def rename_labels_process_code():
    return load_process_code("rename_labels")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        (
            {
                'data': [1,2,3],
                'dimension': 'test_dimension',
                'label': 'test_label',
                'target': ['new_test_label'],
            }, 
            "The number of labels in the parameters `source` and `target` don't match."
        ),
        (
            {
                'data': [1,2,3],
                'dimension': 'test_dimension',
                'label': 'test_label',
                'should_corrupt_labels': True,
            }, 
            "The dimension labels are not enumerated."
        ),
        (
            {
                'data': [1,2,3],
                'dimension': 'test_dimension',
                'label': 'test_label',
                'target': ['test_label'],
                'source': ['test_label']
            },  
            "A label with the specified name exists."
        ),
        (
            {
                'data': [1,2,3],
                'dimension': 'test_dimension',
                'label': 'test_label',
                'target': ['new_test_label'],
                'source': ['fake_test_label']
            }, 
            "A label with the specified name does not exist."
        ),
        (
            {
                'data': [1,2,3],
                'dimension': 'test_dimension',
                'label': 'test_label',
                'target': ['new_test_label'],
                'source': ['test_label']
            }, 
            {
                'BANDS': 'bands', 
                'OTHER': 'other', 
                'TEMPORAL': 'temporal', 
                'bands_dimension_name': 'bands_name', 
                'temporal_dimension_name': 'temporal_name',
                'dimensions': [
                    {'labels': ['new_test_label'], 'name': 'test_dimension', 'type': 'other'},
                    {'labels': [], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': [], 'name': 'bands_name', 'type': 'bands'}],
                'data': [[1,2,3]]
            }
        ),
    ],
)
def test_rename_labels(rename_labels_process_code, example_input, expected_output):
    output = run_process(rename_labels_process_code, "_rename_labels", example_input)
    output = json.loads(output)
    assert output == expected_output
