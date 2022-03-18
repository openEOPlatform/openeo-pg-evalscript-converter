import json

import pytest
from pg_to_evalscript import convert_from_process_graph, list_supported_processes

from tests.utils import (
    get_process_graph_json,
    run_evalscript,
    get_defined_processes_from_files,
    get_evalscript_input_object,
)


@pytest.mark.parametrize(
    "pg_name,example_input,expected_output",
    [
        ("test_graph_1", [{"B01": 3, "B02": 3}, {"B01": 5, "B02": 1}], [4, 2]),
        ("reduce_mean_one_band", [{"B01": 3}, {"B01": 5}], [4]),
        ("reduce_mean_one_band", [{"B01": 3}], [3]),
        ("reduce_mean_one_band", [{"B01": 3}, {"B01": 5}, {"B01": 10}, {"B01": 6}], [6]),
        ("test_short_graph", [{"B01": 3, "B02": 2}, {"B01": 5, "B02": 1}], [3, 2, 5, 1]),
        ("test_apply_absolute", [{"B01": 0.1, "B02": -0.15}, {"B01": 0, "B02": 2}], [0.1, 0.15, 0, 2]),
        (
            "test_apply_math",
            [{"B01": 0, "B02": 1}, {"B01": -1, "B02": 0.5}, {"B01": None, "B02": None}],
            [-0.75, 0, -1.5, -0.375, None, None],
        ),
        (
            "test_apply_linear_scale_range",
            [{"B01": 0.5, "B02": 0.75}, {"B01": 0, "B02": 1}, {"B01": -3, "B02": 4}, {"B01": None, "B02": None}],
            [1, 1.5, 0, 2, 0, 2, None, None],
        ),
        (
            "test_count_with_condition",
            [{"B01": 0, "B02": 1}, {"B01": 2, "B02": 3}, {"B01": 4, "B02": 5}, {"B01": None, "B02": None}],
            [1, 2],
        ),
        (
            "test_count_without_condition",
            [{"B01": 0, "B02": 1}, {"B01": 2, "B02": 3}, {"B01": 4, "B02": 5}, {"B01": None, "B02": 3}],
            [3, 4],
        ),
        (
            "test_array_apply_add",
            [{"B01": 0, "B02": 1, "B03": 2, "B04": 3, "B05": 4, "B06": 5}],
            [10, 11, 12, 13, 14, 15],
        ),
        ("test_array_filter", [{"B01": 0}, {"B01": 1}, {"B01": 2}, {"B01": 4}, {"B01": 5}], [11]),
    ],
)
def test_convertable_process_graphs(pg_name, example_input, expected_output):
    process_graph = get_process_graph_json(pg_name)
    result = convert_from_process_graph(process_graph, encode_result=False)

    assert len(result) == 1 and result[0]["invalid_node_id"] is None

    evalscript = result[0]["evalscript"].write()
    output = run_evalscript(evalscript, example_input)
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
    [["B01", "B02", "B03"]],
)
def test_set_input_bands(new_bands):
    process_graph = get_process_graph_json("bands_null_graph")
    bands_dimension_name = "bands"
    result = convert_from_process_graph(process_graph, bands_dimension_name=bands_dimension_name, encode_result=False)
    evalscript = result[0]["evalscript"]

    assert evalscript.input_bands is None
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
    ] == len(new_bands)

    input_object = get_evalscript_input_object(evalscript.write())
    assert input_object["input"] == new_bands
