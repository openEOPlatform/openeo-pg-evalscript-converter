import json
import math

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def arctan_process_code():
    return load_process_code("arctan")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 0}, 0),  # arctan(0) = 0°
        ({"x": math.sqrt(3) / 3}, math.pi / 6),  # arctan(sqrt(3)/3) = 30°
        ({"x": 1}, math.pi / 4),  # arctan(1) = 45°
        ({"x": math.sqrt(3)}, math.pi / 3),  # arctan(sqrt(3)) = 60°
        ({"x": math.inf}, math.pi / 2),  # arctan(infinity) = 90°
        ({"x": -math.sqrt(3) / 3}, -math.pi / 6),  # arctan(-sqrt(3)/3) = -30°
        ({"x": -1}, -math.pi / 4),  # arctan(-1) = -45°
        ({"x": -math.sqrt(3)}, -math.pi / 3),  # arctan(-sqrt(3)) = -60°
        ({"x": -math.inf}, -math.pi / 2),  # arctan(-infinity) = -90°
        ({"x": None}, None),
    ],
)
def test_arctan(arctan_process_code, example_input, expected_output):
    output = run_process(arctan_process_code, "arctan", example_input)
    output = json.loads(output)
    assert expected_output == pytest.approx(output)


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 0}, False, None),
        ({}, True, "Mandatory argument `x` is not defined."),
        ({"y": 0.5}, True, "Mandatory argument `x` is not defined."),
        ({"x": "0.5"}, True, "Argument `x` is not a number."),
    ],
)
def test_arctan_exceptions(
    arctan_process_code, example_input, raises_exception, error_message
):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(arctan_process_code, "arctan", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(arctan_process_code, "arctan", example_input)
