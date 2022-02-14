import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def first_process_code():
    return load_process_code("first")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({'data': []}, None),
        ({'data': [1,2,3]}, 1),
        ({'data': [10,0,3,2]}, 10),
        ({'data': [None, "A","B","C"]}, "A"),
        ({'data': [None, "A","B","C"], 'ignore_nodata': False}, None),
        ({'data': [None,1,2,3]}, 1),
        ({'data': [None,1,2,3], 'ignore_nodata': False}, None),
        ({'data': [[1,2],[3,4]]}, [1,2]),
        ({'data': [1,2,None]}, 1),
        ({'data': [{"a":"b"},{"c":"d"}]}, {"a":"b"})
    ],
)
def test_first(first_process_code, example_input, expected_output):
    output = run_process(first_process_code, "first", example_input)
    output = json.loads(output)
    assert output == expected_output

@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({'data': [10,0,3,2]}, False, None),
        ({'data': None}, True, 'Mandatory argument `data` is either null or not defined.'),
        ({}, True, 'Mandatory argument `data` is either null or not defined.')
    ]
)
def test_first_exceptions(first_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(first_process_code, "first", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(first_process_code, "first", example_input)