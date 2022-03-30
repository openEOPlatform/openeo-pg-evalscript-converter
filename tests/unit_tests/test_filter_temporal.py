import json

import pytest

from tests.utils import load_process_code, load_datacube_code, run_process


@pytest.fixture
def filter_temporal_process_code():
    return load_process_code("filter_temporal")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        # temporal extent inludes all data
        (
            {
                "data": [{"B01": 1, "B02": 2, "B03": 3}, {"B01": 11, "B02": 12, "B03": 13}, {"B01": 21, "B02": 22, "B03": 23}],
                "scenes": [
                    {"date":"2022-03-21T00:00:00.000Z"},
                    {"date":"2022-03-19T00:00:00.000Z"},
                    {"date":"2022-03-16T00:00:00.000Z"},
                ],
                "extent": [
                    "2022-03-10T00:00:00.000Z",
                    "2022-03-25T00:00:00.000Z",
                ],
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                'dimensions': [
                    {'labels': ['2022-03-21T00:00:00.000Z', '2022-03-19T00:00:00.000Z', '2022-03-16T00:00:00.000Z'], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': ['B01', 'B02', 'B03'], 'name': 'bands_name', 'type': 'bands'}
                ],
                'data': {
                    'data': [1, 2, 3, 11, 12, 13, 21, 22, 23],
                    'offset': 0,
                    'shape': [3, 3],
                    'stride': [3, 1]
                }
            },
        ),
        # temporal extent is within data range, but includes no data (note it's left-closed)
        (
            {
                "data": [{"B01": 1, "B02": 2, "B03": 3}, {"B01": 11, "B02": 12, "B03": 13}, {"B01": 21, "B02": 22, "B03": 33}],
                "scenes": [
                    {"date":"2022-03-21T00:00:00.000Z"},
                    {"date":"2022-03-19T00:00:00.000Z"},
                    {"date":"2022-03-16T00:00:00.000Z"},
                ],
                "extent": [
                    "2022-03-17T00:00:00.000Z",
                    "2022-03-19T00:00:00.000Z",
                ],
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                'dimensions': [
                    {'labels': [], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': ['B01', 'B02', 'B03'], 'name': 'bands_name', 'type': 'bands'}
                ],
                'data': {
                    'data': [],
                    'offset': 0,
                    'shape': [0, 3],
                    'stride': [3, 1]
                }
            },
        ),
        # temporal extent is out of data range, includes no data (note it's left-closed)
        (
            {
                "data": [{"B01": 1, "B02": 2, "B03": 3}, {"B01": 11, "B02": 12, "B03": 13}, {"B01": 21, "B02": 22, "B03": 33}],
                "scenes": [
                    {"date":"2022-03-21T00:00:00.000Z"},
                    {"date":"2022-03-19T00:00:00.000Z"},
                    {"date":"2022-03-16T00:00:00.000Z"},
                ],
                "extent": [
                    "2022-03-10T00:00:00.000Z",
                    "2022-03-16T00:00:00.000Z",
                ],
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                'dimensions': [
                    {'labels': [], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': ['B01', 'B02', 'B03'], 'name': 'bands_name', 'type': 'bands'}
                ],
                'data': {
                    'data': [],
                    'offset': 0,
                    'shape': [0, 3],
                    'stride': [3, 1]
                }
            },
        ),
        # temporal extent inludes end of data range (note it's left-closed)
        (
            {
                "data": [{"B01": 1, "B02": 2, "B03": 3}, {"B01": 11, "B02": 12, "B03": 13}, {"B01": 21, "B02": 22, "B03": 33}],
                "scenes": [
                    {"date":"2022-03-21T00:00:00.000Z"},
                    {"date":"2022-03-19T00:00:00.000Z"},
                    {"date":"2022-03-16T00:00:00.000Z"},
                ],
                "extent": [
                    "2022-03-19T00:00:00.000Z",
                    "2022-03-25T00:00:00.000Z",
                ],
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                'dimensions': [
                    {'labels': ['2022-03-21T00:00:00.000Z', '2022-03-19T00:00:00.000Z'], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': ['B01', 'B02', 'B03'], 'name': 'bands_name', 'type': 'bands'}
                ],
                'data': {
                    'data': [1, 2, 3, 11, 12, 13],
                    'offset': 0,
                    'shape': [2, 3],
                    'stride': [3, 1]
                }
            },
        ),
        # temporal extent includes middle of data range
        (
            {
                "data": [{"B01": 1, "B02": 2, "B03": 3}, {"B01": 11, "B02": 12, "B03": 13}, {"B01": 21, "B02": 22, "B03": 33}],
                "scenes": [
                    {"date":"2022-03-21T00:00:00.000Z"},
                    {"date":"2022-03-19T00:00:00.000Z"},
                    {"date":"2022-03-16T00:00:00.000Z"},
                ],
                "extent": [
                    "2022-03-18T00:00:00.000Z",
                    "2022-03-20T00:00:00.000Z",
                ],
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                'dimensions': [
                    {'labels': ['2022-03-19T00:00:00.000Z'], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': ['B01', 'B02', 'B03'], 'name': 'bands_name', 'type': 'bands'}
                ],
                'data': {
                    'data': [11, 12, 13],
                    'offset': 0,
                    'shape': [1, 3],
                    'stride': [3, 1]
                }
            },
        ),
        # temporal extent includes start of data range (note it's left-closed)
        (
            {
                "data": [{"B01": 1, "B02": 2, "B03": 3}, {"B01": 11, "B02": 12, "B03": 13}, {"B01": 21, "B02": 22, "B03": 23}],
                "scenes": [
                    {"date":"2022-03-21T00:00:00.000Z"},
                    {"date":"2022-03-19T00:00:00.000Z"},
                    {"date":"2022-03-16T00:00:00.000Z"},
                ],
                "extent": [
                    "2022-03-16T00:00:00.000Z",
                    "2022-03-19T00:00:00.000Z",
                ],
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                'dimensions': [
                    {'labels': ['2022-03-16T00:00:00.000Z'], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': ['B01', 'B02', 'B03'], 'name': 'bands_name', 'type': 'bands'}
                ],
                'data': {
                    'data': [21, 22, 23],
                    'offset': 0,
                    'shape': [1, 3],
                    'stride': [3, 1]
                }
            },
        ),
        # temporal extent includes minimum range to include all data (note it's right-closed)
        (
            {
                "data": [{"B01": 1, "B02": 2, "B03": 3}, {"B01": 11, "B02": 12, "B03": 13}, {"B01": 21, "B02": 22, "B03": 23}],
                "scenes": [
                    {"date":"2022-03-21T00:00:00.000Z"},
                    {"date":"2022-03-19T00:00:00.000Z"},
                    {"date":"2022-03-16T00:00:00.000Z"},
                ],
                "extent": [
                    "2022-03-16T00:00:00.000Z",
                    "2022-03-21T00:00:00.001Z",
                ],
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                'dimensions': [
                    {'labels': ['2022-03-21T00:00:00.000Z', '2022-03-19T00:00:00.000Z', '2022-03-16T00:00:00.000Z'], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': ['B01', 'B02', 'B03'], 'name': 'bands_name', 'type': 'bands'}
                ],
                'data': {
                    'data': [1, 2, 3, 11, 12, 13, 21, 22, 23],
                    'offset': 0,
                    'shape': [3, 3],
                    'stride': [3, 1]
                }
            },
        ),
    ],
)
def test_filter_temporal(filter_temporal_process_code, example_input, expected_output):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube = new DataCube({example_input['data']}, 'bands_name', 'temporal_name', true, {example_input['scenes']});"
    )
    process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube}}"
    output = run_process(
        filter_temporal_process_code + additional_js_code_to_run,
        "filter_temporal",
        process_arguments,
    )
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
         (
            {
                "data": [{"B01": 1}],
                "scenes": [
                    {"date":"2022-03-16T00:00:00.000Z"},
                ],
                "extent": [
                    "2022-03-10T00:00:00.000Z",
                    "2022-03-25T00:00:00.000Z",
                ],
            },
            False,
            None,
        ),
        (
            {
                "data": [{"B01": 1}],
                "scenes": [
                    {"date":"2022-03-16T00:00:00.000Z"},
                ],
            },
            True,
            "MISSING_PARAMETER"
        ),
        (
            {
                "data": [{"B01": 1}],
                "scenes": [
                    {"date":"INVALID_DATE_FORMAT"},
                ],
                "extent": [
                    "2022-03-10T00:00:00.000Z",
                    "2022-03-25T00:00:00.000Z",
                ],
            },
            True,
            "Invalid ISO date string in temporal dimension label.",
        ),
        (
            {
                "data": [{"B01": 1}],
                "scenes": [
                    {"date":"2022-03-16T00:00:00.000Z"},
                ],
                "extent": [],
            },
            True,
            "Invalid temporal extent. Temporal extent must be an array of exactly two ISO date strings."
        ),
        (
            {
                "data": [{"B01": 1}],
                "scenes": [
                    {"date":"2022-03-16T00:00:00.000Z"},
                ],
                "extent": [
                    "2022-03-10T00:00:00.000Z",
                ],
            },
            True,
            "Invalid temporal extent. Temporal extent must be an array of exactly two ISO date strings."
        ),
        (
            {
                "data": [{"B01": 1}],
                "scenes": [
                    {"date":"2022-03-16T00:00:00.000Z"},
                ],
                "extent": [
                    "2022-03-10T00:00:00.000Z",
                    "2022-03-10T00:00:00.000Z",
                    "2022-03-25T00:00:00.000Z",
                ],
            },
            True,
            "Invalid temporal extent. Temporal extent must be an array of exactly two ISO date strings."
        ),
        (
            {
                "data": [{"B01": 1}],
                "scenes": [
                    {"date":"2022-03-16T00:00:00.000Z"},
                ],
                "extent": [
                    "2022-03-10T00:00:00.000Z",
                    "2022-03-25T00:00:00.000Z",
                ],
                "dimension": "temporal"
            },
            False,
            None,
        ),
        (
            {
                "data": [{"B01": 1}],
                "scenes": [
                    {"date":"2022-03-16T00:00:00.000Z"},
                ],
                "extent": [
                    "2022-03-10T00:00:00.000Z",
                    "2022-03-25T00:00:00.000Z",
                ],
                "dimension": 15
            },
            True,
            "WRONG_TYPE",
        ),
    ],
)
def test_filter_temporal_exceptions(filter_temporal_process_code, example_input, raises_exception, error_message):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube = new DataCube({example_input['data']}, 'bands_name', 'temporal_name', true, {example_input['scenes']});"
    )
    process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube}}"
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(
                filter_temporal_process_code + additional_js_code_to_run,
                "filter_temporal",
                process_arguments,
            )
        assert error_message in str(exc.value)

    else:
        run_process(
            filter_temporal_process_code + additional_js_code_to_run,
            "filter_temporal",
            process_arguments,
        )
        