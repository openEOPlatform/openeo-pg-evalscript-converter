import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def array_append_process_code():
    return load_process_code("array_append")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"array": [], "value": None}, [None]),
        ({"array": [1, 2], "value": 3}, [1, 2, 3]),
        ({"array": ["a"], "value": "b"}, ["a", "b"]),
        (
            {"array": [True], "value": "2020-01-01T00:00:00Z"},
            [True, "2020-01-01T00:00:00Z"],
        ),
    ],
)
def test_array_append(array_append_process_code, example_input, expected_output):
    output = run_process(array_append_process_code, "array_append", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"array": [1, 2], "value": [3]}, False, None),
        (
            {"value": 1},
            True,
            "Mandatory argument `array` is either null or not defined.",
        ),
        (
            {
                "array": [1],
            },
            True,
            "Mandatory argument `value` is not defined.",
        ),
        ({"array": "[0]", "value": 1}, True, "Argument `array` is not an array."),
    ],
)
def test_array_append_exceptions(
    array_append_process_code, example_input, raises_exception, error_message
):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(array_append_process_code, "array_append", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(array_append_process_code, "array_append", example_input)
