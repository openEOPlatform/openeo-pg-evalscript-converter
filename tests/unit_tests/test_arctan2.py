import json
import math

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def arctan2_process_code():
    return load_process_code("arctan2")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        # test generated from examples at
        # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/atan2
        # -0 has to be passed as a float so that the python handles it as a -0, not 0
        ({"x": 0.0, "y": 0.0}, 0.0),
        ({"x": -0.0, "y": 0.0}, math.pi),
        ({"x": -0.0, "y": -0.0}, -math.pi),
        ({"x": 0.0, "y": -0.0}, -0.0),
        ({"x": -1, "y": 0.0}, math.pi),
        ({"x": -1, "y": -0.0}, -math.pi),
        ({"x": 1, "y": 0.0}, 0.0),
        ({"x": 1, "y": -0.0}, -0.0),
        ({"x": 0.0, "y": -1}, -math.pi / 2),
        ({"x": -0.0, "y": -1}, -math.pi / 2),
        ({"x": 0.0, "y": 1}, math.pi / 2),
        ({"x": -0.0, "y": 1}, math.pi / 2),
        ({"x": -math.inf, "y": 1}, math.pi),
        ({"x": -math.inf, "y": -1}, -math.pi),
        ({"x": math.inf, "y": 1}, 0.0),
        ({"x": math.inf, "y": -1}, -0.0),
        ({"x": 1, "y": math.inf}, math.pi / 2),
        ({"x": 1, "y": -math.inf}, -math.pi / 2),
        ({"x": -math.inf, "y": math.inf}, 3 * math.pi / 4),
        ({"x": -math.inf, "y": -math.inf}, -3 * math.pi / 4),
        ({"x": math.inf, "y": math.inf}, math.pi / 4),
        ({"x": math.inf, "y": -math.inf}, -math.pi / 4),
        ({"x": 1, "y": None}, None),
        ({"x": None, "y": 1}, None),
        ({"x": None, "y": None}, None),
    ],
)
def test_arctan2(arctan2_process_code, example_input, expected_output):
    output = run_process(arctan2_process_code, "arctan2", example_input)
    output = json.loads(output)
    assert expected_output == pytest.approx(output)


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 0, "y": 0}, False, None),
        ({}, True, "Mandatory arguments `x` and `y` are not defined."),
        ({"z": 0.5}, True, "Mandatory arguments `x` and `y` are not defined."),
        ({"y": 0.5}, True, "Mandatory argument `x` is not defined."),
        ({"x": 0.5}, True, "Mandatory argument `y` is not defined."),
        ({"x": "0.5", "y": 0.5}, True, "Argument `x` is not a number."),
        ({"x": 0.5, "y": "0.5"}, True, "Argument `x` is not a number."),
    ],
)
def test_arctan2_exceptions(
    arctan2_process_code, example_input, raises_exception, error_message
):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(arctan2_process_code, "arctan2", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(arctan2_process_code, "arctan2", example_input)
