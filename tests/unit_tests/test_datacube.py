import json

import pytest

from tests.utils import load_datacube_code, with_stdout_call, run_javascript


@pytest.fixture
def datacube_code():
    def wrapped(
        samples,
        bands_dimension_name="b",
        temporal_dimension_name="t",
        from_samples=True,
        json_samples=True,
        bands_metadata=[],
        scenes=[],
    ):
        return (
            load_datacube_code()
            + f"\nconst datacube = new DataCube({json.dumps(samples) if json_samples else samples}, '{bands_dimension_name}', '{temporal_dimension_name}', {json.dumps(from_samples)}, {json.dumps(bands_metadata)}, {json.dumps(scenes)})"
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
        datacube_code([], from_samples=False)
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
    "example_data,example_data_shape,dimensions,dimension_to_reduce,expected_data,expected_shape",
    [
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
    datacube_code, example_data, example_data_shape, dimensions, dimension_to_reduce, expected_data, expected_shape
):
    reducer = "({data}) => data.reduce((a, b) => a + b, 0)"
    testing_code = (
        datacube_code(f"ndarray({example_data},{example_data_shape})", from_samples=False, json_samples=False)
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


@pytest.mark.parametrize(
    "example_data,example_data_shape,expected_data",
    [
        ([1, 2, 3, 4], [2, 2], [1, 2, 3, 4]),
        ([1, 2, 3, 4], [4], [1, 2, 3, 4]),
        ([1, 2, 3, 4, 5, 6, 7, 8], [2, 2, 2], [1, 2, 3, 4, 5, 6, 7, 8]),
        ([1], [], 1),
    ],
)
def test_flattenToArray(datacube_code, example_data, example_data_shape, expected_data):
    testing_code = datacube_code(
        f"ndarray({example_data},{example_data_shape})", from_samples=False, json_samples=False
    ) + with_stdout_call("datacube.flattenToArray()")
    output = run_javascript(testing_code).decode("utf-8")
    output = json.loads(output)

    assert output == expected_data


@pytest.mark.parametrize(
    "bands,expected_indices",
    [
        (["B01"], [0]),
        (["B02"], [1]),
        (["B03"], [2]),
        (["B01", "B02", "B03"], [0, 1, 2]),
        (["B01", "B02", "non-existent"], [0, 1]),
        (["non-existent"], []),
    ],
)
def test_getBandIndices(datacube_code, bands, expected_indices):
    testing_code = datacube_code([{"B01": 1, "B02": 2, "B03": 3}, {"B01": 4, "B02": 5, "B03": 6}]) + with_stdout_call(
        f"datacube.getBandIndices({bands})"
    )
    output = run_javascript(testing_code).decode("utf-8")
    output = json.loads(output)

    assert output == expected_indices


@pytest.mark.parametrize(
    "example_data,bands_dimension_name,temporal_dimension_name,dimensions,expected_data",
    [
        (
            [{"B01": 1, "B02": 2, "B03": 3}, {"B01": 4, "B02": 5, "B03": 6}],
            "bands",
            "temp",
            [
                {"name": "temp", "labels": [], "type": "temporal"},
                {"name": "bands", "labels": [], "type": "bands"},
            ],
            {"data": [1, 2, 3, 4, 5, 6], "shape": [2, 3], "stride": [3, 1], "offset": 0},
        ),
    ],
)
def test_clone(datacube_code, example_data, bands_dimension_name, temporal_dimension_name, dimensions, expected_data):
    testing_code = (
        datacube_code(
            example_data, bands_dimension_name=bands_dimension_name, temporal_dimension_name=temporal_dimension_name
        )
        + (f"\ndatacube.dimensions = {json.dumps(dimensions)}" if dimensions else "")
        + with_stdout_call("datacube.clone()")
    )
    output = run_javascript(testing_code)
    output = json.loads(output)

    assert output["data"] == expected_data
    assert output["dimensions"] == dimensions
    assert output["temporal_dimension_name"] == temporal_dimension_name
    assert output["bands_dimension_name"] == bands_dimension_name


@pytest.mark.parametrize(
    "example_data,example_data_shape,dimensions,axis_to_filter,indices_to_keep,expected_data,expected_shape",
    [
        ([1, 2, 3, 4], [2, 2], None, 1, [0], [1, 3], [2, 1]),
        ([1, 2, 3, 4], [2, 2], None, 0, [0], [1, 2], [1, 2]),
        (
            [1, 2, 3, 4, 5, 6, 7, 8],
            [2, 2, 2],
            [
                {"name": "x", "labels": [], "type": "other"},
                {"name": "t", "labels": [], "type": "temporal"},
                {"name": "b", "labels": [], "type": "bands"},
            ],
            0,
            [1],
            [5, 6, 7, 8],
            [1, 2, 2],
        ),
        (
            [1, 2, 3, 4, 5, 6],
            [2, 3, 1],
            [
                {"name": "x", "labels": [], "type": "other"},
                {"name": "t", "labels": [], "type": "temporal"},
                {"name": "b", "labels": [], "type": "bands"},
            ],
            1,
            [0, 2],
            [1, 3, 4, 6],
            [2, 2, 1],
        ),
        (
            [1, 2, 3, 4, 5, 6, 7, 8],
            [2, 2, 2],
            [
                {"name": "x", "labels": [], "type": "other"},
                {"name": "t", "labels": [], "type": "temporal"},
                {"name": "b", "labels": [], "type": "bands"},
            ],
            1,
            [0, 1],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [2, 2, 2],
        ),
        (
            [1, 2, 3, 4, 5, 6, 7, 8],
            [4, 1, 2],
            [
                {"name": "x", "labels": [], "type": "other"},
                {"name": "t", "labels": [], "type": "temporal"},
                {"name": "b", "labels": [], "type": "bands"},
            ],
            0,
            [0, 1, 3],
            [1, 2, 3, 4, 7, 8],
            [3, 1, 2],
        ),
        (
            [1, 2, 3, 4, 5, 6, 7, 8],
            [4, 1, 2],
            [
                {"name": "x", "labels": [], "type": "other"},
                {"name": "t", "labels": [], "type": "temporal"},
                {"name": "b", "labels": [], "type": "bands"},
            ],
            2,
            [0],
            [1, 3, 5, 7],
            [4, 1, 1],
        ),
    ],
)
def test_filter(
    datacube_code,
    example_data,
    example_data_shape,
    dimensions,
    axis_to_filter,
    indices_to_keep,
    expected_data,
    expected_shape,
):
    testing_code = (
        datacube_code(f"ndarray({example_data},{example_data_shape})", from_samples=False, json_samples=False)
        + (f"\ndatacube.dimensions = {json.dumps(dimensions)}" if dimensions else "")
        + f"\ndatacube._filter({axis_to_filter},{json.dumps(indices_to_keep)});"
        + with_stdout_call("datacube")
    )
    output = run_javascript(testing_code)
    output = json.loads(output)
    assert output["data"]["data"] == expected_data
    assert output["data"].get("shape") == expected_shape


@pytest.mark.parametrize(
    "example_data,example_data_shape,axis_to_extend,data_to_add,expected_data,expected_data_shape",
    [
        ([1, 2, 3, 4, 5, 6], [2, 3], 1, [-10, -11], [1, 2, 3, -10, 4, 5, 6, -11], [2, 4]),
        ([1, 2, 3, 4, 5, 6], [3, 2], 0, [-10, -11], [1, 2, 3, 4, 5, 6, -10, -11], [4, 2]),
        ([1, 2, 3, 4, 5, 6], [2, 3], 0, [-10, -11, -12], [1, 2, 3, 4, 5, 6, -10, -11, -12], [3, 3]),
        ([1, 2, 3, 4, 5, 6], [3, 2], 1, [-10, -11, -12], [1, 2, -10, 3, 4, -11, 5, 6, -12], [3, 3]),
        ([1, 2, 3, 4, 5, 6, 7, 8], [2, 2, 2], 0, [-1, -2, -3, -4], [1, 2, 3, 4, 5, 6, 7, 8, -1, -2, -3, -4], [3, 2, 2]),
        ([1, 2, 3, 4, 5, 6, 7, 8], [2, 2, 2], 1, [-1, -2, -3, -4], [1, 2, 3, 4, -1, -2, 5, 6, 7, 8, -3, -4], [2, 3, 2]),
        ([1, 2, 3, 4, 5, 6, 7, 8], [2, 2, 2], 2, [-1, -2, -3, -4], [1, 2, -1, 3, 4, -2, 5, 6, -3, 7, 8, -4], [2, 2, 3]),
    ],
)
def test_extendDimensionWithData(
    datacube_code, example_data, example_data_shape, axis_to_extend, data_to_add, expected_data, expected_data_shape
):
    testing_code = (
        datacube_code(f"ndarray({example_data},{example_data_shape})", from_samples=False, json_samples=False)
        + f"\ndatacube.extendDimensionWithData({axis_to_extend},{data_to_add});"
        + with_stdout_call("datacube")
    )
    output = run_javascript(testing_code)
    output = json.loads(output)
    assert output["data"]["data"] == expected_data
    assert output["data"].get("shape") == expected_data_shape


@pytest.mark.parametrize(
    "example_data,example_data_shape,axis,data_to_add,location_in_dimension,expected_data,expected_shape",
    [
        ([1, 2, 3, 4], [2, 2], 0, [5, 6], 0, [5, 6, 1, 2, 3, 4], [3, 2]),
        ([1, 2, 3, 4], [2, 2], 0, [5, 6], 1, [1, 2, 5, 6, 3, 4], [3, 2]),
        ([1, 2, 3, 4], [2, 2], 0, [5, 6], 2, [1, 2, 3, 4, 5, 6], [3, 2]),
        ([1, 2, 3, 4], [2, 2], 1, [5, 6], 0, [5, 1, 2, 6, 3, 4], [2, 3]),
        ([1, 2, 3, 4], [2, 2], 1, [5, 6], 1, [1, 5, 2, 3, 6, 4], [2, 3]),
        ([1, 2, 3, 4], [2, 2], 1, [5, 6], 2, [1, 2, 5, 3, 4, 6], [2, 3]),
    ],
)
def test_insert_into_dimension(
    datacube_code,
    example_data,
    example_data_shape,
    axis,
    data_to_add,
    location_in_dimension,
    expected_data,
    expected_shape,
):
    testing_code = (
        datacube_code(f"ndarray({example_data},{example_data_shape})", from_samples=False, json_samples=False)
        + f"\ndatacube.insertIntoDimension({axis},{json.dumps(data_to_add)},{location_in_dimension});"
        + with_stdout_call("datacube")
    )
    output = run_javascript(testing_code)
    output = json.loads(output)
    assert output["data"]["data"] == expected_data
    assert output["data"].get("shape") == expected_shape


@pytest.mark.parametrize(
    "example_data,example_data_shape,axis,data_to_set,index,expected_data",
    [
        ([1, 2, 3, 4, 5, 6, 7, 8], [2, 2, 2], 0, [9, 99, 999, 9999], 0, [9, 99, 999, 9999, 5, 6, 7, 8]),
        ([1, 2, 3, 4, 5, 6, 7, 8], [2, 2, 2], 0, [9, 99, 999, 9999], 1, [1, 2, 3, 4, 9, 99, 999, 9999]),
        ([1, 2, 3, 4, 5, 6, 7, 8], [2, 2, 2], 1, [9, 99, 999, 9999], 0, [9, 99, 3, 4, 999, 9999, 7, 8]),
        ([1, 2, 3, 4, 5, 6, 7, 8], [2, 2, 2], 1, [9, 99, 999, 9999], 1, [1, 2, 9, 99, 5, 6, 999, 9999]),
        ([1, 2, 3, 4, 5, 6, 7, 8], [2, 2, 2], 2, [9, 99, 999, 9999], 0, [9, 2, 99, 4, 999, 6, 9999, 8]),
        ([1, 2, 3, 4, 5, 6, 7, 8], [2, 2, 2], 2, [9, 99, 999, 9999], 1, [1, 9, 3, 99, 5, 999, 7, 9999]),
    ],
)
def test_set_in_dimension(datacube_code, example_data, example_data_shape, axis, data_to_set, index, expected_data):
    testing_code = (
        datacube_code(f"ndarray({example_data},{example_data_shape})", from_samples=False, json_samples=False)
        + f"\ndatacube.setInDimension({axis},{json.dumps(data_to_set)},{index});"
        + with_stdout_call("datacube")
    )
    output = run_javascript(testing_code)
    output = json.loads(output)
    assert output["data"]["data"] == expected_data
    assert output["data"].get("shape") == example_data_shape


@pytest.mark.parametrize(
    "scenes,expected_temporal_labels",
    [
        ({"bandBuffers": []}, []),
        (
            [
                {
                    "date": "2022-07-04T10:09:39.000Z",
                    "tileId": 21257937,
                    "tileOriginalId": "S2A_OPER_MSI_L2A_TL_ATOS_20220704T141618_A036727_T32TQL_N04.00",
                    "orbitId": 66338,
                    "productId": "S2A_MSIL2A_20220704T100041_N0400_R122_T32TQL_20220704T141618",
                    "__idx": 0,
                    "bandBuffers": [{}, {}, {}, {}],
                },
                {
                    "date": "2022-07-04T10:09:39.000Z",
                    "tileId": 21257552,
                    "tileOriginalId": "S2A_OPER_MSI_L2A_TL_ATOS_20220704T141618_A036727_T33TTF_N04.00",
                    "orbitId": 66338,
                    "productId": "S2A_MSIL2A_20220704T100041_N0400_R122_T33TTF_20220704T141618",
                    "__idx": 1,
                    "bandBuffers": [{}, {}, {}, {}],
                },
            ],
            ["2022-07-04T10:09:39.000Z", "2022-07-04T10:09:39.000Z"],
        ),
        (
            [{"date": "2022-07-04T00:00:00.000Z", "__idx": 0, "bandBuffers": [{}, {}, {}, {}]}],
            ["2022-07-04T00:00:00.000Z"],
        ),
    ],
)
def test_scenes(datacube_code, scenes, expected_temporal_labels):
    testing_code = datacube_code(
        f"ndarray([1, 2, 3, 4, 5, 6, 7, 8],[2, 2, 2])", from_samples=False, json_samples=False, scenes=scenes
    ) + with_stdout_call("datacube")

    output = run_javascript(testing_code)
    output = json.loads(output)
    assert next(dim for dim in output["dimensions"] if dim["name"] == "t")["labels"] == expected_temporal_labels
