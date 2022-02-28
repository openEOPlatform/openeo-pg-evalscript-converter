import json
import math

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def arcsin_process_code():
    return load_process_code("arcsin")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 0),  # arcsin(0) = 0°
        ({"x": 0.5}, math.pi / 6),  # arcsin(0.5) = 30°
        ({"x": math.sqrt(2) / 2}, math.pi / 4),  # arcsin(sqrt(2)/2) = 45°
        ({"x": math.sqrt(3) / 2}, math.pi / 3),  # arcsin(sqrt(3)/2 ) = 60°
        ({"x": 1}, math.pi / 2),  # arcsin(1) = 90°
        ({"x": -0.5}, -math.pi / 6),  # arcsin(-0.5) = -30°
        ({"x": -math.sqrt(2) / 2}, -math.pi / 4),  # arcsin(-sqrt(2)/2) = -45°
        ({"x": -math.sqrt(3) / 2}, -math.pi / 3),  # arcsin(-sqrt(3)/2 ) = -60°
        ({"x": -1}, -math.pi / 2),  # arcsin(-1) = -90°
        ({"x": None}, None),
    ],
)
def test_arcsin(arcsin_process_code, example_input, expected_output):
    output = run_process(arcsin_process_code, "arcsin", example_input)
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
def test_arcsin_exceptions(
    arcsin_process_code, example_input, raises_exception, error_message
):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(arcsin_process_code, "arcsin", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(arcsin_process_code, "arcsin", example_input)
