import json
import math

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def arccos_process_code():
    return load_process_code("arccos")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 1}, 0),  # arccos(1) = 0°
        ({"x": math.sqrt(3) / 2}, math.pi / 6),  # arccos(sqrt(3)/2) = 30°
        ({"x": math.sqrt(2) / 2}, math.pi / 4),  # arccos(sqrt(2)/2) = 45°
        ({"x": 0.5}, math.pi / 3),  # arccos(0.5) = 60°
        ({"x": 0}, math.pi / 2),  # arccos(0) = 90°
        ({"x": -1}, math.pi),  # arccos(-1) = 180°
        ({"x": None}, None),
    ],
)
def test_arccos(arccos_process_code, example_input, expected_output):
    output = run_process(arccos_process_code, "arccos", example_input)
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
def test_arccos_exceptions(
    arccos_process_code, example_input, raises_exception, error_message
):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(arccos_process_code, "arccos", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(arccos_process_code, "arccos", example_input)
