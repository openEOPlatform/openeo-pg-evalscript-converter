import json
import math

import pytest

from tests.utils import load_process_code, run_process, run_input_validation


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
        ({"x": 0.0, "y": -1}, -math.pi / 2),
        ({"x": 0.0, "y": 1}, math.pi / 2),
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
    "example_input,raises_exception,error_name",
    [
        ({"x": 0, "y": 0}, False, None),
        ({}, True, "MISSING_PARAMETER"),
        ({"z": 0.5}, True, "MISSING_PARAMETER"),
        ({"y": 0.5}, True, "MISSING_PARAMETER"),
        ({"x": 0.5}, True, "MISSING_PARAMETER"),
        ({"x": "0.5", "y": 0.5}, True, "WRONG_TYPE"),
        ({"x": 0.5, "y": "0.5"}, True, "WRONG_TYPE"),
    ],
)
def test_arctan2_exceptions(arctan2_process_code, example_input, raises_exception, error_name):
    run_input_validation(arctan2_process_code, "arctan2", example_input, raises_exception, error_name)
