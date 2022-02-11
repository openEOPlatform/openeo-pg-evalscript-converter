import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def array_contains_process_code():
    return load_process_code("array_contains")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({'data': [1,2,3], 'value': 2}, True),
        ({'data': ["A","B","C"], 'value': "b"}, False),
        ({'data': [1,2,3], 'value': "2"}, False),
        ({'data': [1,2,None], 'value': None}, False),
        ({'data': [[1,2],[3,4]], 'value': [1,2]}, False),
        ({'data': [[1,2],[3,4]], 'value': 2}, False),
        ({'data': [{"a":"b"},{"c":"d"}], 'value': {"a":"b"}}, False),
        ({'data': ['12:23:54','13.1.2022','5/28/2013 10:30:15 AM'], 'value': '13.1.2022'}, True),
        ({'data': ['12:23:54','13.1.2022','5/28/2013 10:30:15 AM'], 'value': '13.1.2022+00:00'}, False)
    ],
)
def test_array_contains(array_contains_process_code, example_input, expected_output):
    output = run_process(array_contains_process_code, "array_contains", example_input)
    output = json.loads(output)
    assert output == expected_output
