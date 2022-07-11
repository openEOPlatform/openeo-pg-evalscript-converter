from collections import defaultdict

import pytest

from pg_to_evalscript.process_graph_utils import get_execution_order


def generate_default_dict_from_dict(d):
    default_d = defaultdict(set)
    for k, v in d.items():
        default_d[k] = v
    return default_d


@pytest.mark.parametrize(
    "dependency_graph,dependents,possible_exection_orders",
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
            [["loadco1", "filter_every_second", "rename_labels1", "resample", "saveresult1"]],
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
            [["loadco1", "filter_every_second", "rename_labels1", "resample", "saveresult1"]],
        ),
        (
            generate_default_dict_from_dict(
                {
                    "loadco1": set(),
                    "filter_every_second": {"loadco1"},
                    "filter_labels": {"loadco1"},
                    "rename_labels1": {"filter_every_second", "filter_labels"},
                    "resample": {"rename_labels1", "loadco1"},
                    "saveresult1": {"resample"},
                }
            ),
            generate_default_dict_from_dict(
                {
                    "loadco1": {"filter_every_second", "resample", "filter_labels"},
                    "filter_every_second": {"rename_labels1"},
                    "filter_labels": {"rename_labels1"},
                    "rename_labels1": {"resample"},
                    "resample": {"saveresult1"},
                }
            ),
            [
                ["loadco1", "filter_every_second", "filter_labels", "rename_labels1", "resample", "saveresult1"],
                ["loadco1", "filter_labels", "filter_every_second", "rename_labels1", "resample", "saveresult1"],
            ],
        ),
    ],
)
def test_execution_order(dependency_graph, dependents, possible_exection_orders):
    execution_order = get_execution_order(dependency_graph, dependents)
    assert execution_order in possible_exection_orders


@pytest.mark.parametrize(
    "dependency_graph,dependents,error",
    [
        (
            generate_default_dict_from_dict(
                {
                    "loadco1": set(),
                    "filterbbox1": {"loadco1"},
                    "ndv1": {"filterbbox1"},
                    "filterbbox2": {"ndvi1"},
                    "saveres1": {"filterbbox2"},
                }
            ),
            generate_default_dict_from_dict(
                {
                    "loadco1": {"filterbbox1"},
                    "filterbbox1": {"ndv1"},
                    "ndvi1": {"filterbbox2"},
                    "filterbbox2": {"saveres1"},
                }
            ),
            "Execution order of process graph nodes cannot be constructed.",
        )
    ],
)
def test_execution_order_error(dependency_graph, dependents, error):
    try:
        execution_order = get_execution_order(dependency_graph, dependents)
    except Exception as e:
        assert error in str(e)
    else:
        assert False, "Test expected an error, but no exception was raised."
