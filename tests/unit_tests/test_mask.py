import json

import pytest
import subprocess

from tests.utils import load_process_code, load_datacube_code, run_process, run_input_validation


@pytest.fixture
def mask_process_code():
    return load_process_code("mask")


@pytest.fixture
def construct_datacube():
    def wrapped(cube_name, data, data_shape, dimensions):
        return (
            f"\nconst {cube_name} = new DataCube(ndarray({json.dumps(data)}, {json.dumps(data_shape)}), 'b', 't', false);"
            + f"\n{cube_name}.dimensions = {json.dumps(dimensions)};"
        )

    return wrapped


@pytest.mark.parametrize(
    "data_array, data_shape, data_dimensions, mask_array, mask_shape, mask_dimensions, replacement, expected_array",
    [
        (  # test different mask values: mask with number values
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {"labels": ["2022-03-21", "2022-03-19", "2022-03-16"],"name": "t","type": "temporal"},
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            [0, 2, 0, 11, 0, 13, 0, 22, 0],
            [3, 3],
            [
                {"labels": ["2022-03-21", "2022-03-19", "2022-03-16"],"name": "t","type": "temporal"},
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            None,
            [1, None, 3, None, 12, None, 21, None, 23],
        ),
        (  # test different mask values: mask with boolean values
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {"labels": ["2022-03-21", "2022-03-19", "2022-03-16"],"name": "t","type": "temporal"},
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            [False, True, False, True, False, True, False, True, False],
            [3, 3],
            [
                {"labels": ["2022-03-21", "2022-03-19", "2022-03-16"],"name": "t","type": "temporal"},
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            None,
            [1, None, 3, None, 12, None, 21, None, 23],
        ),
        (  # test different replacement values: replacement = number
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {"labels": ["2022-03-21", "2022-03-19", "2022-03-16"],"name": "t","type": "temporal"},
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            [0, 2, 0, 11, 0, 13, 0, 22, 0],
            [3, 3],
            [
                {"labels": ["2022-03-21", "2022-03-19", "2022-03-16"],"name": "t","type": "temporal"},
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            42,
            [1, 42, 3, 42, 12, 42, 21, 42, 23],
        ),
        (  # test different replacement values: replacement = boolean
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {"labels": ["2022-03-21", "2022-03-19", "2022-03-16"],"name": "t","type": "temporal"},
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            [0, 2, 0, 11, 0, 13, 0, 22, 0],
            [3, 3],
            [
                {"labels": ["2022-03-21", "2022-03-19", "2022-03-16"],"name": "t","type": "temporal"},
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            True,
            [1, True, 3, True, 12, True, 21, True, 23],
        ),
        (  # test different replacement values: replacement = string
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {"labels": ["2022-03-21", "2022-03-19", "2022-03-16"],"name": "t","type": "temporal"},
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            [0, 2, 0, 11, 0, 13, 0, 22, 0],
            [3, 3],
            [
                {"labels": ["2022-03-21", "2022-03-19", "2022-03-16"],"name": "t","type": "temporal"},
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            "qwe",
            [1, "qwe", 3, "qwe", 12, "qwe", 21, "qwe", 23],
        ),
        (  # test mask parameter missing dimensions: mask parameter with no temporal dimension
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {"labels": ["2022-03-21", "2022-03-19", "2022-03-16"],"name": "t","type": "temporal"},
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            [0, 2, 0],
            [3],
            [{"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"}],
            None,
            [1, None, 3, 11, None, 13, 21, None, 23],
        ),
        (  # test mask parameter missing dimensions: mask parameter with no bands dimension
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {"labels": ["2022-03-21", "2022-03-19", "2022-03-16"],"name": "t","type": "temporal"},
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            [0, 11, 0],
            [3],
            [
                {"labels": ["2022-03-21", "2022-03-19", "2022-03-16"],"name": "t","type": "temporal"}
            ],
            None,
            [1, 2, 3, None, None, None, 21, 22, 23],
        ),
        (  # test mask parameter missing dimensions: data parameter with additional dimension
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [1, 3, 3],
            [
                {"labels": [], "name": "test_name", "type": "other"},
                {"labels": ["2022-03-21", "2022-03-19", "2022-03-16"],"name": "t","type": "temporal"},
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            [0, 2, 0, 11, 0, 13, 0, 22, 0],
            [3, 3],
            [
                {"labels": ["2022-03-21", "2022-03-19", "2022-03-16"],"name": "t","type": "temporal"},
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            None,
            [1, None, 3, None, 12, None, 21, None, 23],
        ),
        (  # test different order of dimensions in data and mask
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {"labels": ["2022-03-21", "2022-03-19", "2022-03-16"],"name": "t","type": "temporal"},
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            [0, 2, 0, 0, 12, 0, 0, 22, 0],
            [3, 3],
            [
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
                {"labels": ["2022-03-21", "2022-03-19", "2022-03-16"],"name": "t","type": "temporal"},
            ],
            None,
            [1, 2, 3, None, None, None, 21, 22, 23],
        ),
    ],
)
def test_mask(
    mask_process_code,
    construct_datacube,
    data_array,
    data_shape,
    data_dimensions,
    mask_array,
    mask_shape,
    mask_dimensions,
    replacement,
    expected_array,
):

    data_cube = construct_datacube("dataCube", data_array, data_shape, data_dimensions)
    mask_cube = construct_datacube("maskCube", mask_array, mask_shape, mask_dimensions)

    additional_js_code_to_run = load_datacube_code() + data_cube + mask_cube
    arguments = f"'data': dataCube, 'mask': maskCube"

    if replacement:
        additional_js_code_to_run = (
            additional_js_code_to_run
            + f"const replacement = {json.dumps(replacement)};"
        )
        arguments = arguments + f", 'replacement': {json.dumps(replacement)}"

    process_arguments = f"{{" + arguments + f"}}"

    output = run_process(
        additional_js_code_to_run + mask_process_code,
        "mask",
        process_arguments,
    )
    output = json.loads(output.decode("utf-8"))

    assert output["data"]["data"] == expected_array


@pytest.mark.parametrize(
    "data_array, data_shape, data_dimensions, mask_array, mask_shape, mask_dimensions, replacement, error_message",
    [
        (  # exception: wrong type of replacement
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {"labels": ["2022-03-21", "2022-03-19", "2022-03-16"],"name": "t","type": "temporal"},
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            [0, 2, 0, 11, 0, 13, 0, 22, 0],
            [3, 3],
            [
                {"labels": ["2022-03-21", "2022-03-19", "2022-03-16"],"name": "t","type": "temporal"},
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            [123, 123],
            "WRONG_TYPE: Value for replacement is not a number or a boolean or a string.",
        ),
        (  # exception: data doesn't have all dimensions that are in mask
            [1, 2, 3],
            [3],
            [{"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"}],
            [0, 2, 0, 11, 0, 13, 0, 22, 0],
            [3, 3],
            [
                {"labels": ["2022-03-21", "2022-03-19", "2022-03-16"],"name": "t","type": "temporal"},
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            None,
            "Error: Dimension `t` from argument `mask` not in argument `data`.",
        ),
        (  # exception: different types of dimension in data and mask
            [1, 2, 3],
            [3],
            [{"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"}],
            [0, 2, 0],
            [3],
            [{"labels": ["B01", "B02", "B03"], "name": "b", "type": "other"}],
            None,
            "Error: Type of the dimension `b` from argument `mask` is not the same as in argument `data`.",
        ),
        (  # exception: dimension has different labels in data and mask
            [1, 2, 3],
            [3],
            [{"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"}],
            [0, 2, 0],
            [3],
            [{"labels": ["B04", "B05", "B06"], "name": "b", "type": "bands"}],
            None,
            "Error: Labels for dimension `b` from argument `mask` are not the same as in argument `data`.",
        ),
    ],
)
def test_mask_exceptions(
    mask_process_code,
    construct_datacube,
    data_array,
    data_shape,
    data_dimensions,
    mask_array,
    mask_shape,
    mask_dimensions,
    replacement,
    error_message,
):
    data_cube = construct_datacube("dataCube", data_array, data_shape, data_dimensions)
    mask_cube = construct_datacube("maskCube", mask_array, mask_shape, mask_dimensions)

    additional_js_code_to_run = load_datacube_code() + data_cube + mask_cube

    arguments = f"'data': dataCube, 'mask': maskCube"

    if replacement:
        additional_js_code_to_run = (
            additional_js_code_to_run
            + f"const replacement = {json.dumps(replacement)};"
        )
        arguments = arguments + f", 'replacement': {json.dumps(replacement)}"

    process_arguments = f"{{" + arguments + f"}}"

    run_input_validation(
        additional_js_code_to_run + mask_process_code,
        "mask",
        process_arguments,
        True,
        error_message=error_message,
    )
