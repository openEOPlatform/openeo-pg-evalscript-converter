import json

import pytest
import subprocess

from tests.utils import load_process_code, load_datacube_code, run_process


@pytest.fixture
def resample_cube_temporal_process_code():
    return load_process_code("resample_cube_temporal")


data_3dates = [
    {"B01": 1, "B02": 2, "B03": 3},  # date 1
    {"B01": 11, "B02": 12, "B03": 13},  # date 2
    {"B01": 21, "B02": 22, "B03": 23},  # date 3
]

target_3dates = [
    {"B01": 1, "B02": 2, "B03": 3},  # date 1
    {"B01": 11, "B02": 12, "B03": 13},  # date 2
    {"B01": 21, "B02": 22, "B03": 23},  # date 3
]

target_2dates = [
    {"B01": 1, "B02": 2, "B03": 3},  # date 1
    {"B01": 11, "B02": 12, "B03": 13},  # date 2
]

target_4dates = [
    {"B01": 1, "B02": 2, "B03": 3},  # date 1
    {"B01": 11, "B02": 12, "B03": 13},  # date 2
    {"B01": 21, "B02": 22, "B03": 23},  # date 3
    {"B01": 31, "B02": 32, "B03": 33},  # date 4
]

data_scenes_3dates = [
    {"date": "2022-03-21T00:00:00.000Z"},  # date 1
    {"date": "2022-03-19T00:00:00.000Z"},  # date 2
    {"date": "2022-03-16T00:00:00.000Z"},  # date 3
]

scenes_2dates = [
    {"date": "2022-03-20T00:00:00.000Z"},  # date 1
    {"date": "2022-03-18T00:00:00.000Z"},  # date 2
]

scenes_4dates = [
    {"date": "2022-03-21T00:00:00.000Z"},  # date 1
    {"date": "2022-03-20T00:00:00.000Z"},  # date 2
    {"date": "2022-03-18T00:00:00.000Z"},  # date 3
    {"date": "2022-03-17T00:00:00.000Z"},  # date 4
]

result_3dates = {
    "data": [1, 2, 3, 11, 12, 13, 21, 22, 23],
    "shape": [3, 3],
    "stride": [3, 1],
    "offset": 0,
}

result_2dates = {
    "data": [1, 2, 3, 11, 12, 13],
    "shape": [2, 3],
    "stride": [3, 1],
    "offset": 0,
}

result_4dates = {
    "data": [1, 2, 3, 11, 12, 13, 21, 22, 23, 31, 32, 33],
    "shape": [4, 3],
    "stride": [3, 1],
    "offset": 0,
}


def resultWithTemporal(dataObject, temporalLabels):
    return {
        "TEMPORAL": "temporal",
        "BANDS": "bands",
        "OTHER": "other",
        "bands_dimension_name": "bands_name",
        "temporal_dimension_name": "temporal_name",
        "dimensions": [
            {
                "name": "temporal_name",
                "labels": [el["date"] for el in temporalLabels],
                "type": "temporal",
            },
            {
                "name": "bands_name",
                "labels": ["B01", "B02", "B03"],
                "type": "bands",
            },
        ],
        "data": dataObject,
    }


@pytest.mark.parametrize(
    "example_input, additional_js_code_specific_to_case, expected_output",
    [
        (
            {
                "data": data_3dates,
                "target": target_3dates,
                "scenes_data": data_scenes_3dates,
                "scenes_target": data_scenes_3dates
                # "dimension": None,
                # "valid_within": None,
            },
            None,
            resultWithTemporal(result_3dates, data_scenes_3dates),
        )
    ],
)
def test_resample_cube_temporal(
    resample_cube_temporal_process_code,
    example_input,
    additional_js_code_specific_to_case,
    expected_output,
):

    data_parameter = json.dumps(example_input["data"])
    target_parameter = json.dumps(example_input["target"])
    scenes_data = json.dumps(example_input["scenes_data"])
    scenes_target = json.dumps(example_input["scenes_target"])

    dimension_parameter = (
        json.dumps(example_input["dimension"]) if "dimension" in example_input else None
    )

    valid_within_parameter = (
        json.dumps(example_input["valid_within"])
        if "valid_within" in example_input
        else None
    )

    vars_definitions = (
        f"const dataCube = new DataCube({data_parameter}, 'bands_name', 'temporal_name', true, [], {scenes_data});"
        + f"let targetCube = new DataCube({target_parameter}, 'bands_name', 'temporal_name', true, [], {scenes_target});"
    )

    if dimension_parameter:
        vars_definitions = (
            vars_definitions + f"const dimension = {dimension_parameter};"
        )

    if valid_within_parameter:
        vars_definitions = (
            vars_definitions + f"const valid_within = {valid_within_parameter};"
        )

    additional_js_code_to_run = (
        load_datacube_code()
        + vars_definitions
        + (additional_js_code_specific_to_case or "")
    )

    arguments = (
        f"'data': dataCube, 'target': targetCube"  # , 'scenes': {dimension_parameter}
    )

    if "dimension" in example_input:
        arguments = arguments + f", 'dimension': {dimension_parameter}"

    if "valid_within" in example_input:
        arguments = arguments + f", 'valid_within': {valid_within_parameter}"

    process_arguments = f"{{" + arguments + f"}}"

    print("EXPECTED OUTPUT:")
    print(json.dumps(expected_output))

    try:
        output = run_process(
            resample_cube_temporal_process_code + additional_js_code_to_run,
            "resample_cube_temporal",
            process_arguments,
        )
        output = json.loads(output)
        assert output == expected_output

    except subprocess.CalledProcessError as exc:
        print("ERROR")
        print(exc.stderr)
        assert "OK" in str(exc.stderr)
