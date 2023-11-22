import json

import pytest
from pg_to_evalscript import convert_from_process_graph, list_supported_processes

from tests.utils import (
    get_process_graph_json,
    run_evalscript,
    get_defined_processes_from_files,
    get_evalscript_input_object,
    get_n_output_bands,
)
from tests.integration_tests.fixtures import user_defined_processes, bands_metadata


@pytest.mark.parametrize(
    "pg_name,example_input,bands_metadata,expected_output",
    [
        ("test_graph_1", [{"B01": 3, "B02": 3}, {"B01": 5, "B02": 1}], None, [4, 2]),
        ("reduce_mean_one_band", [{"B01": 3}, {"B01": 5}], None, [4]),
        ("reduce_mean_one_band", [{"B01": 3}], None, [3]),
        ("reduce_mean_one_band", [{"B01": 3}, {"B01": 5}, {"B01": 10}, {"B01": 6}], None, [6]),
        ("test_short_graph", [{"B01": 3, "B02": 2}, {"B01": 5, "B02": 1}], None, [3, 2, 5, 1]),
        ("test_apply_absolute", [{"B01": 0.1, "B02": -0.15}, {"B01": 0, "B02": 2}], None, [0.1, 0.15, 0, 2]),
        (
            "test_apply_math",
            [{"B01": 0, "B02": 1}, {"B01": -1, "B02": 0.5}, {"B01": None, "B02": None}],
            None,
            [-0.75, 0, -1.5, -0.375, None, None],
        ),
        (
            "test_apply_linear_scale_range",
            [{"B01": 0.5, "B02": 0.75}, {"B01": 0, "B02": 1}, {"B01": -3, "B02": 4}, {"B01": None, "B02": None}],
            None,
            [1, 1.5, 0, 2, 0, 2, None, None],
        ),
        ("test_graph_1", [], None, []),
        (
            "test_mean_of_mean",
            [{"B04": 0, "B08": 1}, {"B04": 2, "B08": 3}, {"B04": 3, "B08": 5}, {"B04": 1, "B08": 4}],
            None,
            [2.375],
        ),
        (
            "test_count_with_condition",
            [{"B01": 0, "B02": 1}, {"B01": 2, "B02": 3}, {"B01": 4, "B02": 5}, {"B01": None, "B02": None}],
            None,
            [1, 2],
        ),
        (
            "test_count_without_condition",
            [{"B01": 0, "B02": 1}, {"B01": 2, "B02": 3}, {"B01": 4, "B02": 5}, {"B01": None, "B02": 3}],
            None,
            [3, 4],
        ),
        (
            "test_array_apply_add",
            [{"B01": 0, "B02": 1, "B03": 2, "B04": 3, "B05": 4, "B06": 5}],
            None,
            [10, 11, 12, 13, 14, 15],
        ),
        ("test_array_filter", [{"B01": 0}, {"B01": 1}, {"B01": 2}, {"B01": 4}, {"B01": 5}], None, [11]),
        (
            "test_apply_dimension_absolute",
            [{"B01": -0.1, "B02": 0.15}, {"B01": 0, "B02": 2}, {"B01": -1, "B02": -2}],
            None,
            [0.1, 0.15, 0, 2, 1, 2],
        ),
        (
            "gee_uc1_pol",
            [{"VV": 0, "VH": 1}, {"VV": 2, "VH": 3}, {"VV": 4, "VH": 5}, {"VV": 6, "VH": 7}],
            None,
            [3, 4, 1],
        ),
        ("test_mean_ndvi", [{"B04": 3, "B08": 9}, {"B04": 1, "B08": 7}], bands_metadata, [0.6]),
    ],
)
def test_convertable_process_graphs(pg_name, example_input, bands_metadata, expected_output):
    process_graph = get_process_graph_json(pg_name)
    result = convert_from_process_graph(process_graph, bands_metadata=bands_metadata, encode_result=False)

    assert len(result) == 1 and result[0]["invalid_node_id"] is None

    evalscript = result[0]["evalscript"].write()

    output = run_evalscript(evalscript, example_input)
    output = json.loads(output)

    assert output == expected_output


