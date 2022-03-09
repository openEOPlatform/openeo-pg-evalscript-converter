import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def array_contains_process_code():
    return load_process_code("array_contains")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [1, 2, 3], "value": 2}, True),
        ({"data": ["A", "B", "C"], "value": "b"}, False),
        ({"data": [1, 2, 3], "value": "2"}, False),
        ({"data": [1, 2, None], "value": None}, False), # example in docs shows "True" as a return, but description states "False"
        ({"data": [[1, 2], [3, 4]], "value": [1, 2]}, False),
        ({"data": [[1, 2], [3, 4]], "value": 2}, False),
        ({"data": [{"a": "b"}, {"c": "d"}], "value": {"a": "b"}}, False),
        ({"data": ["12:23:54", "13.1.2022", "5/28/2013 10:30:15 AM"], "value": "13.1.2022"}, True),
        ({"data": ["12:23:54", "13.1.2022", "5/28/2013 10:30:15 AM"], "value": "13.1.2022+00:00"}, False),
        ({"data": [1, 2, 3], "value": "2"}, False),
        ({"data": ["1", "2", "3"], "value": 2}, False),
    ],
)
def test_array_contains(array_contains_process_code, example_input, expected_output):
    output = run_process(array_contains_process_code, "array_contains", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [1, 2, 3], "value": 2}, False, None),
        ({"value": 2}, True, "Mandatory argument `data` is either null or not defined."),
        ({"data": None, "value": 2}, True, "Mandatory argument `data` is either null or not defined."),
        ({"data": [1, 2, 3]}, True, "Mandatory argument `value` is not defined."),
        ({"data": "[1,2,3]", "value": 2}, True, "Argument `data` is not an array."),
    ],
)
def test_array_contains_exceptions(array_contains_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(array_contains_process_code, "array_contains", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(array_contains_process_code, "array_contains", example_input)
