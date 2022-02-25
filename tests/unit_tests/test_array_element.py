import json

import pytest

from tests.utils import load_process_code, run_process, run_process_with_additional_js_code


@pytest.fixture
def array_element_process_code():
    return load_process_code("array_element")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [9, 8, 7, 6, 5], "index": 2}, 7),
        ({"data": ["A", "B", "C"], "index": 0}, "A"),
        ({"data": [], "index": 0, "return_nodata": True}, None),
        ({"data": [1, 2, 3], "labels": ["one", "two", "three"], "label": "two"}, 2),
        ({"data": [1, 2, 3], "labels": ["one", "two", "three"], "label": "four", "return_nodata": True}, None),
        ({"data": [5, "ABC", True, None], "index": 0}, 5),
        ({"data": [5, "ABC", True, None], "index": 1, "return_nodata": True}, "ABC"),
        ({"data": [5, "ABC", True, None], "labels": ["number", "string", "bool", "null"], "label": "bool"}, True),
        ({"data": [5, "ABC", True, None], "labels": ["number", "string", "bool", "null"], "label": "null"}, None),
        (
            {
                "data": [5, "ABC", True, None],
                "labels": ["number", "string", "bool", "null"],
                "label": "True",
                "return_nodata": True,
            },
            None,
        ),
        ({"data": [5, "ABC", {"name": "John", "age": 27}, [1, True, False, None]], "index": 3}, [1, True, False, None]),
    ],
)
def test_array_element(array_element_process_code, example_input, expected_output):
    additional_js_code_to_run = f"const d = {json.dumps(example_input['data'])}; d.labels = {json.dumps(example_input['labels']) if 'labels' in example_input else 'undefined'};"
    output = run_process_with_additional_js_code(
        array_element_process_code,
        "array_element",
        example_input,
        False,
        additional_js_code_to_run,
        additional_params_in_string="'data': d",
    )
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [9, 8, 7, 6, 5], "index": 2}, False, None),
        ({"index": 2}, True, "Mandatory argument `data` is either null or not defined."),
        (
            {"data": [1, 2, 3]},
            True,
            "The process `array_element` requires either the `index` or `labels` parameter to be set.",
        ),
        (
            {"data": [1, 2, 3], "index": 2, "label": "two"},
            True,
            "The process `array_element` only allows that either the `index` or the `labels` parameter is set.",
        ),
        ({"data": [1, 2, 3], "index": 4}, True, "The array has no element with the specified index or label."),
        (
            {"data": [1, 2, 3], "label": "two"},
            True,
            "The array is not a labeled array, but the `label` parameter is set. Use the `index` instead.",
        ),
        (
            {"data": [1, 2, 3], "labels": ["one", "two", "three"], "label": "four"},
            True,
            "The array has no element with the specified index or label.",
        ),
        ({"data": ["A", "B", "C"], "index": "0"}, True, "Argument `index` is not an integer."),
        ({"data": ["A", "B", "C"], "index": 1.2}, True, "Argument `index` is not an integer."),
        (
            {"data": [1, 2, 3], "labels": ["one", "two", "three"], "label": ["two"]},
            True,
            "Argument `label` is not a string or a number.",
        ),
    ],
)
def test_array_element_exceptions(array_element_process_code, example_input, raises_exception, error_message):
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(array_element_process_code, "array_element", example_input)
        assert error_message in str(exc.value)

    else:
        run_process(array_element_process_code, "array_element", example_input)
