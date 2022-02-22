import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def mod_process_code():
    return load_process_code("mod")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 27, "y": 5}, 2),
        ({"x": -27, "y": 5}, 2),
        ({"x": 3.14, "y": -2}, -1.14),
        ({"x": -27, "y": -5}, -2),
        ({"x": -3, "y": -1}, -0),
        ({"x": 3, "y": -2}, -1),
        ({"x": 3, "y": 4}, 3),
        ({"x": None, "y": 3}, None),
        ({"x": 1, "y": None}, None),
        ({"x": None, "y": None}, None)
    ],
)
def test_mod(mod_process_code, example_input, expected_output):
    output = run_process(mod_process_code, "mod", example_input)
    output = json.loads(output)
    assert pytest.approx(output) == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"x": 1, "y": 2}, False, None),
        ({"x": 2, "y": 0}, True, "Division by zero is not supported."),
        ({"x": 1}, True, "Mandatory argument `y` is not defined."),
        ({"y": 1}, True, "Mandatory argument `x` is not defined."),
        ({"x": "1", "y": 2}, True, "Argument `x` is not a number."),
        ({"x": 1, "y": {"name": "John", "surname": "Doe"}}, True, "Argument `y` is not a number."),
    ],
)
def test_mod_exceptions(mod_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(mod_process_code, "mod", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(mod_process_code, "mod", example_input)
