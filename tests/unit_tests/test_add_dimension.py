import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def add_dimension_process_code():
    return load_process_code("add_dimension")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        (
            {
                'data': [1,2,3], 
                'name': 'test_new_dimensions', 
                'label': 'test_new_label'
            }, 
            {
                'BANDS': 'bands', 
                'OTHER': 'other', 
                'TEMPORAL': 'temporal', 
                'bands_dimension_name': 'bands_name', 
                'temporal_dimension_name': 'temporal_name',
                'dimensions': [
                    {'labels': ['test_new_label'], 'name': 'test_new_dimensions', 'type': 'other'},
                    {'labels': [], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': [], 'name': 'bands_name', 'type': 'bands'}],
                'data': [[1,2,3]]
            }
        ),
        (
            {
                'data': [1,2,3], 
                'name': 'test_new_dimensions', 
                'label': 'test_new_label',
                'type': 'bands'
            }, 
            {
                'BANDS': 'bands', 
                'OTHER': 'other', 
                'TEMPORAL': 'temporal', 
                'bands_dimension_name': 'bands_name', 
                'temporal_dimension_name': 'temporal_name',
                'dimensions': [
                    {'labels': ['test_new_label'], 'name': 'test_new_dimensions', 'type': 'bands'},
                    {'labels': [], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': [], 'name': 'bands_name', 'type': 'bands'}],
                'data': [[1,2,3]]
            }
        ),
        (
            {
                'data': [1,2,3], 
                'name': 'test_new_dimensions', 
                'label': 23,
                'type': 'spatial'
            }, 
            {
                'BANDS': 'bands', 
                'OTHER': 'other', 
                'TEMPORAL': 'temporal', 
                'bands_dimension_name': 'bands_name', 
                'temporal_dimension_name': 'temporal_name',
                'dimensions': [
                    {'labels': [23], 'name': 'test_new_dimensions', 'type': 'spatial'},
                    {'labels': [], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': [], 'name': 'bands_name', 'type': 'bands'}],
                'data': [[1,2,3]]
            }
        ),
        (
            {
                'data': [1,2,3], 
                'name': 'temporal_name', 
                'label': 23,
            }, 
            'A dimension with the specified name already exists.'
        )
    ],
)
def test_add_dimension(add_dimension_process_code, example_input, expected_output):
    output = run_process(add_dimension_process_code, "_add_dimension", example_input)
    output = json.loads(output)
    assert output == expected_output
