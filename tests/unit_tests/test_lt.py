import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def lt_process_code():
    return load_process_code("lt")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({'x': 1, 'y': 2}, True),
        ({'x': 100, 'y': 100.000001}, True),
        ({'x': 23, 'y': 22}, False),
        ({'x': -123, 'y': -124}, False),
        ({'x': 0, 'y': 0}, False),
        ({'x': -0.5, 'y': -0.6}, False),
        ({'x': None, 'y': 1}, None),
        ({'x': 2, 'y': None}, None),
        ({'x': [1,2,3], 'y': None}, None),
        ({'x': [1,2,3], 'y': 100}, False),
        ({'x': 1, 'y': [100, 1002]}, False),
        ({'x': "00:00:00+01:00", 'y': "00:00:00Z"}, True),
        ({'x': "1950-01-01T00:00:00Z", 'y': "2018-01-01T12:00:00Z"}, True),
        ({'x': "2018-01-01T12:00:00+00:00", 'y': "2018-01-01T12:00:00Z"}, False),
        ({'x': 0, 'y': False}, False),
        ({'x': True, 'y': False}, False),
        ({'x': {
            'name': 'John',
            'surname': 'Doe'
        }, 'y': 2}, False),
        ({'x': None, 'y': {
            'name': 'John',
            'surname': 'Doe'
        }}, None),
        ({'x': 23, 'y': {
            'name': 'John',
            'surname': 'Doe'
        }}, False)
    ]
)
def test_lt(lt_process_code, example_input, expected_output ):
    output = run_process(lt_process_code, "lt", example_input)
    output = json.loads(output)
    assert output == expected_output
