import json

import pytest

from tests.utils import load_process_code, load_datacube_code, run_process, run_input_validation


@pytest.fixture
def aggregate_temporal_period_process_code():
    return load_process_code("aggregate_temporal_period")


@pytest.mark.parametrize(
    "data,period,reducer,dimension,context,scenes,expected_output",
    [
        (
            [{"B01": 1, "B02": 2}],
            "day",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            [{"date": "2020-01-05"}],
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {"labels": ["2020-005"], "name": "t", "type": "temporal"},
                    {"labels": ["B01", "B02"], "name": "bands", "type": "bands"},
                ],
                "data": {"data": [1, 2], "offset": 0, "shape": [1, 2], "stride": [2, 1]},
            },
        ),
        (
            [{"B01": 1, "B02": 2}, {"B01": 11, "B02": 12}],
            "day",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            [{"date": "2020-01-05"}, {"date": "2020-01-07"}],
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {"labels": ["2020-005", "2020-006", "2020-007"], "name": "t", "type": "temporal"},
                    {"labels": ["B01", "B02"], "name": "bands", "type": "bands"},
                ],
                "data": {"data": [6, 7, None, None, 6, 7], "offset": 0, "shape": [3, 2], "stride": [2, 1]},
            },
        ),
        (
            [{"B01": 1, "B02": 2}, {"B01": 11, "B02": 12}],
            "hour",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            [{"date": "2020-01-05T00:00:00.000Z"}, {"date": "2020-01-05T04:00:00.000Z"}],
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {
                        "labels": ["2020-01-05-00", "2020-01-05-01", "2020-01-05-02", "2020-01-05-03", "2020-01-05-04"],
                        "name": "t",
                        "type": "temporal",
                    },
                    {"labels": ["B01", "B02"], "name": "bands", "type": "bands"},
                ],
                "data": {
                    "data": [6, 7, None, None, None, None, None, None, 6, 7],
                    "offset": 0,
                    "shape": [5, 2],
                    "stride": [2, 1],
                },
            },
        ),
        (
            [{"B01": 21, "B02": 22}, {"B01": 31, "B02": 32}],
            "week",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            [{"date": "2020-01-01"}, {"date": "2020-02-15"}],
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {
                        "labels": ["2020-01", "2020-02", "2020-03", "2020-04", "2020-05", "2020-06", "2020-07"],
                        "name": "t",
                        "type": "temporal",
                    },
                    {"labels": ["B01", "B02"], "name": "bands", "type": "bands"},
                ],
                "data": {
                    "data": [26, 27, None, None, None, None, None, None, None, None, None, None, 26, 27],
                    "offset": 0,
                    "shape": [7, 2],
                    "stride": [2, 1],
                },
            },
        ),
        (
            [{"B01": 21, "B02": 22}, {"B01": 31, "B02": 32}],
            "dekad",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            [{"date": "2020-01-01"}, {"date": "2020-02-15"}],
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {
                        "labels": ["2020-01", "2020-02", "2020-03", "2020-04", "2020-05"],
                        "name": "t",
                        "type": "temporal",
                    },
                    {"labels": ["B01", "B02"], "name": "bands", "type": "bands"},
                ],
                "data": {
                    "data": [26, 27, None, None, None, None, None, None, 26, 27],
                    "offset": 0,
                    "shape": [5, 2],
                    "stride": [2, 1],
                },
            },
        ),
        (
            [{"B01": 21, "B02": 22}, {"B01": 31, "B02": 32}],
            "month",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            [{"date": "2020-01-01"}, {"date": "2020-02-15"}],
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {
                        "labels": ["2020-01", "2020-02"],
                        "name": "t",
                        "type": "temporal",
                    },
                    {"labels": ["B01", "B02"], "name": "bands", "type": "bands"},
                ],
                "data": {
                    "data": [26, 27, 26, 27],
                    "offset": 0,
                    "shape": [2, 2],
                    "stride": [2, 1],
                },
            },
        ),
        (
            [{"B01": 21, "B02": 22}, {"B01": 31, "B02": 32}],
            "season",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            [{"date": "2020-01-01"}, {"date": "2020-02-15"}],
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {
                        "labels": ["2020-djf"],
                        "name": "t",
                        "type": "temporal",
                    },
                    {"labels": ["B01", "B02"], "name": "bands", "type": "bands"},
                ],
                "data": {
                    "data": [26, 27],
                    "offset": 0,
                    "shape": [1, 2],
                    "stride": [2, 1],
                },
            },
        ),
        (
            [{"B01": 21, "B02": 22}, {"B01": 31, "B02": 32}],
            "season",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            [{"date": "2020-01-01"}, {"date": "2020-04-15"}],
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {
                        "labels": ["2020-djf", "2020-mam"],
                        "name": "t",
                        "type": "temporal",
                    },
                    {"labels": ["B01", "B02"], "name": "bands", "type": "bands"},
                ],
                "data": {
                    "data": [26, 27, 26, 27],
                    "offset": 0,
                    "shape": [2, 2],
                    "stride": [2, 1],
                },
            },
        ),
        (
            [{"B01": 21, "B02": 22}, {"B01": 31, "B02": 32}],
            "tropical-season",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            [{"date": "2020-01-01"}, {"date": "2020-02-15"}],
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {
                        "labels": ["2020-ndjfma"],
                        "name": "t",
                        "type": "temporal",
                    },
                    {"labels": ["B01", "B02"], "name": "bands", "type": "bands"},
                ],
                "data": {
                    "data": [26, 27],
                    "offset": 0,
                    "shape": [1, 2],
                    "stride": [2, 1],
                },
            },
        ),
        (
            [{"B01": 21, "B02": 22}, {"B01": 31, "B02": 32}],
            "tropical-season",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            [{"date": "2020-01-01"}, {"date": "2020-09-15"}],
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {
                        "labels": ["2020-ndjfma", "2020-mjjaso"],
                        "name": "t",
                        "type": "temporal",
                    },
                    {"labels": ["B01", "B02"], "name": "bands", "type": "bands"},
                ],
                "data": {
                    "data": [26, 27, 26, 27],
                    "offset": 0,
                    "shape": [2, 2],
                    "stride": [2, 1],
                },
            },
        ),
        (
            [{"B01": 21, "B02": 22}],
            "week",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            [{"date": "2020-01-17"}],
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {
                        "labels": ["2020-03"],
                        "name": "t",
                        "type": "temporal",
                    },
                    {"labels": ["B01", "B02"], "name": "bands", "type": "bands"},
                ],
                "data": {
                    "data": [21, 22],
                    "offset": 0,
                    "shape": [1, 2],
                    "stride": [2, 1],
                },
            },
        ),
        (
            [{"B01": 21, "B02": 22}],
            "dekad",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            [{"date": "2020-01-17"}],
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {
                        "labels": ["2020-02"],
                        "name": "t",
                        "type": "temporal",
                    },
                    {"labels": ["B01", "B02"], "name": "bands", "type": "bands"},
                ],
                "data": {
                    "data": [21, 22],
                    "offset": 0,
                    "shape": [1, 2],
                    "stride": [2, 1],
                },
            },
        ),
        (
            [{"B01": 21, "B02": 22}],
            "month",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            [{"date": "2020-01-17"}],
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {
                        "labels": ["2020-01"],
                        "name": "t",
                        "type": "temporal",
                    },
                    {"labels": ["B01", "B02"], "name": "bands", "type": "bands"},
                ],
                "data": {
                    "data": [21, 22],
                    "offset": 0,
                    "shape": [1, 2],
                    "stride": [2, 1],
                },
            },
        ),
        (
            [{"B01": 21, "B02": 22}],
            "decade",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            [{"date": "2020-01-12"}],
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {
                        "labels": ["2020"],
                        "name": "t",
                        "type": "temporal",
                    },
                    {"labels": ["B01", "B02"], "name": "bands", "type": "bands"},
                ],
                "data": {
                    "data": [21, 22],
                    "offset": 0,
                    "shape": [1, 2],
                    "stride": [2, 1],
                },
            },
        ),
        (
            [{"B01": 21, "B02": 22}],
            "decade-ad",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0)",
            None,
            None,
            [{"date": "2020-01-12"}],
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {
                        "labels": ["2021"],
                        "name": "t",
                        "type": "temporal",
                    },
                    {"labels": ["B01", "B02"], "name": "bands", "type": "bands"},
                ],
                "data": {
                    "data": [21, 22],
                    "offset": 0,
                    "shape": [1, 2],
                    "stride": [2, 1],
                },
            },
        ),
    ],
)
def test_aggregate_temporal_period(
    aggregate_temporal_period_process_code,
    data,
    period,
    reducer,
    dimension,
    context,
    scenes,
    expected_output,
):
    additional_js_code_to_run = (
        load_datacube_code() + f"let cube = new DataCube({json.dumps(data)}, 'bands', 't', true, [], {scenes});"
    )
    process_arguments = f"{{'data': cube, 'period': {json.dumps(period)}, 'reducer': {reducer}, 'dimension': {json.dumps(dimension)}, 'context': {json.dumps(context)}}}"
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
            "day",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val), 0)",
            None,
            None,
            "cube.getDimensionByName(cube.temporal_dimension_name).labels = ['2020-01-05'];",
            False,
            None,
        ),
        (
            [{"B01": 1, "B02": 2}],
            "day",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val), 0)",
            None,
            None,
            "cube = undefined;",
            True,
            "MISSING_PARAMETER",
        ),
        (
            [{"B01": 1, "B02": 2}],
            "day",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val), 0)",
            None,
            None,
            "cube = null;",
            True,
            "NOT_NULL",
        ),
        (
            [{"B01": 1, "B02": 2}],
            True,
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val), 0)",
            None,
            None,
            None,
            True,
            "WRONG_TYPE",
        ),
        (
            [{"B01": 1, "B02": 2}],
            12.432,
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val), 0)",
            None,
            None,
            None,
            True,
            "WRONG_TYPE",
        ),
        (
            [{"B01": 1, "B02": 2}],
            None,
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val), 0)",
            None,
            None,
            None,
            True,
            "NOT_NULL",
        ),
        (
            [{"B01": 1, "B02": 2}],
            "day",
            None,
            None,
            None,
            None,
            True,
            "NOT_NULL",
        ),
        (
            [{"B01": 1, "B02": 2}],
            "day",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val), 0)",
            12.354,
            None,
            None,
            True,
            "WRONG_TYPE",
        ),
        (
            [{"B01": 1, "B02": 2}],
            "day",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val), 0)",
            [12, 34, 56],
            None,
            None,
            True,
            "WRONG_TYPE",
        ),
        (
            [{"B01": 1, "B02": 2}],
            "day",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val), 0)",
            None,
            None,
            "cube.addDimension('new_temporal_name', 'new_temporal_label', cube.TEMPORAL);",
            True,
            "TooManyDimensions",
        ),
        (
            [{"B01": 1, "B02": 2}],
            "day",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val), 0)",
            "wrong_dimension_name",
            None,
            None,
            True,
            "DimensionNotAvailable",
        ),
        (
            [{"B01": 1, "B02": 2}],
            "unknown_period",
            "({data, context}) => data.reduce((acc, val, i, arr) => (acc + val), 0)",
            None,
            None,
            "cube.getDimensionByName(cube.temporal_dimension_name).labels = ['2020-01-05'];",
            True,
            "Value 'unknown_period' is not an allowed value for period.",
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
    process_arguments = f"{{'data': cube, 'period': {json.dumps(period)}, 'reducer': {reducer if type(reducer) is str else json.dumps(reducer)}, 'dimension': {json.dumps(dimension)}, 'context': {json.dumps(context)}}}"
    run_input_validation(
        aggregate_temporal_period_process_code + additional_js_code_to_run,
        "aggregate_temporal_period",
        process_arguments,
        raises_exception,
        error_name,
    )
