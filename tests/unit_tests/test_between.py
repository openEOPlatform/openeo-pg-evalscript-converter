import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def between_process_code():
    return load_process_code("between")


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({}, True, "Process between requires argument x"),
        ({"x": None}, False, None),
        ({"x": 0.3, "min": 0, "max": 1}, False, None),
        ({"x": 0.3, "min": 0, "max": 1, "exclude_max": False}, False, None),
        ({"x": 0.3}, True, "Process between requires argument min."),
        ({"x": 0.3, "max": 1}, True, "Process between requires argument min."),
        ({"x": 0.3, "min": 0}, True, "Process between requires argument max."),
        ({"x": 0.3, "min": None, "max": 1}, True, "Process between requires argument min."),
        ({"x": 0.3, "min": 1, "max": None}, True, "Process between requires argument max."),
        (
            {"x": 0.3, "min": None, "max": None},
            True,
            "Process between requires argument min.",
        ),
    ],
)
def test_between_inputs(between_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(between_process_code, "between", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(between_process_code, "between", example_input)


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": None, "min": 0, "max": 1}, None),
        ({"x": 1, "min": 0, "max": 1}, True),
        ({"x": 1, "min": 0, "max": 1, "exclude_max": True}, False),
        ({"x": 0.5, "min": 1, "max": 0}, False),
        ({"x": -0.5, "min": -1, "max": 0}, True),
        ({"x": "2018-07-23T17:22:45Z", "min": "2018-01-01T00:00:00Z", "max": "2018-12-31T23:59:59Z"}, True),
        ({"x": "2000-01-01", "min": "2018-01-01", "max": "2020-01-01"}, False),
        ({"x": "2018-12-31T17:22:45Z", "min": "2018-01-01T00:00:00Z", "max": "2018-12-31T23:59:59Z"}, True),
        # YYYY-MM-DD represents a whole day
        ({"x": "2018-12-31T17:22:45Z", "min": "2018-01-01", "max": "2018-12-31"}, True),
        ({"x": "2018-12-31T17:22:45Z", "min": "2018-01-01", "max": "2018-12-30"}, False),
        ({"x": "2018-12-31T17:22:45Z", "min": "2018-01-01", "max": "2019-01-01"}, True),
        ({"x": "2018-12-31T17:22:45Z", "min": "2018-01-01", "max": "2018-12-31", "exclude_max": True}, False),
        ({"x": "2018-12-31T17:22:45Z", "min": "2018-01-01", "max": "2019-01-01", "exclude_max": True}, True),
        ({"x": "2018-12-31", "min": "2018-01-01", "max": "2018-12-31"}, True),
        ({"x": "2018-12-31", "min": "2018-01-01", "max": "2018-12-31", "exclude_max": True}, False),
        ({"x": "2018-12-31", "min": "2018-01-01", "max": "2018-12-30"}, False),
        ({"x": "2018-12-31", "min": "2018-12-31", "max": "2018-12-31"}, True),
        ({"x": "2018-12-31", "min": "2018-12-31", "max": "2018-12-31", "exclude_max": True}, False),
        # TODO handle time-strings
        # ({"x": "00:59:59Z", "min": "01:00:00+01:00", "max": "01:00:00Z"}, True),  # 5
    ],
)
def test_between(between_process_code, example_input, expected_output):
    output = run_process(between_process_code, "between", example_input)
    output = json.loads(output)
    assert output == expected_output
