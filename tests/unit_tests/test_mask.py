import json

import pytest

from tests.utils import load_process_code, load_datacube_code, run_process


@pytest.fixture
def mask_process_code():
    return load_process_code("mask")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        (
            {
                "data": {"B01": [1, 2, 3], "B02": [4, 5, 6]},
                "mask": {"B01": [11, 12, 13], "B02": [14, 15, 16]},
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B01", "B02"], "name": "bands_name", "type": "bands"},
                ],
                "data": [[11, 12, 13], [14, 15, 16]],
            },
        ),
    ],
)
def test_mask(mask_process_code, example_input, expected_output):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const data = new DataCube({example_input['data']}, 'bands_name', 'temporal_name', true);"
        + f"const mask1 = new DataCube({example_input['mask']}, 'bands_name', 'temporal_name', true);"
    )
    process_arguments = (
        f"{{...{json.dumps(example_input)}, 'data': data, 'mask': mask1}}"
    )

    # print("---------- js code -------------")
    # print(additional_js_code_to_run)
    # print(mask_process_code)

    # print("------------ arg ------------")
    # print(process_arguments)

    output = run_process(
        mask_process_code + additional_js_code_to_run,
        "mask",
        process_arguments,
    )
    print("output")

    output = json.loads(output)

    print(output)
    assert output == expected_output
