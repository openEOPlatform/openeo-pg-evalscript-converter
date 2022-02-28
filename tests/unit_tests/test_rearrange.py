import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def rearrange_process_code():
    return load_process_code("rearrange")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [], "order": []}, []),
        ({"data": [None, None, None], "order": [0, 1, 2]}, [None, None, None]),
        ({"data": [1, None, None], "order": [1, 0]}, [None, 1]),
        ({"data": [5, 4, 3], "order": [2, 1, 0]}, [3, 4, 5]),
        ({"data": [5, 4, 3, 2], "order": [1, 3]}, [4, 2]),
        ({"data": [5, 4, 3, 2], "order": [0, 2, 1, 3]}, [5, 3, 4, 2]),
        (
            {"data": [False, "c", "b", "a", True], "order": [4, 3, 2, 1, 0]},
            [True, "a", "b", "c", False],
        ),
    ],
)
def test_rearrange(rearrange_process_code, example_input, expected_output):
    output = run_process(rearrange_process_code, "rearrange", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [1, 2], "order": [0, 1]}, False, None),
        (
            {"order": [0]},
            True,
            "Mandatory argument `data` is either null or not defined.",
        ),
        (
            {"data": [0]},
            True,
            "Mandatory argument `order` is either null or not defined.",
        ),
        (
            {"data": [1, 2], "order": [0, -1]},
            True,
            "Argument `order` must contain only integer values greater than or equal to 0.",
        ),
        (
            {"data": [1], "order": [1]},
            True,
            "Argument `order` contains an index which does not exist in argument `data`.",
        ),
    ],
)
def test_rearrange_exceptions(
    rearrange_process_code, example_input, raises_exception, error_message
):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(rearrange_process_code, "rearrange", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(rearrange_process_code, "rearrange", example_input)
