import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def power_process_code():
    return load_process_code("power")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"p": 1, "base": 2}, 2),
        ({"p": 0, "base": 1234}, 1),
        ({"p": 2.718281828459045, "base": 2}, 6.5808859910179205),
        ({"p": None, "base": 2}, None),
        ({"p": 12, "base": None}, None),
        ({"p": 12, "base": 2}, 4096),
        ({"p": 0.5, "base": 4}, 2),
        ({"p": 7.54, "base": 0.5}, 0.0053732102271083736),
        ({"p": 29, "base": -1}, -1),
        ({"p": 30, "base": -1}, 1),
        ({"p": 2, "base": 0}, 0),
    ],
)
def test_power(power_process_code, example_input, expected_output):
    output = run_process(power_process_code, "power", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"p": 1, "base": 2}, False, None),
        ({}, True, "Mandatory argument `p` or `base` is not defined."),
        ({"p": 2}, True, "Mandatory argument `p` or `base` is not defined."),
        ({"base": 3}, True, "Mandatory argument `p` or `base` is not defined."),
        ({"q": 0.5, "base": 12}, True, "Mandatory argument `p` or `base` is not defined."),
        ({"p": "0.5", "base": 1}, True, "Argument `p` is not a number."),
        ({"p": {"p": 0.5}, "base": 4}, True, "Argument `p` is not a number."),
        ({"p": 12, "base": "3"}, True, "Argument `base` is not a number."),
        ({"p": 2, "base": {"base": 4}}, True, "Argument `base` is not a number."),
    ],
)
def test_power_exceptions(power_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(power_process_code, "power", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(power_process_code, "power", example_input)
