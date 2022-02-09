import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def array_element_process_code():
    return load_process_code("array_element")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({'data': [9,8,7,6,5], 'index': 2}, 7),
        ({'data': ['A','B','C'], 'index': 0}, 'A'),
        ({'data': [], 'index': 0, 'return_nodata': True}, None),
        ({'data': [1,2,3], 'labels': ['one','two','three'], 'label':'two'}, 2),
        ({'data': [1,2,3], 'labels': ['one','two','three'], 'label':'four', 'return_nodata': True}, None),
        ({'data': [5,'ABC',True,None], 'index': 0}, 5),
        ({'data': [5,'ABC',True,None], 'index': 1, 'return_nodata': True}, 'ABC'),
        ({'data': [5,'ABC',True,None], 'labels': ['number','string','bool','null'], 'label': 'bool'}, True),
        ({'data': [5,'ABC',True,None], 'labels': ['number','string','bool','null'], 'label': 'null'}, None),
        ({'data': [5,'ABC',True,None], 'labels': ['number','string','bool','null'], 'label': 'True', 'return_nodata': True}, None),
        ({'data': [5,'ABC', {'name': 'John', 'age': 27}, [1, True, False, None]], 'index': 3}, [1, True, False, None]),
        ({'data': [1,2,3]}, "The process `array_element` requires either the `index` or `labels` parameter to be set."),
        ({'data': [1,2,3], 'index': 2, 'label': 'two'}, "The process `array_element` only allows that either the `index` or the `labels` parameter is set."),
        ({'data': [1,2,3], 'index': 4}, "The array has no element with the specified index or label."),
        ({'data': [1,2,3], 'label': 'two'}, "The array is not a labeled array, but the `label` parameter is set. Use the `index` instead."),
        ({'data': [1,2,3], 'labels': ['one','two','three'], 'label':'four'}, 'The array has no element with the specified index or label.'),
    ]
)
def test_array_element(array_element_process_code, example_input, expected_output ):
    output = run_process(array_element_process_code, "_array_element", example_input)
    output = json.loads(output)
    assert output == expected_output
