import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def merge_cubes_process_code():
    return load_process_code("merge_cubes")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        (
            {
                'cube1': {'B01':[1,2,3],'B02':[4,5,6],'B03':[7,8,9]},
                'cube2': {'B04':[11,12,13],'B05':[14,15,16],'B06':[17,18,19]}
            }, 
            'Overlapping data cubes, but no overlap resolver has been specified.'
        ),
        (
            {
                'cube1': {'B01':[1,2,3],'B02':[4,5,6],'B03':[7,8,9]},
                'cube2': {'B01':[11,12,13],'B02':[14,15,16],'B03':[17,18,19]}
            }, 
            {
                'BANDS': 'bands', 
                'OTHER': 'other', 
                'TEMPORAL': 'temporal', 
                'bands_dimension_name': 'bands_name', 
                'temporal_dimension_name': 'temporal_name',
                'dimensions': [
                    {'labels': [], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': ['B01', 'B02', 'B03'], 'name': 'bands_name', 'type': 'bands'}],
                'data': [[1,2,3],[4,5,6],[7,8,9]]
            }
        ),
        (
            {
                'cube1': {'B01':[1,2,3],'B02':[4,5,6],'B03':[7,8,9]},
                'cube2': {'B04':[11,12,13],'B05':[14,15,16],'B06':[17,18,19]},
                'should_use_overlap_resolver': True,
                'overlap_resolver_code': '({x,y}) => { if ((x*3) >= y) { return x; } return y; }'
            }, 
            {
                'BANDS': 'bands', 
                'OTHER': 'other', 
                'TEMPORAL': 'temporal', 
                'bands_dimension_name': 'bands_name', 
                'temporal_dimension_name': 'temporal_name',
                'dimensions': [
                    {'labels': [], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': ['B01', 'B02', 'B03'], 'name': 'bands_name', 'type': 'bands'}],
                'data': [[11,12,13],[14,5,6],[7,8,9]]
            }
        ),
        (
            {
                'cube1': {'B01':[1,2,3],'B02':[4,5,6],'B03':[7,8,9]},
                'cube2': {'B04':[11,12,13],'B05':[14,15,16],'B06':[17,18,19]},
                'should_use_overlap_resolver': True,
                'overlap_resolver_code': '({x,y}) => { return y; }'
            }, 
            {
                'BANDS': 'bands', 
                'OTHER': 'other', 
                'TEMPORAL': 'temporal', 
                'bands_dimension_name': 'bands_name', 
                'temporal_dimension_name': 'temporal_name',
                'dimensions': [
                    {'labels': [], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': ['B01', 'B02', 'B03'], 'name': 'bands_name', 'type': 'bands'}],
                'data': [[11,12,13],[14,15,16],[17,18,19]]
            }
        ),
    ],
)
def test_merge_cubes(merge_cubes_process_code, example_input, expected_output):
    output = run_process(merge_cubes_process_code, "_merge_cubes", example_input)
    output = json.loads(output)
    assert output == expected_output
