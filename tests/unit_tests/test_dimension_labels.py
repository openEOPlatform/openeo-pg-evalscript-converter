import json

import pytest

from tests.utils import load_process_code, load_datacube_code, run_process_with_additional_js_code


@pytest.fixture
def dimension_labels_process_code():
    return load_process_code("dimension_labels")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        (
            {"data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]}, "dimension": "bands_name"},
            ["B01", "B02", "B03"],
        ),
        ({"data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]}, "dimension": "temporal_name"}, []),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "dimension": "temporal_name",
                "additional_js_code_specific_to_case": "cube.getDimensionByName('temporal_name').labels = ['test1', 'test2', 'test3'];",
            },
            ["test1", "test2", "test3"],
        ),
    ],
)
def test_dimension_labels(dimension_labels_process_code, example_input, expected_output):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube = new DataCube({example_input['data']}, 'bands_name', 'temporal_name', true);"
        + f"{example_input['additional_js_code_specific_to_case'] if 'additional_js_code_specific_to_case' in example_input else ''}"
    )
    process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube}}"
    output = run_process_with_additional_js_code(
        dimension_labels_process_code,
        "dimension_labels",
        process_arguments,
        additional_js_code_to_run,
    )
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        (
            {"data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]}, "dimension": "bands_name"},
            False,
            None,
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "dimension": "bands_name",
                "additional_js_code_specific_to_case": "cube = undefined;",
            },
            True,
            "Mandatory argument `data` is not defined.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
            },
            True,
            "Mandatory argument `dimension` is not defined.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "dimension": 123,
            },
            True,
            "Argument `dimension` is not a string.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "dimension": "fake_name",
            },
            True,
            "A dimension with the specified name does not exist.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "dimension": "bands_name",
                "additional_js_code_specific_to_case": "cube.getDimensionByName('bands_name').labels = undefined;",
            },
            True,
            "Dimension is missing attribute labels.",
        ),
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "dimension": "bands_name",
                "additional_js_code_specific_to_case": "cube.getDimensionByName('bands_name').labels = '[]';",
            },
            True,
            "Dimension labels is not an array.",
        ),
    ],
)
def test_dimension_labels_exceptions(dimension_labels_process_code, example_input, raises_exception, error_message):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube = new DataCube({example_input['data']}, 'bands_name', 'temporal_name', true);"
        + f"{example_input['additional_js_code_specific_to_case'] if 'additional_js_code_specific_to_case' in example_input else ''}"
    )
    process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube}}"
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process_with_additional_js_code(
                dimension_labels_process_code,
                "dimension_labels",
                process_arguments,
                additional_js_code_to_run,
            )
        assert error_message in str(exc.value)

    else:
        run_process_with_additional_js_code(
            dimension_labels_process_code,
            "dimension_labels",
            process_arguments,
            additional_js_code_to_run,
        )
