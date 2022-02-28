import json
import math

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def cosh_process_code():
    return load_process_code("cosh")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 1),
        ({"x": 1}, 1.5430806348152437),
        ({"x": -1}, 1.5430806348152437),
        ({"x": None}, None),
    ],
)
def test_cosh(cosh_process_code, example_input, expected_output):
    output = run_process(cosh_process_code, "cosh", example_input)
    output = json.loads(output)
    assert pytest.approx(output) == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 0}, False, None),
        ({}, True, "Mandatory argument `x` is not defined."),
        ({"y": 0.5}, True, "Mandatory argument `x` is not defined."),
        ({"x": "0.5"}, True, "Argument `x` is not a number."),
    ],
)
def test_cosh_exceptions(
    cosh_process_code, example_input, raises_exception, error_message
):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(cosh_process_code, "cosh", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(cosh_process_code, "cosh", example_input)
