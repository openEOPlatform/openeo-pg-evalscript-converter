import json

import pytest

from tests.utils import load_process_code, load_datacube_code, run_process


@pytest.fixture
def aggregate_temporal_process_code():
    return load_process_code("aggregate_temporal")

@pytest.fixture
def data():
    return [
        {"B01": 16, "B02": 6},
        {"B01": 17, "B02": 5},
        {"B01": 18, "B02": 4},
        {"B01": 19, "B02": 3},
        {"B01": 20, "B02": 2},
        {"B01": 21, "B02": 1},
    ]

@pytest.fixture
def scenes():
    return [
        {"date":"2022-03-16T00:00:00.000Z"},
        {"date":"2022-03-17T00:00:00.000Z"},
        {"date":"2022-03-18T00:00:00.000Z"},
        {"date":"2022-03-19T00:00:00.000Z"},
        {"date":"2022-03-20T00:00:00.000Z"},
        {"date":"2022-03-21T00:00:00.000Z"},
    ]


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        (
            {
                "intervals": [
                    [ "2022-03-16T00:00:00.000Z", "2022-03-18T00:00:00.000Z" ],
                    [ "2022-03-18T00:00:00.000Z", "2022-03-22T00:00:00.000Z" ],
                ],
                "reducer": "({data})=>{ return data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0) }",
            },
            {
                'dimensions': [
                    {'labels': ['2022-03-16T00:00:00.000Z', '2022-03-18T00:00:00.000Z'], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': ['B01', 'B02'], 'name': 'bands_name', 'type': 'bands'}
                ],
                'data': {
                    'data': [16.5, 5.5, 19.5, 2.5],
                }
            },
        ),
        (
            {
                "intervals": [
                    [ "2022-03-16T00:00:00.000Z", "2022-03-18T00:00:00.000Z" ],
                    [ "2022-03-18T00:00:00.000Z", "2022-03-22T00:00:00.000Z" ],
                ],
                "labels": [ "interval1", "interval2" ],
                "reducer": "({data})=>{ return data.reduce((acc, val, i, arr) => (acc + val / arr.length), 0) }",
                "dimension": "temporal_name",
            },
            {
                'dimensions': [
                    {'labels': ['interval1', 'interval2'], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': ['B01', 'B02'], 'name': 'bands_name', 'type': 'bands'}
                ],
                'data': {
                    'data': [16.5, 5.5, 19.5, 2.5],
                }
            },
        ),
    ],
)
def test_aggregate_temporal(aggregate_temporal_process_code, data, scenes, example_input, expected_output):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube = new DataCube({data}, 'bands_name', 'temporal_name', true, {scenes});"
    )
    process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube, 'scenes': {scenes}, 'reducer': {example_input['reducer']}}}"
    output = run_process(
        aggregate_temporal_process_code + additional_js_code_to_run,
        "aggregate_temporal",
        process_arguments,
    )
    output = json.loads(output)
    assert output['dimensions'] == expected_output['dimensions']
    assert output['data']['data'] == expected_output['data']['data']


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
    ],
)
def test_aggregate_temporal_exceptions(aggregate_temporal_process_code, example_input, raises_exception, error_message):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube = new DataCube({example_input['data']}, 'bands_name', 'temporal_name', true, {example_input['scenes']});"
    )
    process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube}}"
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(
                aggregate_temporal_process_code + additional_js_code_to_run,
                "aggregate_temporal",
                process_arguments,
            )
        assert error_message in str(exc.value)

    else:
        run_process(
            aggregate_temporal_process_code + additional_js_code_to_run,
            "aggregate_temporal",
            process_arguments,
        )
