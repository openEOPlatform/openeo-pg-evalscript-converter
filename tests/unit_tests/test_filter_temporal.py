import json

import pytest

from tests.utils import load_process_code, load_datacube_code, run_process, run_input_validation


@pytest.fixture
def filter_temporal_process_code():
    return load_process_code("filter_temporal")


@pytest.fixture
def data():
    return [{"B01": 1, "B02": 2, "B03": 3}, {"B01": 11, "B02": 12, "B03": 13}, {"B01": 21, "B02": 22, "B03": 23}]


@pytest.fixture
def scenes():
    return [
        {"date": "2022-03-21T00:00:00.000Z"},
        {"date": "2022-03-19T00:00:00.000Z"},
        {"date": "2022-03-16T00:00:00.000Z"},
    ]


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        # temporal extent inludes all data
        (
            {
                "extent": [
                    "2022-03-10T00:00:00.000Z",
                    "2022-03-25T00:00:00.000Z",
                ],
            },
            {
                "dimensions": [
                    {
                        "labels": ["2022-03-21T00:00:00.000Z", "2022-03-19T00:00:00.000Z", "2022-03-16T00:00:00.000Z"],
                        "name": "temporal_name",
                        "type": "temporal",
                    },
                    {"labels": ["B01", "B02", "B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": {
                    "data": [1, 2, 3, 11, 12, 13, 21, 22, 23],
                },
            },
        ),
        # temporal extent is within data range, but includes no data (note it's left-closed)
        (
            {
                "extent": [
                    "2022-03-17T00:00:00.000Z",
                    "2022-03-19T00:00:00.000Z",
                ],
            },
            {
                "dimensions": [
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B01", "B02", "B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": {
                    "data": [],
                },
            },
        ),
        # temporal extent is out of data range, includes no data (note it's left-closed)
        (
            {
                "extent": [
                    "2022-03-10T00:00:00.000Z",
                    "2022-03-16T00:00:00.000Z",
                ],
            },
            {
                "dimensions": [
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B01", "B02", "B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": {
                    "data": [],
                },
            },
        ),
        # temporal extent inludes end of data range (note it's left-closed)
        (
            {
                "extent": [
                    "2022-03-19T00:00:00.000Z",
                    "2022-03-25T00:00:00.000Z",
                ],
            },
            {
                "dimensions": [
                    {
                        "labels": ["2022-03-21T00:00:00.000Z", "2022-03-19T00:00:00.000Z"],
                        "name": "temporal_name",
                        "type": "temporal",
                    },
                    {"labels": ["B01", "B02", "B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": {
                    "data": [1, 2, 3, 11, 12, 13],
                },
            },
        ),
        # temporal extent includes middle of data range
        (
            {
                "extent": [
                    "2022-03-18T00:00:00.000Z",
                    "2022-03-20T00:00:00.000Z",
                ],
            },
            {
                "dimensions": [
                    {"labels": ["2022-03-19T00:00:00.000Z"], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B01", "B02", "B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": {
                    "data": [11, 12, 13],
                },
            },
        ),
        # temporal extent includes start of data range (note it's left-closed)
        (
            {
                "extent": [
                    "2022-03-16T00:00:00.000Z",
                    "2022-03-19T00:00:00.000Z",
                ],
            },
            {
                "dimensions": [
                    {"labels": ["2022-03-16T00:00:00.000Z"], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B01", "B02", "B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": {
                    "data": [21, 22, 23],
                },
            },
        ),
        # temporal extent includes minimum range to include all data (note it's right-closed)
        (
            {
                "extent": [
                    "2022-03-16T00:00:00.000Z",
                    "2022-03-21T00:00:00.001Z",
                ],
            },
            {
                "dimensions": [
                    {
                        "labels": ["2022-03-21T00:00:00.000Z", "2022-03-19T00:00:00.000Z", "2022-03-16T00:00:00.000Z"],
                        "name": "temporal_name",
                        "type": "temporal",
                    },
                    {"labels": ["B01", "B02", "B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": {
                    "data": [1, 2, 3, 11, 12, 13, 21, 22, 23],
                },
            },
        ),
        # open end interval
        (
            {
                "extent": [
                    "2022-03-17T00:00:00.000Z",
                    None,
                ],
            },
            {
                "dimensions": [
                    {
                        "labels": ["2022-03-21T00:00:00.000Z", "2022-03-19T00:00:00.000Z"],
                        "name": "temporal_name",
                        "type": "temporal",
                    },
                    {"labels": ["B01", "B02", "B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": {
                    "data": [1, 2, 3, 11, 12, 13],
                },
            },
        ),
        # open start interval
        (
            {
                "extent": [
                    None,
                    "2022-03-20T00:00:00.000Z",
                ],
            },
            {
                "dimensions": [
                    {
                        "labels": ["2022-03-19T00:00:00.000Z", "2022-03-16T00:00:00.000Z"],
                        "name": "temporal_name",
                        "type": "temporal",
                    },
                    {"labels": ["B01", "B02", "B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": {
                    "data": [11, 12, 13, 21, 22, 23],
                },
            },
        ),
        # dimension parameter
        (
            {
                "extent": [
                    "2022-03-10T00:00:00.000Z",
                    "2022-03-25T00:00:00.000Z",
                ],
                "dimension": "temporal_name",
            },
            {
                "dimensions": [
                    {
                        "labels": ["2022-03-21T00:00:00.000Z", "2022-03-19T00:00:00.000Z", "2022-03-16T00:00:00.000Z"],
                        "name": "temporal_name",
                        "type": "temporal",
                    },
                    {"labels": ["B01", "B02", "B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": {
                    "data": [1, 2, 3, 11, 12, 13, 21, 22, 23],
                },
            },
        ),
        # temporal extent in date format
        (
            {
                "extent": [
                    "2022-03-19",
                    "2022-03-25",
                ],
            },
            {
                "dimensions": [
                    {
                        "labels": ["2022-03-21T00:00:00.000Z", "2022-03-19T00:00:00.000Z"],
                        "name": "temporal_name",
                        "type": "temporal",
                    },
                    {"labels": ["B01", "B02", "B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": {
                    "data": [1, 2, 3, 11, 12, 13],
                },
            },
        ),
    ],
)
def test_filter_temporal(filter_temporal_process_code, data, scenes, example_input, expected_output):
    additional_js_code_to_run = (
        load_datacube_code() + f"const cube = new DataCube({data}, 'bands_name', 'temporal_name', true, [], {scenes});"
    )
    process_arguments = f"Object.assign({json.dumps(example_input)}, {{'data': cube, 'scenes': {scenes}}})"
    output = run_process(
        filter_temporal_process_code + additional_js_code_to_run,
        "filter_temporal",
        process_arguments,
    )
    output = json.loads(output)
    assert output["dimensions"] == expected_output["dimensions"]
    assert output["data"]["data"] == expected_output["data"]["data"]


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        (
            {
                "data": [{"B01": 1}],
                "scenes": [
                    {"date": "2022-03-16T00:00:00.000Z"},
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
                    {"date": "2022-03-16T00:00:00.000Z"},
                ],
                "extent": [
                    "2022-03-10T00:00:00.000Z",
                    "2022-03-25T00:00:00.000Z",
                ],
                "dimension": "temporal_name",
            },
            False,
            None,
        ),
        (
            {
                "data": [{"B01": 1}],
                "scenes": [
                    {"date": "2022-03-16T00:00:00.000Z"},
                ],
            },
            True,
            "MISSING_PARAMETER",
        ),
        (
            {
                "data": [{"B01": 1}],
                "scenes": [
                    {"date": "INVALID_DATE_FORMAT"},
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
                    {"date": "2022-03-16T00:00:00.000Z"},
                ],
                "extent": [],
            },
            True,
            "Invalid temporal extent. Temporal extent must be an array of exactly two elements.",
        ),
        (
            {
                "data": [{"B01": 1}],
                "scenes": [
                    {"date": "2022-03-16T00:00:00.000Z"},
                ],
                "extent": [
                    "2022-03-10T00:00:00.000Z",
                ],
            },
            True,
            "Invalid temporal extent. Temporal extent must be an array of exactly two elements.",
        ),
        (
            {
                "data": [{"B01": 1}],
                "scenes": [
                    {"date": "2022-03-16T00:00:00.000Z"},
                ],
                "extent": [
                    "2022-03-10T00:00:00.000Z",
                    "2022-03-10T00:00:00.000Z",
                    "2022-03-25T00:00:00.000Z",
                ],
            },
            True,
            "Invalid temporal extent. Temporal extent must be an array of exactly two elements.",
        ),
        (
            {
                "data": [{"B01": 1}],
                "scenes": [
                    {"date": "2022-03-16T00:00:00.000Z"},
                ],
                "extent": [
                    None,
                    None,
                ],
            },
            True,
            "Invalid temporal extent. Only one of the boundaries can be null.",
        ),
        (
            {
                "data": [{"B01": 1}],
                "scenes": [
                    {"date": "2022-03-16T00:00:00.000Z"},
                ],
                "extent": [
                    "INVALID_DATE",
                    None,
                ],
            },
            True,
            "Invalid temporal extent. Boundary must be ISO date string or null.",
        ),
        (
            {
                "data": [{"B01": 1}],
                "scenes": [
                    {"date": "2022-03-16T00:00:00.000Z"},
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
                    {"date": "2022-03-16T00:00:00.000Z"},
                ],
                "extent": [
                    "2022-03-10T00:00:00.000Z",
                    "2022-03-25T00:00:00.000Z",
                ],
                "dimension": 15,
            },
            True,
            "WRONG_TYPE",
        ),
        (
            {
                "data": [{"B01": 1}],
                "scenes": [
                    {"date": "2022-03-16T00:00:00.000Z"},
                ],
                "extent": [
                    "2022-03-10T00:00:00.000Z",
                    "2022-03-25T00:00:00.000Z",
                ],
                "dimension": "NON_EXISTENT_DIMENSION",
            },
            True,
            "Dimension not available.",
        ),
        (
            {
                "data": [{"B01": 1}],
                "scenes": [
                    {"date": "2022-03-16T00:00:00.000Z"},
                ],
                "extent": [
                    "2022-03-10T00:00:00.000Z",
                    "2022-03-25T00:00:00.000Z",
                ],
                "dimension": "bands_name",
            },
            True,
            "Dimension is not of type temporal.",
        ),
    ],
)
def test_filter_temporal_exceptions(filter_temporal_process_code, example_input, raises_exception, error_message):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube = new DataCube({example_input['data']}, 'bands_name', 'temporal_name', true, [], {example_input['scenes']});"
    )
    process_arguments = f"Object.assign({json.dumps(example_input)}, {{'data': cube}})"
    run_input_validation(
        filter_temporal_process_code + additional_js_code_to_run,
        "filter_temporal",
        process_arguments,
        raises_exception,
        error_message=error_message,
    )