@pytest.mark.parametrize(
    "pg_name,example_input,scenes,expected_output",
    [
        (
            "test_filter_temporal",
            [{"B01": 3, "B02": 3}, {"B01": 5, "B02": 1}],
            [
                {"date": "2022-03-21T00:00:00.000Z"},
                {"date": "2022-03-19T00:00:00.000Z"},
            ],
            [5, 1],
        ),
        (
            "test_filter_temporal",
            [{"B01": -0.1, "B02": 0.15}, {"B01": 0, "B02": 2}, {"B01": -1, "B02": -2}],
            [
                {"date": "2022-03-21T00:00:00.000Z"},
                {"date": "2022-03-19T00:00:00.000Z"},
                {"date": "2022-03-16T00:00:00.000Z"},
            ],
            [0, 2, -1, -2],
        ),
        (
            "test_aggregate_temporal",
            [
                {"B01": 16, "B02": 6},
                {"B01": 17, "B02": 5},
                {"B01": 18, "B02": 4},
                {"B01": 19, "B02": 3},
                {"B01": 20, "B02": 2},
                {"B01": 21, "B02": 1},
            ],
            [
                {"date": "2022-03-16T00:00:00.000Z"},
                {"date": "2022-03-17T00:00:00.000Z"},
                {"date": "2022-03-18T00:00:00.000Z"},
                {"date": "2022-03-19T00:00:00.000Z"},
                {"date": "2022-03-20T00:00:00.000Z"},
                {"date": "2022-03-21T00:00:00.000Z"},
            ],
            [16.5, 5.5, 19.5, 2.5],
        ),
        (
            "test_atp_week_sum",
            [{"B01": 0.1, "B02": 23}, {"B01": 2.7, "B02": -1}, {"B01": 17, "B02": -3.9}, {"B01": 0, "B02": 0.1}],
            [
                {"date": "2022-03-19T00:00:00.000Z"},
                {"date": "2022-03-20T00:00:00.000Z"},
                {"date": "2022-03-21T00:00:00.000Z"},
                {"date": "2022-04-01T00:00:00.000Z"},
            ],
            [19.8, 18.1, 0, 0.1],
        ),
        (
            "test_atp_week_sum",
            [{"B01": 0.1, "B02": 23}, {"B01": 2.7, "B02": -1}, {"B01": 17, "B02": -3.9}, {"B01": -28.8, "B02": -2.1}],
            [
                {"date": "2022-03-19T00:00:00.000Z"},
                {"date": "2022-03-20T00:00:00.000Z"},
                {"date": "2022-03-21T00:00:00.000Z"},
                {"date": "2022-03-23T00:00:00.000Z"},
            ],
            [-9, 16],
        ),
        (
            "test_atp_month_mean",
            [
                {"B01": 1, "B02": 2, "B03": 3},
                {"B01": 4, "B02": 5, "B03": 6},
                {"B01": 10, "B02": 11, "B03": 12},
                {"B01": 14, "B02": 15, "B03": 16},
            ],
            [
                {"date": "2022-02-11T00:00:00.000Z"},
                {"date": "2022-02-12T00:00:00.000Z"},
                {"date": "2022-02-13T00:00:00.000Z"},
                {"date": "2022-04-27T00:00:00.000Z"},
            ],
            [5, 6, 7, None, None, None, 14, 15, 16],
        ),
        (
            "test_atp_season_count",
            [
                {"B01": 1, "B02": 2, "B03": 3},
                {"B01": 4, "B02": 5, "B03": 6},
                {"B01": 10, "B02": 11, "B03": 12},
                {"B01": 14, "B02": 15, "B03": 16},
            ],
            [
                {"date": "2022-02-11T00:00:00.000Z"},
                {"date": "2022-02-12T00:00:00.000Z"},
                {"date": "2022-02-13T00:00:00.000Z"},
                {"date": "2022-11-27T00:00:00.000Z"},
            ],
            [3, 3, 3, None, None, None, None, None, None, 1, 1, 1],
        ),
        (  # resample_cube_temporal: tests for valid_within argument (downsampling)
            # first pair in expected_output: VALID values from nearest date in the timespan [targetLabel +/- valid_within]
            # second pair in expected_output: no VALID or INVALID values in the timespan [targetLabel +/- valid_within], return null
            "test_resample_cube_temporal_downsample",
            [
                {"B01": 0, "B02": 9},
                {"B01": 1, "B02": 8},
                {"B01": 2, "B02": 7},
                {"B01": 3, "B02": 6},
            ],
            [
                {"date": "2022-01-01T00:00:00.000Z"},
                {"date": "2022-01-07T00:00:00.000Z"},
                {"date": "2022-01-15T00:00:00.000Z"},
                {"date": "2022-01-28T00:00:00.000Z"},
            ],
            [0, 9, None, None],
        ),
        (  # resample_cube_temporal: tests for valid_within argument (downsampling)
            # first pair in expected_output: nearest date has invalid values, use second nearest in the timespan [targetLabel +/- valid_within]
            # second pair in expected_output: no VALID values in the timespan [targetLabel +/- valid_within], return null
            "test_resample_cube_temporal_downsample",
            [
                {"B01": None, "B02": None},
                {"B01": 1, "B02": 8},
                {"B01": None, "B02": None},
                {"B01": None, "B02": None},
            ],
            [
                {"date": "2022-01-01T00:00:00.000Z"},
                {"date": "2022-01-07T00:00:00.000Z"},
                {"date": "2022-01-18T00:00:00.000Z"},
                {"date": "2022-01-22T00:00:00.000Z"},
            ],
            [1, 8, None, None],
        ),
        (  # resample_cube_temporal: tests for valid_within argument (upsampling)
            # first pair in expected_output: valid values the timespan [targetLabel +/- valid_within]
            # second pair in expected_output: valid values the timespan [targetLabel +/- valid_within]
            # third pair in expected_output: valid values in the timespan [targetLabel +/- valid_within]
            # fourth pair in expected_output: no valid values in the timespan [targetLabel +/- valid_within], return null
            "test_resample_cube_temporal_upsample",
            [
                # these are used here for target, values for data are at the even indices (filter_temporal)
                {"B01": 0, "B02": 9},  # used for data
                {"B01": 1, "B02": 8},
                {"B01": 2, "B02": 7},  # used for data
                {"B01": 3, "B02": 6},
            ],
            [
                # these are used here for target, dates for data are in the json file with process graph
                {"date": "2022-01-01T00:00:00.000Z"},
                {"date": "2022-01-07T00:00:00.000Z"},
                {"date": "2022-01-15T00:00:00.000Z"},
                {"date": "2022-01-28T00:00:00.000Z"},
            ],
            [0, 9, 0, 9, 2, 7, None, None],
        ),
    ],
)
def test_process_graphs_with_scenes(pg_name, example_input, scenes, expected_output):
    process_graph = get_process_graph_json(pg_name)
    result = convert_from_process_graph(process_graph, encode_result=False)

    assert len(result) == 1 and result[0]["invalid_node_id"] is None

    evalscript = result[0]["evalscript"].write()

    output = run_evalscript(evalscript, example_input, scenes)
    output = json.loads(output)

    assert output == expected_output


