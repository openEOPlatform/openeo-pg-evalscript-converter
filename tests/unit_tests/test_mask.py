import json

import pytest

from tests.utils import load_process_code, load_datacube_code, run_process


@pytest.fixture
def mask_process_code():
    return load_process_code("mask")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        # basic, same dimensions and labels in data and mask, mask contains numbers
        (
            {
                "data": [{"B01": 1}, {"B01": 2}, {"B01": 3}],
                "mask": [{"B01": 0}, {"B01": 1}, {"B01": 0}],
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B01"], "name": "bands_name", "type": "bands"},
                ],
                "data": {'data': [1, None, 3], 'offset': 0, 'shape': [3, 1], 'stride': [1, 1]},
            },
        ),

        # basic, same dimensions and labels in data and mask, mask contains booleans
        (
            {
                "data": [{"B01": 1}, {"B01": 2}, {"B01": 3}],
                "mask": [{"B01": False}, {"B01": True}, {"B01": False}],
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B01"], "name": "bands_name", "type": "bands"},
                ],
                "data": {'data': [1, None, 3], 'offset': 0, 'shape': [3, 1], 'stride': [1, 1]},
            },
        ),

        # basic, same dimensions and labels in data and mask, mask contains booleans, replace with 'aaa'
        (
            {
                "data": [{"B01": 1}, {"B01": 2}, {"B01": 3}],
                "mask": [{"B01": False}, {"B01": True}, {"B01": False}],
                "replacement": 'aaa',
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B01"], "name": "bands_name", "type": "bands"},
                ],
                "data": {'data': [1, 'aaa', 3], 'offset': 0, 'shape': [3, 1], 'stride': [1, 1]},
            },
        ),

        # multiple labels for bands
        (
            {
                "data": [{"B01": 1, "B02": 1}, {"B01": 2, "B02": 2}, {"B01": 3, "B02": 3}],
                "mask": [{"B01": 0, "B02": 0}, {"B01": 1, "B02": 0}, {"B01": 1, "B02": 1}],
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B01", "B02"], "name": "bands_name", "type": "bands"},
                ],
                "data": {'data': [1, 1, None, 2, None, None], 'offset': 0, 'shape': [3, 2], 'stride': [2, 1]},
            },
        ),

        # no data, no mask
        (
            {
                "data": [],
                "mask": [],
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
                "data": {'data': [], 'offset': 0, 'shape': [0], 'stride': [1]},
            },
        ),
    ],
)
def test_mask(mask_process_code, example_input, expected_output):
    vars_definitions = (
        f"const data = new DataCube({json.dumps(example_input['data'])}, 'bands_name', 'temporal_name', true);"
        + f"const mask1 = new DataCube({json.dumps(example_input['mask'])}, 'bands_name', 'temporal_name', true);"
    )

    if 'replacement' in example_input:
        vars_definitions = ( 
            vars_definitions 
            + f"const replacement = {json.dumps(example_input['replacement'])};"
        ) 
    
    additional_js_code_to_run = (
        load_datacube_code()
        + vars_definitions
    )

    arguments = (
        f"...{json.dumps(example_input)}"
        + f", 'data': data, 'mask': mask1"
    )

    if 'replacement' in example_input:
        arguments = ( arguments  + f", 'replacement': replacement" )

    process_arguments = ( f"{{" + arguments + f"}}" )


    # print("// ------------ vars_def ------------")
    # print(vars_definitions)

#     print("// ---------- additional js code -------------")
#     print(additional_js_code_to_run)

#     print("// ---------- mask process code -------------")
#     print(mask_process_code)
    
#     print("// ------------ arg ------------")
#     print("const res = mask(" + process_arguments + ")")
#     console_log = '''console.log('res', {
#   res,
#   resJSON: JSON.stringify(res),
#   d: res.data
# });'''
#     print(console_log)

    output = run_process(
        mask_process_code + additional_js_code_to_run,
        "mask",
        process_arguments,
    )
    output = json.loads(output)

    # print("output")
    # print(output)
    
    assert output == expected_output
