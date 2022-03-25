import json

import pytest

from tests.utils import load_datacube_code, with_stdout_call, run_javascript


@pytest.fixture
def datacube_code():
    def wrapped(samples, from_samples=True, json_samples=True):
        return (
            load_datacube_code()
            + f"\nconst datacube = new DataCube({json.dumps(samples) if json_samples else samples}, 'b', 't', {json.dumps(from_samples)})"
        )

    return wrapped


@pytest.mark.parametrize(
    "example_samples,expected_data,expected_shape",
    [
        ([{"B01": 1, "B02": 2}, {"B01": 3, "B02": 4}], [1, 2, 3, 4], [2, 2]),
        ({"B01": 1, "B02": 2}, [1, 2], [1, 2]),
        ([{"B01": 1, "B02": 2, "B03": 3, "B04": 4}], [1, 2, 3, 4], [1, 4]),
    ],
)
def test_makeArrayFromSamples(datacube_code, example_samples, expected_data, expected_shape):
    testing_code = datacube_code(example_samples) + with_stdout_call("datacube")
    output = run_javascript(testing_code)
    output = json.loads(output)
    assert output["data"]["data"] == expected_data
    assert output["data"]["shape"] == expected_shape


@pytest.mark.parametrize(
    "shape,null_axes,expected_coords",
    [
        ([2, 2], [], [[0, 0], [0, 1], [1, 0], [1, 1]]),
        ([1], [], [[0]]),
        ([3], [], [[0], [1], [2]]),
        ([2, 2, 2], [], [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]),
        ([2, 2], [0], [[None, 0], [None, 1]]),
        ([2, 2], [1], [[0, None], [1, None]]),
        ([2, 2], [0, 1], [[None, None]]),
        ([2, 2, 2], [0, 1, 2], [[None, None, None]]),
        ([2, 2, 2], [0, 1], [[None, None, 0], [None, None, 1]]),
        ([2, 2, 2], [0, 2], [[None, 0, None], [None, 1, None]]),
        ([2, 2, 2], [1], [[0, None, 0], [0, None, 1], [1, None, 0], [1, None, 1]]),
        ([2, 2, 2], [2], [[0, 0, None], [0, 1, None], [1, 0, None], [1, 1, None]]),
    ],
)
def test_iterateCoords(datacube_code, shape, null_axes, expected_coords):
    testing_code = (
        datacube_code([])
        + f"\nfor(let c of datacube._iterateCoords({json.dumps(shape)}, {json.dumps(null_axes)})) {{console.log(c)}}"
    )
    output = run_javascript(testing_code).decode("utf-8")
    coords = output.strip().split("\n")

    for i, coord in enumerate(coords):
        coord = json.loads(coord)
        assert coord in expected_coords
        expected_coords.remove(coord)

    assert len(expected_coords) == 0


@pytest.mark.parametrize(
    "example_data,expected_data_shape,dimensions,dimension_to_reduce,expected_data,expected_shape",
    [
        ([1, 2, 3, 4], [2, 2], None, "b", [3, 7], [2]),
        ([1, 2, 3, 4], [2, 2], None, "t", [4, 6], [2]),
        (
            [1, 2, 3, 4, 5, 6, 7, 8],
            [2, 2, 2],
            [
                {"name": "x", "labels": [], "type": "other"},
                {"name": "t", "labels": [], "type": "temporal"},
                {"name": "b", "labels": [], "type": "bands"},
            ],
            "b",
            [3, 7, 11, 15],
            [2, 2],
        ),
        (
            [1, 2, 3, 4, 5, 6, 7, 8],
            [2, 2, 2],
            [
                {"name": "x", "labels": [], "type": "other"},
                {"name": "t", "labels": [], "type": "temporal"},
                {"name": "b", "labels": [], "type": "bands"},
            ],
            "t",
            [4, 6, 12, 14],
            [2, 2],
        ),
        (
            [1, 2, 3, 4, 5, 6, 7, 8],
            [2, 2, 2],
            [
                {"name": "x", "labels": [], "type": "other"},
                {"name": "t", "labels": [], "type": "temporal"},
                {"name": "b", "labels": [], "type": "bands"},
            ],
            "x",
            [6, 8, 10, 12],
            [2, 2],
        ),
        ([1, 2], [2], [{"name": "t", "labels": [], "type": "temporal"}], "t", [3], None),
    ],
)
def test_reduceByDimension(
    datacube_code, example_data, expected_data_shape, dimensions, dimension_to_reduce, expected_data, expected_shape
):
    reducer = "({data}) => data.reduce((a, b) => a + b, 0)"
    testing_code = (
        datacube_code(f"ndarray({example_data},{expected_data_shape})", from_samples=False, json_samples=False)
        + (f"\ndatacube.dimensions = {json.dumps(dimensions)}" if dimensions else "")
        + f"\ndatacube.reduceByDimension({reducer},'{dimension_to_reduce}');"
        + with_stdout_call("datacube")
    )
    output = run_javascript(testing_code)
    output = json.loads(output)
    assert output["data"]["data"] == expected_data
    assert output["data"].get("shape") == expected_shape


@pytest.mark.parametrize(
    "example_data,example_data_shape,expected_data",
    [
        ([1, 2, 3, 4], [2, 2], [3, 6, 9, 12]),
        ([1, 2, 3, 4], [4], [3, 6, 9, 12]),
        ([1], [], [3]),
        ([1, 2, 3, 4, 5, 6, 7, 8], [2, 2, 2], [3, 6, 9, 12, 15, 18, 21, 24]),
    ],
)
def test_apply(datacube_code, example_data, example_data_shape, expected_data):
    process = "({x}) => x * 3"
    testing_code = (
        datacube_code(f"ndarray({example_data},{example_data_shape})", from_samples=False, json_samples=False)
        + f"\ndatacube.apply({process});"
        + with_stdout_call("datacube")
    )
    output = run_javascript(testing_code)
    output = json.loads(output)
    assert output["data"]["data"] == expected_data