def test_list_supported_processes():
    known_supported_processes = [
        "load_collection",
        "save_result",
        "reduce_dimension",
        "apply",
        *get_defined_processes_from_files(),
    ]
    supported_processes = list_supported_processes()
    assert len(known_supported_processes) == len(supported_processes)
    assert set(known_supported_processes) == set(supported_processes)


@pytest.mark.parametrize(
    "new_bands",
    [[{"datasource": "node_loadcollection", "bands": ["B01", "B02", "B03"]}]],
)
def test_set_input_bands(new_bands):
    process_graph = get_process_graph_json("bands_null_graph")
    bands_dimension_name = "bands"
    result = convert_from_process_graph(process_graph, bands_dimension_name=bands_dimension_name, encode_result=False)
    evalscript = result[0]["evalscript"]

    assert evalscript.input_bands[0]["bands"] is None
    assert (
        evalscript._output_dimensions[0]["name"] == bands_dimension_name
        and evalscript._output_dimensions[0]["size"] == 0
    )

    with pytest.raises(Exception) as exc:
        evalscript.write()
    assert "input_bands must be set" in str(exc.value)

    evalscript.set_input_bands(new_bands)

    assert evalscript.input_bands == new_bands
    assert evalscript._output_dimensions[0]["name"] == bands_dimension_name and evalscript._output_dimensions[0][
        "size"
    ] == len(new_bands[0]["bands"])

    input_object = get_evalscript_input_object(evalscript.write())
    assert input_object["input"] == new_bands


@pytest.mark.parametrize(
    "process_graph,example_input,expected_output",
    [
        (
            "user_defined_process_fahrenheit",
            [{"B01": -40, "B02": -4}, {"B01": 32, "B02": 50}, {"B01": 68, "B02": 86}, {"B01": 104, "B02": 212}],
            [-40, -20, 0, 10, 20, 30, 40, 100],
        ),
        (
            # The index of the first no-data element in each temporal series is connverted to celsius
            "user_defined_process_find_nodata_convert_to_celsius",
            [{"B01": None, "B02": 2}, {"B01": 3, "B02": 4}, {"B01": 5, "B02": 6}, {"B01": None, "B02": None}],
            [-17.77778, -16.11111],
        ),
    ],
)
def test_user_defined_processes(process_graph, example_input, expected_output):
    process_graph = get_process_graph_json(process_graph)
    result = convert_from_process_graph(
        process_graph, user_defined_processes=user_defined_processes, encode_result=False
    )
    evalscript = result[0]["evalscript"].write()

    output = run_evalscript(evalscript, example_input)
    output = json.loads(output)

    assert pytest.approx(output) == expected_output


@pytest.mark.parametrize(
    "process_graph,expected_output",
    [
        (
            "test_ndvi_s2l2a",
            [],
        )
    ],
)
def test_empty_input(process_graph, expected_output):
    """
    Sentinel Hub Batch runs pre-processing analysis on empty input. Evalscripts should therefore pass without error
    """
    process_graph = get_process_graph_json(process_graph)
    result = convert_from_process_graph(
        process_graph, user_defined_processes=user_defined_processes, bands_metadata=bands_metadata, encode_result=False
    )
    evalscript = result[0]["evalscript"].write()
    try:
        output = run_evalscript(evalscript, [], scenes=[])
        output = json.loads(output)

        assert pytest.approx(output) == expected_output
    except Exception as e:
        raise Exception(e.stderr)


@pytest.mark.parametrize(
    "process_graph,expected_n_output_bands",
    [
        (
            "test_ndvi_with_target_band",
            3,
        ),
        (
            "test_ndvi_without_target_band",
            1,
        ),
    ],
)
def test_ndvi(process_graph, expected_n_output_bands):
    process_graph = get_process_graph_json(process_graph)
    result = convert_from_process_graph(process_graph, encode_result=False)
    evalscript = result[0]["evalscript"].write()
    try:
        output = get_n_output_bands(evalscript)
        assert output["bands"] == expected_n_output_bands
    except Exception as e:
        raise Exception(e.stderr)
