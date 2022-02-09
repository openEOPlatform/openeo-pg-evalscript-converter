import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def filter_bands_process_code():
    return load_process_code("filter_bands")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        (
            {
                'data': {'B01':[1,2,3],'B02':[4,5,6],'B03':[7,8,9]}, 
            }, 
            'The process `filter_bands` requires any of the parameters `bands`, `common_names` or `wavelengths` to be set.'
        ),
        (
            {
                'data': {'B01':[1,2,3],'B02':[4,5,6],'B03':[7,8,9]}, 
                'bands': []
            }, 
            'The process `filter_bands` requires any of the parameters `bands`, `common_names` or `wavelengths` to be set.'
        ),
        (
            {
                'data': {'B01':[1,2,3],'B02':[4,5,6],'B03':[7,8,9]},
                'bands': ['B01','B02'],
                'shouldRemoveBandsDim': True 
            }, 
            'A band dimension is missing.'
        ),
        (
            {
                'data': {'B01':[1,2,3],'B02':[4,5,6],'B03':[7,8,9]},
                'bands': ['B01','B02'],
            }, 
            {
                'BANDS': 'bands', 
                'OTHER': 'other', 
                'TEMPORAL': 'temporal', 
                'bands_dimension_name': 'bands_name', 
                'temporal_dimension_name': 'temporal_name',
                'dimensions': [
                    {'labels': [], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': ['B01', 'B02'], 'name': 'bands_name', 'type': 'bands'}],
                'data': [[1,2],[4,5],[7,8]]
            }
        ),
        (
            {
                'data': {'B01':[1,2,3],'B02':[4,5,6],'B03':[7,8,9]},
                'bands': ['abc','def'],
            }, 
            {
                'BANDS': 'bands', 
                'OTHER': 'other', 
                'TEMPORAL': 'temporal', 
                'bands_dimension_name': 'bands_name', 
                'temporal_dimension_name': 'temporal_name',
                'dimensions': [
                    {'labels': [], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': [], 'name': 'bands_name', 'type': 'bands'}],
            }
        ),
        (
            {
                'data': {'B01':[1,2,3],'B02':[4,5,6],'B03':[7,8,9]},
                'bands': ['B01','B02','B03'],
            }, 
            {
                'BANDS': 'bands', 
                'OTHER': 'other', 
                'TEMPORAL': 'temporal', 
                'bands_dimension_name': 'bands_name', 
                'temporal_dimension_name': 'temporal_name',
                'dimensions': [
                    {'labels': [], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': ['B01','B02','B03'], 'name': 'bands_name', 'type': 'bands'}],
                'data': [[1,2,3],[4,5,6],[7,8,9]]
            }
        ),
        (
            {
                'data': {'B01':[1,2,3],'B02':[4,5,6],'B03':[7,8,9]},
                'bands': ['B03'],
            }, 
            {
                'BANDS': 'bands', 
                'OTHER': 'other', 
                'TEMPORAL': 'temporal', 
                'bands_dimension_name': 'bands_name', 
                'temporal_dimension_name': 'temporal_name',
                'dimensions': [
                    {'labels': [], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': ['B03'], 'name': 'bands_name', 'type': 'bands'}],
                'data': [[3],[6],[9]]
            }
        ),
    ],
)
def test_filter_bands(filter_bands_process_code, example_input, expected_output):
    output = run_process(filter_bands_process_code, "_filter_bands", example_input)
    output = json.loads(output)
    assert output == expected_output
