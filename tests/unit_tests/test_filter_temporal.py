import json

import pytest

from tests.utils import load_process_code, load_datacube_code, run_process


@pytest.fixture
def filter_temporal_process_code():
    return load_process_code("filter_temporal")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        (
            {
                "data": [
                    {"date":"2022-03-21T00:00:00.000Z"},
                    {"date":"2022-03-19T00:00:00.000Z"},
                    {"date":"2022-03-16T00:00:00.000Z"}
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
                    {'labels': [], 'name': 'temporal_name', 'type': 'temporal'},
                    {'labels': ['date'], 'name': 'bands_name', 'type': 'bands'}
                ],
                'data': {
                    'data': [
                        '2022-03-21T00:00:00.000Z',
                        '2022-03-19T00:00:00.000Z',
                        '2022-03-16T00:00:00.000Z'
                    ],
                    'offset': 0,
                    'shape': [3, 1],
                    'stride': [1, 1]
                }
            },
        ),
    ],
)
def test_filter_temporal(filter_temporal_process_code, example_input, expected_output):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube = new DataCube({example_input['data']}, 'bands_name', 'temporal_name', true);"
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
    ],
)
def test_filter_temporal_exceptions(filter_temporal_process_code, example_input, raises_exception, error_message):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube = new DataCube({example_input['data']}, 'bands_name', 'temporal_name', true);"
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
        