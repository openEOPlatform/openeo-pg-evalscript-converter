import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def count_process_code():
    return load_process_code("count")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": []}, 0),
        ({"data": [False, None, 12, "string", {"name": "John"}], "condition": True}, 5),
    ],
)
def test_count(count_process_code, example_input, expected_output):
    output = run_process(count_process_code, "count", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [False, None, 12, "string", {"name": "John"}], "condition": True}, False, None),
        ({"data_fake": [1, 0, 3, 2]}, True, "Mandatory argument `data` is not defined."),
        ({"data": "[1,0,3,2]"}, True, "Argument `data` is not an array."),
        (
            {"data": [1, 0, 3, 2], "condition": [1, 2, 3]},
            True,
            "Argument `condition` is not a boolean, object or null.",
        ),
        (
            {"data": [1, 0, 3, 2], "condition": 12},
            True,
            "Argument `condition` is not a boolean, object or null.",
        ),
    ],
)
def test_count_exceptions(count_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(count_process_code, "count", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(count_process_code, "count", example_input)