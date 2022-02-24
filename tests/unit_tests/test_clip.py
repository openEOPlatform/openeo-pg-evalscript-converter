import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def clip_process_code():
    return load_process_code("clip")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 1, "min": 0, "max": 2}, 1),
        ({"x": -5, "min": -1, "max": 1}, -1),
        ({"x": 10.001, "min": 1, "max": 10}, 10),
        ({"x": 0.00001, "min": 0, "max": 0.02}, 0.00001),
        ({"x": None, "min": 0, "max": 2}, None),
    ],
)
def test_clip(clip_process_code, example_input, expected_output):
    output = run_process(clip_process_code, "clip", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 1, "min": 0, "max": 2}, False, None),
        ({"min": 0, "max": 2}, True, "Mandatory argument `x` is not defined."),
        ({"x": 1, "max": 2}, True, "Mandatory argument `min` is not defined."),
        (
            {
                "x": 1,
                "min": 0,
            },
            True,
            "Mandatory argument `max` is not defined.",
        ),
        ({"x": "1", "min": 0, "max": 2}, True, "Argument `x` is not a number."),
        ({"x": 1, "min": "0", "max": 2}, True, "Argument `min` is not a number."),
        ({"x": 1, "min": 0, "max": "2"}, True, "Argument `max` is not a number."),
    ],
)
def test_clip_exceptions(clip_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(clip_process_code, "clip", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(clip_process_code, "clip", example_input)
