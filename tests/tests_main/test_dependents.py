import json
from collections import defaultdict

import pytest

from pg_to_evalscript.process_graph_utils import get_dependencies, get_dependents, get_execution_order


process_graph = {
    "loadco1": {
        "process_id": "load_collection",
        "arguments": {
            "id": "S2L1C",
            "spatial_extent": {"west": 16.1, "east": 16.6, "north": 48.6, "south": 47.2},
            "temporal_extent": ["2022-01-01", "2022-02-01"],
            "bands": ["B01", "B02"],
        },
    },
    "filter_every_second": {
        "process_id": "apply_dimension",
        "arguments": {
            "data": {"from_node": "loadco1"},
            "process": {
                "process_graph": {
                    "filter": {
                        "process_id": "array_filter",
                        "arguments": {
                            "data": {"from_parameter": "data"},
                            "condition": {
                                "process_graph": {
                                    "mod2": {
                                        "process_id": "mod",
                                        "arguments": {"x": {"from_parameter": "index"}, "y": 2},
                                    },
                                    "iseven": {
                                        "process_id": "eq",
                                        "arguments": {"x": {"from_node": "mod2"}, "y": 0},
                                        "result": True,
                                    },
                                }
                            },
                        },
                        "result": True,
                    }
                }
            },
            "dimension": "t",
        },
    },
    "rename_labels1": {
        "process_id": "rename_labels",
        "arguments": {
            "data": {"from_node": "filter_every_second"},
            "dimension": "t",
            "target": ["2022-01-03", "2022-01-20"],
        },
    },
    "resample": {
        "process_id": "resample_cube_temporal",
        "arguments": {"data": {"from_node": "loadco1"}, "target": {"from_node": "rename_labels1"}, "valid_within": 4},
    },
    "saveresult1": {
        "process_id": "save_result",
        "arguments": {"data": {"from_node": "resample"}, "format": "png"},
        "result": True,
    },
}


def test_get_dependents():
    n_repeats = 10000
    prev_dependents = None
    prev_dependency_graph = None
    prev_execution_order = None

    for i in range(n_repeats):
        dependency_graph = get_dependencies(process_graph)
        if prev_dependency_graph is not None:
            assert prev_dependency_graph == dependency_graph
        dependents = get_dependents(dependency_graph)
        if prev_dependents is not None:
            assert prev_dependents == dependents
        execution_order = get_execution_order(dependency_graph, dependents)
        if prev_execution_order is not None:
            assert prev_execution_order == execution_order
        prev_dependency_graph = dependency_graph
        prev_dependents = dependents
        prev_execution_order = execution_order
