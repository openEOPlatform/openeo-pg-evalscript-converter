import json

import pytest

from tests.utils import load_process_code, load_datacube_code, run_process, run_input_validation


@pytest.fixture
def aggregate_temporal_period_process_code():
    return load_process_code("aggregate_temporal_period")


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.parametrize(
    "data,period,reducer,dimension,context,expected_output",
    [
        (
            [{"B01": 1, "B02": 2}],
            "",
            "({{data, context}}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {"labels": [], "name": "t", "type": "temporal"},
                    {"labels": ["B01", "B02"], "name": "bands", "type": "bands"},
                ],
                "data": {"data": [1, 2], "offset": 0, "shape": [1, 2], "stride": [2, 1]},
            },
        ),
    ],
)
def test_aggregate_temporal_period(
    aggregate_temporal_period_process_code, data, period, reducer, dimension, context, expected_output
):
    additional_js_code_to_run = (
        load_datacube_code() + f"let cube = new DataCube({json.dumps(data)}, 'bands', 't', true);"
    )
    process_arguments = f"{{'data': cube, 'period': {json.dumps(period)}, 'reducer': {json.dumps(reducer)}, 'dimension': {json.dumps(dimension)}, 'context': {json.dumps(context)}}}"
    output = run_process(
        aggregate_temporal_period_process_code + additional_js_code_to_run,
        "aggregate_temporal_period",
        process_arguments,
    )
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "data,period,reducer,dimension,context,additional_code_specific_to_test_case,raises_exception,error_name",
    [
        (
            [{"B01": 1, "B02": 2}],
            "period",
            "({{data, context}}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            None,
            False,
            None,
        ),
        (
            [{"B01": 1, "B02": 2}],
            "period",
            "({{data, context}}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            "cube = undefined;",
            True,
            "MISSING_PARAMETER",
        ),
        (
            [{"B01": 1, "B02": 2}],
            "period",
            "({{data, context}}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            "cube = null;",
            True,
            "NOT_NULL",
        ),
        (
            [{"B01": 1, "B02": 2}],
            True,
            "({{data, context}}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            None,
            True,
            "WRONG_TYPE",
        ),
        (
            [{"B01": 1, "B02": 2}],
            12.432,
            "({{data, context}}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            None,
            True,
            "WRONG_TYPE",
        ),
        (
            [{"B01": 1, "B02": 2}],
            None,
            "({{data, context}}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            None,
            True,
            "NOT_NULL",
        ),
        (
            [{"B01": 1, "B02": 2}],
            "period",
            None,
            None,
            None,
            None,
            True,
            "NOT_NULL",
        ),
        (
            [{"B01": 1, "B02": 2}],
            "period",
            "({{data, context}}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            12.354,
            None,
            None,
            True,
            "WRONG_TYPE",
        ),
        (
            [{"B01": 1, "B02": 2}],
            "period",
            "({{data, context}}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            [12,34,56],
            None,
            None,
            True,
            "WRONG_TYPE",
        ),
        (
            [{"B01": 1, "B02": 2}],
            "period",
            "({{data, context}}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            "cube.addDimension('new_temporal_name', 'new_temporal_label', cube.TEMPORAL);",
            True,
            "TooManyDimensions",
        ),
        (
            [{"B01": 1, "B02": 2}],
            "period",
            "({{data, context}}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            "wrong_dimension_name",
            None,
            None,
            True,
            "DimensionNotAvailable",
        ),
    ],
)
def test_aggregate_temporal_period_exceptions(
    aggregate_temporal_period_process_code,
    data,
    period,
    reducer,
    dimension,
    context,
    additional_code_specific_to_test_case,
    raises_exception,
    error_name,
):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"let cube = new DataCube({json.dumps(data)}, 'bands', 't', true);"
        + (additional_code_specific_to_test_case or "")
    )
    process_arguments = f"{{'data': cube, 'period': {json.dumps(period)}, 'reducer': {json.dumps(reducer)}, 'dimension': {json.dumps(dimension)}, 'context': {json.dumps(context)}}}"
    run_input_validation(
        aggregate_temporal_period_process_code + additional_js_code_to_run,
        "aggregate_temporal_period",
        process_arguments,
        raises_exception,
        error_name,
    )
