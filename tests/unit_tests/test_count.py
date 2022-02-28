import json

import pytest

from tests.utils import load_process_code, run_process_with_additional_js_code


@pytest.fixture
def count_process_code():
    return load_process_code("count")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": []}, 0),
        ({"data": [1, 0, 3, 2]}, 4),
        ({"data": ["ABC", None]}, 1),
        ({"data": [False, None], "condition": True}, 2),
        ({"data": [0, 1, 2, 3, 4, 5, None], "condition": "({x}) => x > 2"}, 3),
    ],
)
def test_count(count_process_code, example_input, expected_output):
    additional_js_code_to_run = (
        load_process_code("is_valid")
        + f"const cond = eval({json.dumps(example_input['condition']) if 'condition' in example_input else 'undefined'});"
    )
    output = run_process_with_additional_js_code(
        count_process_code,
        "count",
        example_input,
        additional_js_code_to_run,
        additional_params_in_string="'condition': cond",
    )
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [1, 0, 3, 2]}, False, None),
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
    additional_js_code_to_run = (
        load_process_code("is_valid")
        + f"const cond = eval({json.dumps(example_input['condition']) if 'condition' in example_input else 'undefined'});"
    )
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process_with_additional_js_code(
                count_process_code,
                "count",
                example_input,
                additional_js_code_to_run,
                additional_params_in_string="'condition': cond",
            )
        assert error_message in str(exc.value)

    else:
        run_process_with_additional_js_code(
            count_process_code,
            "count",
            example_input,
            additional_js_code_to_run,
            additional_params_in_string="'condition': cond",
        )
