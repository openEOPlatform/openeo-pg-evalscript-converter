import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def sgn_process_code():
    return load_process_code("sgn")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [({"x": -2}, -1), ({"x": 3.5}, 1), ({"x": 0}, 0), ({"x": None}, None)],
)
def test_sgn(sgn_process_code, example_input, expected_output):
    output = run_process(sgn_process_code, "sgn", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 1}, False, None),
        ({"x": True}, True, "Argument `x` is not a number."),
        ({"y": 1}, True, "Mandatory argument `x` is not defined."),
    ],
)
def test_sgn_exceptions(sgn_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(sgn_process_code, "sgn", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(sgn_process_code, "sgn", example_input)
