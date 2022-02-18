import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def last_process_code():
    return load_process_code("last")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": []}, None),
        ({"data": [1, 2, 3]}, 3),
        ({"data": [10, 0, 3, 2]}, 2),
        ({"data": ["A", "B", "C", None]}, "C"),
        ({"data": ["A", "B", "C", None], "ignore_nodata": False}, None),
        ({"data": [1, 2, 3, None]}, 3),
        ({"data": [1, 2, 3, None], "ignore_nodata": False}, None),
        ({"data": [[1, 2], [3, 4]]}, [3, 4]),
        ({"data": [None, 1, 2]}, 2),
        ({"data": [{"a": "b"}, {"c": "d"}]}, {"c": "d"}),
        ({"data": [None, None, None]}, None),
        ({"data": [None, None, None], "ignore_nodata": False}, None),
    ],
)
def test_last(last_process_code, example_input, expected_output):
    output = run_process(last_process_code, "last", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [10, 0, 3, 2]}, False, None),
        ({"data": None}, True, "Mandatory argument `data` is either null or not defined."),
        ({}, True, "Mandatory argument `data` is either null or not defined."),
    ],
)
def test_last_exceptions(last_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(last_process_code, "last", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(last_process_code, "last", example_input)
