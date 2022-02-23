import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def sort_process_code():
    return load_process_code("sort")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [6, -1, 2, None, 7, 4, None, 8, 3, 9, 9]}, [-1, 2, 3, 4, 6, 7, 8, 9, 9]),
        ({"data": [6, -1, 2, None, 7, 4, None, 8, 3, 9, 9], "asc": False}, [9, 9, 8, 7, 6, 4, 3, 2, -1]),
        ({"data": [6, -1, 2, None, 7, 4, None, 8, 3, 9, 9], "nodata": True}, [-1, 2, 3, 4, 6, 7, 8, 9, 9, None, None]),
        (
            {"data": [6, -1, 2, None, 7, 4, None, 8, 3, 9, 9], "asc": False, "nodata": True},
            [9, 9, 8, 7, 6, 4, 3, 2, -1, None, None],
        ),
        ({"data": [6, -1, 2, None, 7, 4, None, 8, 3, 9, 9], "nodata": False}, [None, None, -1, 2, 3, 4, 6, 7, 8, 9, 9]),
        (
            {"data": [6, -1, 2, None, 7, 4, None, 8, 3, 9, 9], "asc": False, "nodata": False},
            [None, None, 9, 9, 8, 7, 6, 4, 3, 2, -1],
        ),
        ({"data": ["delta", None, "alpha", "charlie", None, "bravo"]}, ["alpha", "bravo", "charlie", "delta"]),
        (
            {"data": ["delta", None, "alpha", "charlie", None, "bravo"], "asc": False},
            ["delta", "charlie", "bravo", "alpha"],
        ),
        (
            {"data": ["delta", None, "alpha", "charlie", None, "bravo"], "nodata": True},
            ["alpha", "bravo", "charlie", "delta", None, None],
        ),
        (
            {"data": ["delta", None, "alpha", "charlie", None, "bravo"], "asc": False, "nodata": True},
            ["delta", "charlie", "bravo", "alpha", None, None],
        ),
        (
            {"data": ["delta", None, "alpha", "charlie", None, "bravo"], "nodata": False},
            [None, None, "alpha", "bravo", "charlie", "delta"],
        ),
        (
            {"data": ["delta", None, "alpha", "charlie", None, "bravo"], "asc": False, "nodata": False},
            [
                None,
                None,
                "delta",
                "charlie",
                "bravo",
                "alpha",
            ],
        ),
        (
            {"data": ["02-01-2022", None, "01-01-2022", "01-02-2021", "09-28-2022"]},
            ["01-02-2021", "01-01-2022", "02-01-2022", "09-28-2022"],
        ),
        (
            {"data": ["02-01-2022", None, "01-01-2022", "01-02-2021", "09-28-2022"], "asc": False},
            ["09-28-2022", "02-01-2022", "01-01-2022", "01-02-2021"],
        ),
        (
            {"data": ["02-01-2022", None, "01-01-2022", "01-02-2021", "09-28-2022"], "nodata": True},
            ["01-02-2021", "01-01-2022", "02-01-2022", "09-28-2022", None],
        ),
        (
            {"data": ["02-01-2022", None, "01-01-2022", "01-02-2021", "09-28-2022"], "nodata": False},
            [None, "01-02-2021", "01-01-2022", "02-01-2022", "09-28-2022"],
        ),
        (
            {
                "data": [
                    "2018-03-01T12:00:00+00:00",
                    None,
                    "2018-01-01T12:00:00+00:00",
                    "2019-01-01T12:00:00+00:00",
                    None,
                    "2018-01-01T12:01:00+00:00",
                ],
                "nodata": True,
            },
            [
                "2018-01-01T12:00:00+00:00",
                "2018-01-01T12:01:00+00:00",
                "2018-03-01T12:00:00+00:00",
                "2019-01-01T12:00:00+00:00",
                None,
                None,
            ],
        ),
        (
            {
                "data": [
                    "2018-03-01T12:00:00+00:00",
                    None,
                    "2018-01-01T12:00:00+00:00",
                    "2019-01-01T12:00:00+00:00",
                    None,
                    "2018-01-01T12:01:00+00:00",
                ],
                "nodata": True,
                "asc": False,
            },
            [
                "2019-01-01T12:00:00+00:00",
                "2018-03-01T12:00:00+00:00",
                "2018-01-01T12:01:00+00:00",
                "2018-01-01T12:00:00+00:00",
                None,
                None,
            ],
        ),
        ({"data": [None, None, None]}, []),
        ({"data": [None, None, None], "nodata": True}, [None, None, None]),
        ({"data": [None, None, None], "nodata": False}, [None, None, None]),
    ],
)
def test_sort(sort_process_code, example_input, expected_output):
    output = run_process(sort_process_code, "sort", example_input)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [1, 2, 3, 4, 5], "asc": False, "nodata": True}, False, None),
        ({"data": "[1,2,3,4,5]", "asc": False, "nodata": True}, True, "Argument `data` is not an array."),
        ({"data": [1, 2, 3, 4, 5], "asc": "False", "nodata": True}, True, "Argument `asc` is not a boolean."),
        (
            {"data": [1, 2, 3, 4, 5], "asc": False, "nodata": "True"},
            True,
            "Argument `nodata` is not a boolean or null.",
        ),
        ({"data": [1, 2, [3], 4, 5], "asc": False, "nodata": True}, True, "Element in `data` is not of correct type."),
    ],
)
def test_sort_exceptions(sort_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(sort_process_code, "sort", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(sort_process_code, "sort", example_input)
