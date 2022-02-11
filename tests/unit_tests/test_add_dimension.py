import json

import pytest

from tests.utils import load_process_code, run_process_with_datacube


@pytest.fixture
def add_dimension_process_code():
    return load_process_code("add_dimension")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        (
            {
                'data': {'B01':[1,2,3],'B02':[4,5,6],'B03':[7,8,9]}, 
                'name': 'test_new_dimension', 
                'label': 'test_new_label'
            }, 
            {
                'BANDS': 'bands', 
                'OTHER': 'other', 
                'TEMPORAL': 'temporal', 
                'bands_dimension_name': 'bands_name', 
                'temporal_dimension_name': 'temporal_name',
                'dimensions': [
                    {'labels': ['test_new_label'], 'name': 'test_new_dimension', 'type': 'other'},
                    {'labels': [], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': ['B01','B02','B03'], 'name': 'bands_name', 'type': 'bands'}],
                'data': [[[1,2,3],[4,5,6],[7,8,9]]]
            }
        ),
        (
            {
                'data': {'B01':[1,2,3],'B02':[4,5,6],'B03':[7,8,9]},
                'name': 'test_bands_name', 
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
                    {'labels': ['test_new_label'], 'name': 'test_bands_name', 'type': 'bands'},
                    {'labels': [], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': ['B01','B02','B03'], 'name': 'bands_name', 'type': 'bands'}],
                'data': [[[1,2,3],[4,5,6],[7,8,9]]]
            }
        ),
        (
            {
                'data': {'B01':[1,2,3],'B02':[4,5,6],'B03':[7,8,9]},
                'name': 'test_spatial_name', 
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
                    {'labels': [23], 'name': 'test_spatial_name', 'type': 'spatial'},
                    {'labels': [], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': ['B01','B02','B03'], 'name': 'bands_name', 'type': 'bands'}],
                'data': [[[1,2,3],[4,5,6],[7,8,9]]]
            }
        ),
        (
            {
                'data': {'B01':[1,2,3],'B02':[4,5,6],'B03':[7,8,9]},
                'name': 'temporal_name', 
                'label': 23,
            }, 
            'A dimension with the specified name already exists.'
        )
    ],
)
def test_add_dimension(add_dimension_process_code, example_input, expected_output):
    output = run_process_with_datacube(add_dimension_process_code, "add_dimension", example_input)
    output = json.loads(output)
    assert output == expected_output
