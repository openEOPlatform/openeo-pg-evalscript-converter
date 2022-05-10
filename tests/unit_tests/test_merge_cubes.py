import json

import pytest

from tests.utils import load_process_code, load_datacube_code, run_process, run_input_validation


@pytest.fixture
def merge_cubes_process_code():
    return load_process_code("merge_cubes")


@pytest.fixture
def construct_datacube():
    def wrapped(cube_name, data, data_shape, dimensions):
        return (
            f"\nconst {cube_name} = new DataCube(ndarray({json.dumps(data)}, {json.dumps(data_shape)}), 'b', 't', false);"
            + f"\n{cube_name}.dimensions = {json.dumps(dimensions)};"
        )

    return wrapped


@pytest.mark.parametrize(
    "data_cube1,data_shape_cube1,dimensions_cube1,data_cube2,data_shape_cube2,dimensions_cube2,overlap_resolver,data_expected_cube,data_shape_expected_cube,dimensions_expected_cube",
    [
        (
            # Merging datacubes with no overlap (different band labels)
            [1, 2, 3, 4, 5, 6],
            [3, 2],
            [
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
            [7, 8, 9, 10, 11, 12],
            [3, 2],
            [
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B3", "B4"], "name": "b", "type": "bands"},
            ],
            None,
            [1, 2, 7, 8, 3, 4, 9, 10, 5, 6, 11, 12],
            [3, 4],
            [
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2", "B3", "B4"], "name": "b", "type": "bands"},
            ],
        ),
        (
            # Merging datacubes with no overlap (different temporal labels)
            [1, 2, 3, 4, 5, 6],
            [3, 2],
            [
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
            [7, 8, 9, 10, 11, 12],
            [3, 2],
            [
                {"labels": ["2022-04-01", "2022-05-01", "2022-06-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
            None,
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            [6, 2],
            [
                {
                    "labels": ["2022-01-01", "2022-02-01", "2022-03-01", "2022-04-01", "2022-05-01", "2022-06-01"],
                    "name": "t",
                    "type": "temporal",
                },
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
        ),
        (
            # Merging datacubes with an overlapping band B2
            [1, 2, 3, 4, 5, 6],
            [3, 2],
            [
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
            [7, 8, 9, 10, 11, 12],
            [3, 2],
            [
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B2", "B3"], "name": "b", "type": "bands"},
            ],
            "({x,y}) => (x+y)",
            [1, 9, 8, 3, 13, 10, 5, 17, 12],
            [3, 3],
            [
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2", "B3"], "name": "b", "type": "bands"},
            ],
        ),
        (
            # Merging datacubes with overlapping temporal labels 2022-02-01 and 2022-03-01
            [1, 2, 3, 4, 5, 6],
            [3, 2],
            [
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
            [7, 8, 9, 10, 11, 12],
            [3, 2],
            [
                {"labels": ["2022-02-01", "2022-03-01", "2022-04-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
            "({x,y}) => (x+y)",
            [1, 2, 10, 12, 14, 16, 11, 12],
            [4, 2],
            [
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01", "2022-04-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
        ),
        (
            # Merging fully overlapping datacubes
            [1, 2, 3, 4, 5, 6],
            [3, 2],
            [
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
            [7, 8, 9, 10, 11, 12],
            [3, 2],
            [
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
            "({x,y}) => (x+y)",
            [8, 10, 12, 14, 16, 18],
            [3, 2],
            [
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
        ),
        (
            # Merging fully overlapping datacubes without overlap_resolver
            [1, 2, 3, 4, 5, 6],
            [3, 2],
            [
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
            [7, 8, 9, 10, 11, 12],
            [3, 2],
            [
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
            None,
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            [2, 3, 2],
            [
                {"labels": ["cube1", "cube2"], "name": "cubes", "type": "other"},
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
        ),
        (
            # Merging lower dimension cube into higher dimension cube
            [1, 2, 3, 4, 5, 6],
            [3, 2],
            [
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
            [7, 8],
            [2],
            [
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
            "({x,y}) => (x+y)",
            [8, 10, 10, 12, 12, 14],
            [3, 2],
            [
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
        ),
        (
            # Merging lower dimension cube into higher dimension cube
            [1, 2, 3, 4, 5, 6, 7, 8],
            [2, 2, 2, 1],
            [
                {"labels": [0, 1], "name": "x", "type": "spatial"},
                {"labels": [0, 1], "name": "y", "type": "spatial"},
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
            [9, 10, 11, 12],
            [2, 2],
            [{"labels": [0, 1], "name": "x", "type": "spatial"}, {"labels": [0, 1], "name": "y", "type": "spatial"}],
            "({x,y}) => (x+y)",
            [10, 11, 13, 14, 16, 17, 19, 20],
            [2, 2, 2, 1],
            [
                {"labels": [0, 1], "name": "x", "type": "spatial"},
                {"labels": [0, 1], "name": "y", "type": "spatial"},
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
        ),
        (
            # Merging lower dimension cube into higher dimension cube other way around
            [9, 10, 11, 12],
            [2, 2],
            [{"labels": [0, 1], "name": "x", "type": "spatial"}, {"labels": [0, 1], "name": "y", "type": "spatial"}],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [2, 2, 2, 1],
            [
                {"labels": [0, 1], "name": "x", "type": "spatial"},
                {"labels": [0, 1], "name": "y", "type": "spatial"},
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
            "({x,y}) => (x+y)",
            [10, 11, 13, 14, 16, 17, 19, 20],
            [2, 2, 2, 1],
            [
                {"labels": [0, 1], "name": "x", "type": "spatial"},
                {"labels": [0, 1], "name": "y", "type": "spatial"},
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
        ),
        (
            # Merging cubes with overlapping dimension y
            [1, 2, 3, 4, 5, 6, 7, 8],
            [2, 2, 2, 1],
            [
                {"labels": [0, 1], "name": "x", "type": "spatial"},
                {"labels": [0, 1], "name": "y", "type": "spatial"},
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
            [9, 10, 11, 12, 13, 14, 15, 16],
            [2, 2, 2, 1],
            [
                {"labels": [0, 1], "name": "x", "type": "spatial"},
                {"labels": [1, 2], "name": "y", "type": "spatial"},
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
            "({x,y}) => (x+y)",
            [1, 2, 12, 14, 11, 12, 5, 6, 20, 22, 15, 16],
            [2, 3, 2, 1],
            [
                {"labels": [0, 1], "name": "x", "type": "spatial"},
                {"labels": [0, 1, 2], "name": "y", "type": "spatial"},
                {"labels": ["2022-01-01", "2022-02-01", "2022-03-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
        )
    ],
)
def test_merge_cubes(
    merge_cubes_process_code,
    construct_datacube,
    data_cube1,
    data_shape_cube1,
    dimensions_cube1,
    data_cube2,
    data_shape_cube2,
    dimensions_cube2,
    overlap_resolver,
    data_expected_cube,
    data_shape_expected_cube,
    dimensions_expected_cube,
):
    cube_1 = construct_datacube("cube1", data_cube1, data_shape_cube1, dimensions_cube1)
    cube_2 = construct_datacube("cube2", data_cube2, data_shape_cube2, dimensions_cube2)

    output = run_process(
        load_datacube_code() + merge_cubes_process_code + cube_1 + cube_2,
        "merge_cubes",
        f"{{cube1:cube1,cube2:cube2,overlap_resolver:{overlap_resolver if overlap_resolver is not None else 'undefined'}}}",
    )

    output = json.loads(output.decode("utf-8"))
    assert output["data"]["data"] == data_expected_cube
    assert output["data"]["shape"] == data_shape_expected_cube
    assert output["dimensions"] == dimensions_expected_cube


@pytest.mark.parametrize(
    "data_cube1,data_shape_cube1,dimensions_cube1,data_cube2,data_shape_cube2,dimensions_cube2,overlap_resolver,error_message",
    [
        (
            [1],
            [1],
            [
                {"labels": ["B1"], "name": "b", "type": "bands"},
            ],
            [2,3],
            [2],
            [
                {"labels": ["B1", "B2"], "name": "b", "type": "bands"},
            ],
            None,
            "Overlapping data cubes, but no overlap resolver has been specified.",
        ),
        (
            [1],
            [1],
            [
                {"labels": ["B1"], "name": "b", "type": "bands"},
            ],
            [2],
            [1],
            [
                {"labels": ["B1"], "name": "b", "type": "temporal"},
            ],
            "({x,y}) => (x+y)",
            "Shared dimensions have to have the same name and type in 'merge_cubes'.",
        ),
        (
            [1],
            [1],
            [
                {"labels": ["2022-01-01"], "name": "t", "type": "temporal"},
                {"labels": ["B1"], "name": "b", "type": "bands"},
            ],
            [2],
            [1],
            [
                {"labels": ["2022-02-02"], "name": "t", "type": "temporal"},
                {"labels": ["B2"], "name": "b", "type": "bands"},
            ],
            "({x,y}) => (x+y)",
            "Only one of the dimensions can have different labels in 'merge_cubes'.",
        ),
    ],
)
def test_merge_cubes_exceptions(
    merge_cubes_process_code,
    construct_datacube,
    data_cube1,
    data_shape_cube1,
    dimensions_cube1,
    data_cube2,
    data_shape_cube2,
    dimensions_cube2,
    overlap_resolver,
    error_message,
):
    cube_1 = construct_datacube("cube1", data_cube1, data_shape_cube1, dimensions_cube1)
    cube_2 = construct_datacube("cube2", data_cube2, data_shape_cube2, dimensions_cube2)
    process_arguments = f"{{cube1:cube1,cube2:cube2,overlap_resolver:{overlap_resolver if overlap_resolver is not None else 'undefined'}}}"

    run_input_validation(
        load_datacube_code() + merge_cubes_process_code + cube_1 + cube_2,
        "merge_cubes",
        process_arguments,
        True,
        error_message=error_message,
    )
