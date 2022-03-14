import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def array_labels_process_code():
    return load_process_code("array_labels")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"data": [1, 0, 3, 2], "labels": []}, []),
        ({"data": [1, 0, 3, 2], "labels": [1, 2, 3, 4]}, [1, 2, 3, 4]),
        ({"data": [1, 0, 3, 2], "labels": ["1", "2", "3", "4"]}, ["1", "2", "3", "4"]),
    ],
)
def test_array_labels(array_labels_process_code, example_input, expected_output):
    additional_js_code_to_run = (
        f"const d = {json.dumps(example_input['data'])};" + f"d.labels = {json.dumps(example_input['labels'])};"
    )
    process_arguments = f"{{'data': d, 'labels': {example_input['labels']}}}"
    output = run_process(
        array_labels_process_code + additional_js_code_to_run,
        "array_labels",
        process_arguments,
    )
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        ({"data": [1, 0, 3, 2], "labels": [1, 2, 3, 4]}, False, None),
        ({"data_fake": [1, 0, 3, 2]}, True, "Mandatory argument `data` is not defined."),
        ({"data": "[1,0,3,2]"}, True, "Argument `data` is not an array."),
        ({"data": [1, 0, 3, 2]}, True, "Argument `data` is not a labeled array."),
        ({"data": [1, 0, 3, 2], "labels": "[1,2,3,4]"}, True, "Labels in argument `data` is not an array."),
    ],
)
def test_array_labels_exceptions(array_labels_process_code, example_input, raises_exception, error_message):
    additional_js_code_to_run = (
        f"const d = {json.dumps(example_input['data'] if 'data' in example_input else 'undefined')};"
        + f"d.labels = {json.dumps(example_input['labels']) if 'labels' in example_input else 'undefined'};"
    )
    process_arguments = f"{{...{json.dumps(example_input)}, 'data': d}}"
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(
                array_labels_process_code + additional_js_code_to_run,
                "array_labels",
                process_arguments,
            )
        assert error_message in str(exc.value)

    else:
        run_process(
            array_labels_process_code + additional_js_code_to_run,
            "array_labels",
            process_arguments,
        )
