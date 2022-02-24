import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def not_process_code():
    return load_process_code("not")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [({"x": None}, None), ({"x": True}, False), ({"x": False}, True)],
)
def test_not(not_process_code, example_input, expected_output):
    output = run_process(not_process_code, "not", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": True}, False, None),
        ({}, True, "Mandatory argument `x` is not defined."),
        ({"y": True}, True, "Mandatory argument `x` is not defined."),
        ({"x": "True"}, True, "Argument `x` is not a boolean."),
    ],
)
def test_not_exceptions(not_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(not_process_code, "not", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(not_process_code, "not", example_input)
