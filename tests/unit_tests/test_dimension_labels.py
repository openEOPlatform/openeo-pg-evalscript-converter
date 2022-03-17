import json

import pytest

from tests.utils import load_process_code, load_datacube_code, run_process


@pytest.fixture
def dimension_labels_process_code():
    return load_process_code("dimension_labels")


@pytest.mark.parametrize(
    "data,dimension,additional_js_code_specific_to_case,expected_output",
    [
        (
            [{"B01": 1, "B02": 2, "B03": 3}, {"B01": 4, "B02": 5, "B03": 6}],
            "bands_name",
            None,
            ["B01", "B02", "B03"],
        ),
        ([{"B01": 1, "B02": 2, "B03": 3}, {"B01": 4, "B02": 5, "B03": 6}], "temporal_name", None, []),
        (
            [{"B01": 1, "B02": 2, "B03": 3}, {"B01": 4, "B02": 5, "B03": 6}],
            "temporal_name",
            "cube.getDimensionByName('temporal_name').labels = ['test1', 'test2', 'test3'];",
            ["test1", "test2", "test3"],
        ),
    ],
)
def test_dimension_labels(
    dimension_labels_process_code, data, dimension, additional_js_code_specific_to_case, expected_output
):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube = new DataCube({data}, 'bands_name', 'temporal_name', true);"
        + (additional_js_code_specific_to_case or "")
    )
    process_arguments = f"{{'data': cube, 'dimension': '{dimension}'}}"
    output = run_process(
        dimension_labels_process_code + additional_js_code_to_run,
        "dimension_labels",
        process_arguments,
    )
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "data,dimension,additional_js_code_specific_to_case,raises_exception,error_message",
    [
        (
            [{"B01": 1, "B02": 2, "B03": 3}, {"B01": 4, "B02": 5, "B03": 6}],
            "bands_name",
            None,
            False,
            None,
        ),
        (
            [{"B01": 1, "B02": 2, "B03": 3}, {"B01": 4, "B02": 5, "B03": 6}],
            "bands_name",
            "cube = undefined;",
            True,
            "Mandatory argument `data` is not defined.",
        ),
        (
            [{"B01": 1, "B02": 2, "B03": 3}, {"B01": 4, "B02": 5, "B03": 6}],
            None,
            None,
            True,
            "Mandatory argument `dimension` is not defined.",
        ),
        (
            [{"B01": 1, "B02": 2, "B03": 3}, {"B01": 4, "B02": 5, "B03": 6}],
            123,
            None,
            True,
            "Argument `dimension` is not a string.",
        ),
        (
            [{"B01": 1, "B02": 2, "B03": 3}, {"B01": 4, "B02": 5, "B03": 6}],
            "fake_name",
            None,
            True,
            "A dimension with the specified name does not exist.",
        ),
        (
            [{"B01": 1, "B02": 2, "B03": 3}, {"B01": 4, "B02": 5, "B03": 6}],
            "bands_name",
            "cube.getDimensionByName('bands_name').labels = undefined;",
            True,
            "Dimension is missing attribute labels.",
        ),
        (
            [{"B01": 1, "B02": 2, "B03": 3}, {"B01": 4, "B02": 5, "B03": 6}],
            "bands_name",
            "cube.getDimensionByName('bands_name').labels = '[]';",
            True,
            "Dimension labels is not an array.",
        ),
    ],
)
def test_dimension_labels_exceptions(
    dimension_labels_process_code, data, dimension, additional_js_code_specific_to_case, raises_exception, error_message
):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube = new DataCube({data}, 'bands_name', 'temporal_name', true);"
        + (additional_js_code_specific_to_case or "")
    )
    process_arguments = f"{{'data': cube, 'dimension': '{dimension}'}}"
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(
                dimension_labels_process_code + additional_js_code_to_run,
                "dimension_labels",
                process_arguments,
            )
        assert error_message in str(exc.value)

    else:
        run_process(
            dimension_labels_process_code + additional_js_code_to_run,
            "dimension_labels",
            process_arguments,
        )
