import json

import pytest
import subprocess

from tests.utils import (
    load_process_code,
    load_dependency_processes_code,
    load_datacube_code,
    run_process,
    run_input_validation,
)


@pytest.fixture
def resample_cube_temporal_process_code():
    process_code = load_process_code("resample_cube_temporal")
    dependency_processes_code = load_dependency_processes_code(["is_valid"])
    return process_code + dependency_processes_code


@pytest.fixture
def construct_datacube():
    def wrapped(cube_name, data, data_shape, dimensions):
        return (
            f"\nconst {cube_name} = new DataCube(ndarray({json.dumps(data)}, {json.dumps(data_shape)}), 'b', 't', false);"
            + f"\n{cube_name}.dimensions = {json.dumps(dimensions)};"
        )

    return wrapped


@pytest.mark.parametrize(
    "data_array, data_shape, data_dimensions, target_array, target_shape, target_dimensions, dimension, valid_within, expected_array, expected_shape, expected_dimensions",
    [
        # bands:  B1, B2, B3
        # date 1:  1,  2,  3,
        # date 2: 11, 12, 13,
        # date 3: 21, 22, 23
        (  # same dates
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {
                    "labels": ["2022-03-21", "2022-03-19", "2022-03-16"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {
                    "labels": ["2022-03-21", "2022-03-19", "2022-03-16"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            None,
            None,
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {
                    "labels": ["2022-03-21", "2022-03-19", "2022-03-16"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
        ),
        (  # same size of temporal dimension, but different dates
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {
                    "labels": ["2022-03-21", "2022-03-19", "2022-03-16"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {
                    "labels": ["2022-03-22", "2022-03-17", "2022-03-15"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            None,
            None,
            [1, 2, 3, 21, 22, 23, 21, 22, 23],
            [3, 3],
            [
                {
                    "labels": ["2022-03-22", "2022-03-17", "2022-03-15"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
        ),
        (  # resample to less dates - downsample
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {
                    "labels": ["2022-03-21", "2022-03-19", "2022-03-16"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            [1, 2, 3, 11, 12, 13],
            [2, 3],
            [
                {
                    "labels": ["2022-03-20", "2022-03-17"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            None,
            None,
            [11, 12, 13, 21, 22, 23],
            [2, 3],
            [
                {
                    "labels": ["2022-03-20", "2022-03-17"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
        ),
        (  # resample to more dates - upsample
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {
                    "labels": ["2022-03-21", "2022-03-19", "2022-03-16"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            [1, 2, 3, 11, 12, 13, 21, 22, 23, 31, 32, 33],
            [4, 3],
            [
                {
                    "labels": ["2022-03-22", "2022-03-20", "2022-03-18", "2022-03-15"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            None,
            None,
            [1, 2, 3, 11, 12, 13, 11, 12, 13, 21, 22, 23],
            [4, 3],
            [
                {
                    "labels": ["2022-03-22", "2022-03-20", "2022-03-18", "2022-03-15"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
        ),
        (  # target has different order of dimension
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {
                    "labels": ["2022-03-21", "2022-03-19", "2022-03-16"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-03-21", "2022-03-19", "2022-03-16"],
                    "name": "t",
                    "type": "temporal",
                },
            ],
            None,
            None,
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {
                    "labels": ["2022-03-21", "2022-03-19", "2022-03-16"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
        ),
        # data has temporal dimension in a different location
        # bands: B1, B2, B3
        # date 1: 1, 11, 21
        # date 2: 2, 12, 22
        # date 3: 3, 13, 23
        (  # same dates; data has different order of dimensions
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-03-21", "2022-03-19", "2022-03-16"],
                    "name": "t",
                    "type": "temporal",
                },
            ],
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {
                    "labels": ["2022-03-21", "2022-03-19", "2022-03-16"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            None,
            None,
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-03-21", "2022-03-19", "2022-03-16"],
                    "name": "t",
                    "type": "temporal",
                },
            ],
        ),
        (  # same size of temporal dimension, but different dates; data has different order of dimensions
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-03-21", "2022-03-19", "2022-03-16"],
                    "name": "t",
                    "type": "temporal",
                },
            ],
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {
                    "labels": ["2022-03-22", "2022-03-17", "2022-03-15"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            None,
            None,
            [1, 3, 3, 11, 13, 13, 21, 23, 23],
            [3, 3],
            [
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-03-22", "2022-03-17", "2022-03-15"],
                    "name": "t",
                    "type": "temporal",
                },
            ],
        ),
        (  # resample to less dates - downsample; data has different order of dimensions
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-03-21", "2022-03-19", "2022-03-16"],
                    "name": "t",
                    "type": "temporal",
                },
            ],
            [1, 2, 3, 11, 12, 13],
            [2, 3],
            [
                {
                    "labels": ["2022-03-20", "2022-03-17"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            None,
            None,
            [2, 3, 12, 13, 22, 23],
            [3, 2],
            [
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-03-20", "2022-03-17"],
                    "name": "t",
                    "type": "temporal",
                },
            ],
        ),
        (  # resample to more dates - upsample; data has different order of dimensions
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-03-21", "2022-03-19", "2022-03-16"],
                    "name": "t",
                    "type": "temporal",
                },
            ],
            [1, 2, 3, 11, 12, 13, 21, 22, 23, 31, 32, 33],
            [4, 3],
            [
                {
                    "labels": ["2022-03-22", "2022-03-20", "2022-03-18", "2022-03-15"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            None,
            None,
            [1, 2, 2, 3, 11, 12, 12, 13, 21, 22, 22, 23],
            [3, 4],
            [
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-03-22", "2022-03-20", "2022-03-18", "2022-03-15"],
                    "name": "t",
                    "type": "temporal",
                },
            ],
        ),
        (  # same size of temporal dimension, but different dates; dimension is set
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {
                    "labels": ["2022-03-21", "2022-03-19", "2022-03-16"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {
                    "labels": ["2022-03-22", "2022-03-17", "2022-03-15"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            "t",
            None,
            [1, 2, 3, 21, 22, 23, 21, 22, 23],
            [3, 3],
            [
                {
                    "labels": ["2022-03-22", "2022-03-17", "2022-03-15"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
        ),
        (  # 2 temporal dimensions; dimension is set to t
            [1, 2, 3, 4, 5, 6, 7, 8],
            [2, 2, 2],
            [
                {
                    "labels": ["2022-03-21", "2022-03-10"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-01-01", "2022-02-01"],
                    "name": "additional_t",
                    "type": "temporal",
                },
            ],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [2, 2, 2],
            [
                {
                    "labels": ["2022-03-22", "2022-03-17"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-01-01", "2022-02-01"],
                    "name": "additional_t",
                    "type": "temporal",
                },
            ],
            "t",
            None,
            [1, 2, 3, 4, 1, 2, 3, 4],
            [2, 2, 2],
            [
                {
                    "labels": ["2022-03-22", "2022-03-17"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-01-01", "2022-02-01"],
                    "name": "additional_t",
                    "type": "temporal",
                },
            ],
        ),
        (  # 2 temporal dimensions; dimension is set to additional_t
            [1, 2, 3, 4, 5, 6, 7, 8],
            [2, 2, 2],
            [
                {
                    "labels": ["2022-03-21", "2022-03-10"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-01-01", "2022-02-01"],
                    "name": "additional_t",
                    "type": "temporal",
                },
            ],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [2, 2, 2],
            [
                {
                    "labels": ["2022-03-15", "2022-03-10"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-01-25", "2022-02-01"],
                    "name": "additional_t",
                    "type": "temporal",
                },
            ],
            "additional_t",
            None,
            [2, 2, 6, 6, 4, 4, 8, 8],
            [2, 2, 2],
            [
                {
                    "labels": ["2022-03-21", "2022-03-10"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-01-25", "2022-02-01"],
                    "name": "additional_t",
                    "type": "temporal",
                },
            ],
        ),
        (  # same size of temporal dimension, but different dates; dimension's labels in different orders
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {
                    "labels": ["2022-03-21", "2022-03-19", "2022-03-16"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            [1, 2, 3, 11, 12, 13, 21, 22, 23],
            [3, 3],
            [
                {
                    "labels": ["2022-03-15", "2022-03-17", "2022-03-22"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
            None,
            None,
            [21, 22, 23, 21, 22, 23, 1, 2, 3],
            [3, 3],
            [
                {
                    "labels": ["2022-03-15", "2022-03-17", "2022-03-22"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02", "B03"], "name": "b", "type": "bands"},
            ],
        ),
        (  # 2 temporal dimensions; resample both
            [1, 2, 3, 4, 5, 6, 7, 8],
            [2, 2, 2],
            [
                {
                    "labels": ["2022-03-21", "2022-03-10"],
                    "name": "t",
                    "type": "temporal",
                },
                {
                    "labels": ["2022-01-01", "2022-02-01"],
                    "name": "additional_t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02"], "name": "b", "type": "bands"},
            ],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [2, 2, 2],
            [
                {
                    "labels": ["2022-03-22", "2022-03-17"],
                    "name": "t",
                    "type": "temporal",
                },
                {
                    "labels": ["2022-01-25", "2022-02-01"],
                    "name": "additional_t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02"], "name": "b", "type": "bands"},
            ],
            None,
            None,
            [3, 4, 3, 4, 3, 4, 3, 4],
            [2, 2, 2],
            [
                {
                    "labels": ["2022-03-22", "2022-03-17"],
                    "name": "t",
                    "type": "temporal",
                },
                {
                    "labels": ["2022-01-25", "2022-02-01"],
                    "name": "additional_t",
                    "type": "temporal",
                },
                {"labels": ["B01", "B02"], "name": "b", "type": "bands"},
            ],
        ),
        # tests for checking resample_cube_temporal process with valid_within param
        # should be in tests/integration_tests/test_integration.py
        # because the process needs is_valid process
        # currently solved by naively loading the additional code for the dependency process
        # data shape
        # bands:  B1, B2
        # date 1: 1, 11,
        # date 2: 2, 12,
        # date 3: 3, 13,
        (  # valid_within: nearest date has invalid values, but there are valid values within timespan [targetLabel +/- valid_within]
            [None, None, 3, 11, None, None],
            [2, 3],
            [
                {"labels": ["B01", "B02"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-01-02", "2022-01-07", "2022-01-11"],
                    "name": "t",
                    "type": "temporal",
                },
            ],
            [1, 2],
            [2, 1],
            [
                {"labels": ["B01", "B02"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-01-08"],
                    "name": "t",
                    "type": "temporal",
                },
            ],
            None,
            10,
            [3, 11],
            [2, 1],
            [
                {"labels": ["B01", "B02"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-01-08"],
                    "name": "t",
                    "type": "temporal",
                },
            ],
        ),
        (  # valid_within: no VALID values in the timespan [targetLabel +/- valid_within]
            [None, None, 3, 11, None, None],
            [2, 3],
            [
                {"labels": ["B01", "B02"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-01-02", "2022-01-07", "2022-01-11"],
                    "name": "t",
                    "type": "temporal",
                },
            ],
            [1, 2],
            [2, 1],
            [
                {"labels": ["B01", "B02"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-01-08"],
                    "name": "t",
                    "type": "temporal",
                },
            ],
            None,
            2,
            [None, None],
            [2, 1],
            [
                {"labels": ["B01", "B02"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-01-08"],
                    "name": "t",
                    "type": "temporal",
                },
            ],
        ),
        # data shape
        # bands:  B1, B2
        # date 1: 1, 11,
        # date 2: 2, 12,
        (  # valid_within: no VALID or INVALID values in the timespan [targetLabel +/- valid_within]
            [1, 2, 11, 12],
            [2, 2],
            [
                {"labels": ["B01", "B02"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-01-01", "2022-02-01"],
                    "name": "t",
                    "type": "temporal",
                },
            ],
            [1, 2],
            [2, 1],
            [
                {"labels": ["B01", "B02"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-01-15"],
                    "name": "t",
                    "type": "temporal",
                },
            ],
            None,
            7,
            [None, None],
            [2, 1],
            [
                {"labels": ["B01", "B02"], "name": "b", "type": "bands"},
                {
                    "labels": ["2022-01-15"],
                    "name": "t",
                    "type": "temporal",
                },
            ],
        ),
    ],
)
def test_resample_cube_temporal(
    resample_cube_temporal_process_code,
    construct_datacube,
    data_array,
    data_shape,
    data_dimensions,
    target_array,
    target_shape,
    target_dimensions,
    dimension,
    valid_within,
    expected_array,
    expected_shape,
    expected_dimensions,
):

    data_cube = construct_datacube("dataCube", data_array, data_shape, data_dimensions)
    target_cube = construct_datacube(
        "targetCube", target_array, target_shape, target_dimensions
    )

    additional_js_code_to_run = load_datacube_code() + data_cube + target_cube
    arguments = f"'data': dataCube, 'target': targetCube"

    if dimension:
        additional_js_code_to_run = (
            additional_js_code_to_run + f"const dimension = {json.dumps(dimension)};"
        )
        arguments = arguments + f", 'dimension': {json.dumps(dimension)}"

    if valid_within:
        additional_js_code_to_run = (
            additional_js_code_to_run
            + f"const valid_within = {json.dumps(valid_within)};"
        )
        arguments = arguments + f", 'valid_within': {json.dumps(valid_within)}"

    process_arguments = f"{{" + arguments + f"}}"

    output = run_process(
        additional_js_code_to_run + resample_cube_temporal_process_code,
        "resample_cube_temporal",
        process_arguments,
    )
    output = json.loads(output.decode("utf-8"))

    assert output["data"]["data"] == expected_array
    assert output["data"]["shape"] == expected_shape
    assert output["dimensions"] == expected_dimensions


@pytest.mark.parametrize(
    "data_array, data_shape, data_dimensions, target_array, target_shape, target_dimensions, dimension, valid_within, error_message",
    [
        (  # no data datacube
            None,
            None,
            None,
            [1],
            [1],
            [
                {"labels": ["2022-03-21"], "name": "t", "type": "temporal"},
                {"labels": ["B01"], "name": "b", "type": "bands"},
            ],
            None,
            None,
            "MISSING_PARAMETER: Process resample_cube_temporal requires parameter data.",
        ),
        (  # no target datacube
            [1],
            [1],
            [
                {"labels": ["2022-03-21"], "name": "t", "type": "temporal"},
                {"labels": ["B01"], "name": "b", "type": "bands"},
            ],
            None,
            None,
            None,
            None,
            None,
            "MISSING_PARAMETER: Process resample_cube_temporal requires parameter target.",
        ),
        (  # dimension not a string
            [1],
            [1],
            [
                {"labels": ["2022-03-21"], "name": "t", "type": "temporal"},
                {"labels": ["B01"], "name": "b", "type": "bands"},
            ],
            [1],
            [1],
            [
                {"labels": ["2022-03-21"], "name": "t", "type": "temporal"},
                {"labels": ["B01"], "name": "b", "type": "bands"},
            ],
            123,
            None,
            "WRONG_TYPE: Value for dimension is not a string.",
        ),
        (  # valid_within not a number
            [1],
            [1],
            [
                {"labels": ["2022-03-21"], "name": "t", "type": "temporal"},
                {"labels": ["B01"], "name": "b", "type": "bands"},
            ],
            [1],
            [1],
            [
                {"labels": ["2022-03-21"], "name": "t", "type": "temporal"},
                {"labels": ["B01"], "name": "b", "type": "bands"},
            ],
            None,
            "qwe",
            "WRONG_TYPE: Value for valid_within is not a number.",
        ),
        (  # dimension is given, but does not exist in data
            [1],
            [1],
            [
                {"labels": ["2022-03-21"], "name": "t", "type": "temporal"},
                {"labels": ["B01"], "name": "b", "type": "bands"},
            ],
            [1],
            [1],
            [
                {"labels": ["2022-03-21"], "name": "temp_dim", "type": "temporal"},
                {"labels": ["B01"], "name": "b", "type": "bands"},
            ],
            "temp_dim",
            None,
            "DimensionNotAvailable: A dimension with the specified name does not exist.",
        ),
        (  # dimension is given, but does not exist in target
            [1],
            [1],
            [
                {"labels": ["2022-03-21"], "name": "temp_dim", "type": "temporal"},
                {"labels": ["B01"], "name": "b", "type": "bands"},
            ],
            [1],
            [1],
            [
                {"labels": ["2022-03-21"], "name": "t", "type": "temporal"},
                {"labels": ["B01"], "name": "b", "type": "bands"},
            ],
            "temp_dim",
            None,
            "DimensionNotAvailable: A dimension with the specified name does not exist.",
        ),
        (  # dimension is given, but does not exist in data or target
            [1],
            [1],
            [
                {"labels": ["2022-03-21"], "name": "t", "type": "temporal"},
                {"labels": ["B01"], "name": "b", "type": "bands"},
            ],
            [1],
            [1],
            [
                {"labels": ["2022-03-21"], "name": "t", "type": "temporal"},
                {"labels": ["B01"], "name": "b", "type": "bands"},
            ],
            "temp_dim",
            None,
            "DimensionNotAvailable: A dimension with the specified name does not exist.",
        ),
        (  # dimension is given, but is not temporal in data
            [1],
            [1],
            [
                {"labels": ["2022-03-21"], "name": "t", "type": "other"},
                {"labels": ["B01"], "name": "b", "type": "bands"},
            ],
            [1],
            [1],
            [
                {"labels": ["2022-03-21"], "name": "t", "type": "temporal"},
                {"labels": ["B01"], "name": "b", "type": "bands"},
            ],
            "t",
            None,
            "DimensionMismatch: The temporal dimensions for resampling don't match.",
        ),
        (  # dimension is given, but is not temporal in target
            [1],
            [1],
            [
                {"labels": ["2022-03-21"], "name": "t", "type": "temporal"},
                {"labels": ["B01"], "name": "b", "type": "bands"},
            ],
            [1],
            [1],
            [
                {"labels": ["2022-03-21"], "name": "t", "type": "other"},
                {"labels": ["B01"], "name": "b", "type": "bands"},
            ],
            "t",
            None,
            "DimensionMismatch: The temporal dimensions for resampling don't match.",
        ),
        (  # dimension is given, but not temporal in data and target
            [1],
            [1],
            [
                {"labels": ["2022-03-21"], "name": "t", "type": "other"},
                {"labels": ["B01"], "name": "b", "type": "bands"},
            ],
            [1],
            [1],
            [
                {"labels": ["2022-03-21"], "name": "t", "type": "other"},
                {"labels": ["B01"], "name": "b", "type": "bands"},
            ],
            "t",
            None,
            "DimensionMismatch: The temporal dimensions for resampling don't match.",
        ),
        (  # dimension not given, no temporal dimensions match by name in data and target
            [1],
            [1],
            [
                {"labels": ["2022-03-21"], "name": "t1", "type": "other"},
                {"labels": ["B01"], "name": "b", "type": "bands"},
            ],
            [1],
            [1],
            [
                {"labels": ["2022-03-21"], "name": "t2", "type": "other"},
                {"labels": ["B01"], "name": "b", "type": "bands"},
            ],
            None,
            None,
            "DimensionMismatch: The temporal dimensions for resampling don't match.",
        ),
    ],
)
def test_mask_exceptions(
    resample_cube_temporal_process_code,
    construct_datacube,
    data_array,
    data_shape,
    data_dimensions,
    target_array,
    target_shape,
    target_dimensions,
    dimension,
    valid_within,
    error_message,
):

    additional_js_code_to_run = load_datacube_code()
    arguments = ""

    if data_array and data_shape and data_dimensions:
        data_cube = construct_datacube(
            "dataCube", data_array, data_shape, data_dimensions
        )
        additional_js_code_to_run = additional_js_code_to_run + data_cube
        arguments = arguments + f"'data': dataCube,"

    if target_array and target_shape and target_dimensions:
        target_cube = construct_datacube(
            "targetCube", target_array, target_shape, target_dimensions
        )
        additional_js_code_to_run = additional_js_code_to_run + target_cube
        arguments = arguments + f"'target': targetCube,"

    if dimension:
        additional_js_code_to_run = (
            additional_js_code_to_run + f"const dimension = {json.dumps(dimension)};"
        )
        arguments = arguments + f"'dimension': {json.dumps(dimension)},"

    if valid_within:
        additional_js_code_to_run = (
            additional_js_code_to_run
            + f"const valid_within = {json.dumps(valid_within)};"
        )
        arguments = arguments + f"'valid_within': {json.dumps(valid_within)}"

    process_arguments = f"{{" + arguments + f"}}"

    print(arguments)

    run_input_validation(
        additional_js_code_to_run + resample_cube_temporal_process_code,
        "resample_cube_temporal",
        process_arguments,
        True,
        error_message=error_message,
    )
