import pytest

from src.pg_to_evalscript import convert_from_process_graph

from tests.utils import get_process_graph_json


@pytest.mark.parametrize(
    "process_graph,expected_output_dimensions",
    [
        (
            "test_apply_filter_merge",
            [{"name": "bands", "size": 2}, {"name": "t", "size": None, "original_temporal": True}],
        )
    ],
)
def test_determine_output_dimensions(process_graph, expected_output_dimensions):
    pg = get_process_graph_json(process_graph)
    evalscript = convert_from_process_graph(pg)[0]["evalscript"]
    output_dimensions = evalscript.determine_output_dimensions()

    assert len(output_dimensions) == len(expected_output_dimensions)
    for i in range(len(expected_output_dimensions)):
        assert output_dimensions[i]["name"] == expected_output_dimensions[i]["name"]
        assert output_dimensions[i]["size"] == expected_output_dimensions[i]["size"]
        assert output_dimensions[i].get("original_temporal", False) == expected_output_dimensions[i].get(
            "original_temporal", False
        )
