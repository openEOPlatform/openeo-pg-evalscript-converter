import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def if_process_code():
    return load_process_code("if")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"value": True, "accept": "A", "reject": "B"}, "A"),
        ({"value": False, "accept": "A", "reject": "B"}, "B"),
        ({"value": 3**2 == 9, "accept": "equals", "reject": [1, 2, 3]}, "equals"),
        ({"value": None, "accept": "ABC", "reject": [1, 2, 3]}, [1, 2, 3]),
        ({"value": None, "accept": 1}, None),
        ({"value": False, "accept": 123}, None),
        ({"value": True, "accept": 4**2}, 16),
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
        ({"accept": "A", "reject": "B"}, True, "Mandatory argument `value` is not defined."),
        ({"value": True, "reject": "B"}, True, "Mandatory argument `accept` is not defined."),
        ({"value": "True", "accept": "A", "reject": "B"}, True, "Argument `value` is not a boolean or null."),
    ],
)
def test_if_exceptions(if_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(if_process_code, "_if", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(if_process_code, "_if", example_input)
