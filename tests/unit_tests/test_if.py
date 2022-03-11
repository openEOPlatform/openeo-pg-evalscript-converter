import json

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


@pytest.fixture
def if_process_code():
    return load_process_code("if")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"value": True, "accept": "A", "reject": "B"}, "A"),
        ({"value": False, "accept": "A", "reject": "B"}, "B"),
        ({"value": 3 ** 2 == 9, "accept": "equals", "reject": [1, 2, 3]}, "equals"),
        ({"value": None, "accept": "ABC", "reject": [1, 2, 3]}, [1, 2, 3]),
        ({"value": None, "accept": 1}, None),
        ({"value": False, "accept": 123}, None),
        ({"value": True, "accept": 4 ** 2}, 16),
    ],
)
def test_if(if_process_code, example_input, expected_output):
    output = run_process(if_process_code, "_if", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"value": True, "accept": "A", "reject": "B"}, False, None),
        ({"accept": "A", "reject": "B"}, True, "MISSING_PARAMETER"),
        ({"value": True, "reject": "B"}, True, "MISSING_PARAMETER"),
        ({"value": "True", "accept": "A", "reject": "B"}, True, "NOT_BOOLEAN"),
    ],
)
def test_if_exceptions(if_process_code, example_input, raises_exception, error_message):
    run_input_validation(if_process_code, "_if", example_input, raises_exception, error_message)
