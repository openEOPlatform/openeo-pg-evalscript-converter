from collections import defaultdict

import pytest

from pg_to_evalscript.process_graph_utils import get_execution_order
from tests.utils import get_process_graph_json


def generate_default_dict_from_dict(d):
    default_d = defaultdict(set)
    for k, v in d.items():
        default_d[k] = v
    return default_d


@pytest.mark.parametrize(
    "dependency_graph,dependents,expected_exection_order",
    [
        (
            generate_default_dict_from_dict(
                {
                    "loadco1": set(),
                    "filter_every_second": {"loadco1"},
                    "rename_labels1": {"filter_every_second"},
                    "resample": {"loadco1", "rename_labels1"},
                    "saveresult1": {"resample"},
                }
            ),
            generate_default_dict_from_dict(
                {
                    "loadco1": {"resample", "filter_every_second"},
                    "filter_every_second": {"rename_labels1"},
                    "rename_labels1": {"resample"},
                    "resample": {"saveresult1"},
                }
            ),
            ["loadco1", "filter_every_second", "rename_labels1", "resample", "saveresult1"],
        ),
        (
            generate_default_dict_from_dict(
                {
                    "loadco1": set(),
                    "filter_every_second": {"loadco1"},
                    "rename_labels1": {"filter_every_second"},
                    "resample": {"loadco1", "rename_labels1"},
                    "saveresult1": {"resample"},
                }
            ),
            generate_default_dict_from_dict(
                {
                    "loadco1": {"filter_every_second", "resample"},
                    "filter_every_second": {"rename_labels1"},
                    "rename_labels1": {"resample"},
                    "resample": {"saveresult1"},
                }
            ),
            ["loadco1", "filter_every_second", "rename_labels1", "resample", "saveresult1"],
        ),
    ],
)
def test_execution_order(dependency_graph, dependents, expected_exection_order):
    execution_order = get_execution_order(dependency_graph, dependents)
    assert execution_order == expected_exection_order
