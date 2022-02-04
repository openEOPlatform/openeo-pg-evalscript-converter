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
    ]
)
def test_array_element(array_element_process_code, example_input, expected_output ):
    output = run_process(array_element_process_code, "array_element", example_input)
    output = json.loads(output)
    assert output == expected_output
