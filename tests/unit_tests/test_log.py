import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def log_process_code():
    return load_process_code("log")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({'x': 1, 'base': 10}, 0),
        ({'x': 2.718281828459045, 'base': 2.718281828459045}, 1),
        ({'x': None, 'base': 10}, None),
        ({'x': 4, 'base': None}, None),
        ({'x': 123, 'base': 2.718281828459045}, 4.812184355372417),
        ({'x': 10, 'base': 100}, 0.5),
        ({'x': 16, 'base': 2}, 4),
        ({'x': 1234, 'base': 17}, 2.512347409134643)
    ],
)
def test_log(log_process_code, example_input, expected_output):
    output = run_process(log_process_code, "log", example_input)
    output = json.loads(output)
    assert output == expected_output

@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({'x': 1, 'base': 10}, False, None),
        ({}, True, 'Mandatory argument `x` or `base` is not defined.'),
        ({'y': 0.5}, True, 'Mandatory argument `x` or `base` is not defined.'),
        ({'x': 0.5}, True, 'Mandatory argument `x` or `base` is not defined.'),
        ({'base': 10}, True, 'Mandatory argument `x` or `base` is not defined.'),
        ({'x': '0.5', 'base': 10}, True, 'Argument `x` is not a number.'),
        ({'x': 0.5, 'base': '10'}, True, 'Argument `base` is not a number.')
    ]
)
def test_log_exceptions(log_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(log_process_code, "log", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(log_process_code, "log", example_input)