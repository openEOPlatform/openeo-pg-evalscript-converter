import json

import pytest
import subprocess

from tests.utils import load_process_code, load_datacube_code, run_process


@pytest.fixture
def mask_process_code():
    return load_process_code("mask")


data_3bands_3dates = [
    {"B01": 1, "B02": 2, "B03": 3},  # date 1
    {"B01": 11, "B02": 12, "B03": 13},  # date 2
    {"B01": 21, "B02": 22, "B03": 23},  # date 3
]

mask_3bands_3dates_num = [
    {"B01": 0, "B02": 2, "B03": 0},  # date 1
    {"B01": 11, "B02": 0, "B03": 13},  # date 2
    {"B01": 0, "B02": 22, "B03": 0},  # date 3
]

mask_3bands_3dates_bool = [
    {"B01": False, "B02": True, "B03": False},  # date 1
    {"B01": True, "B02": False, "B03": True},  # date 2
    {"B01": False, "B02": True, "B03": False},  # date 3
]

scenes_3dates = [
    {"date": "2022-03-21T00:00:00.000Z"},  # date 1
    {"date": "2022-03-19T00:00:00.000Z"},  # date 2
    {"date": "2022-03-16T00:00:00.000Z"},  # date 3
]

replacement_val_num = 42
replacement_val_bool = True
replacement_val_str = "qwe"

result_3bands_3dates = [1, None, 3, None, 12, None, 21, None, 23]
result_mask_no_temporal = [1, None, 3, 11, None, 13, 21, None, 23]
result_mask_no_bands = [None, 2, 3, None, 12, 13, None, 22, 23]


def resultWithReplacement(dataArray, val=None):
    return {
        "TEMPORAL": "temporal",
        "BANDS": "bands",
        "OTHER": "other",
        "bands_dimension_name": "bands_name",
        "temporal_dimension_name": "temporal_name",
        "dimensions": [
            {
                "name": "temporal_name",
                "labels": [
                    "2022-03-21T00:00:00.000Z",
                    "2022-03-19T00:00:00.000Z",
                    "2022-03-16T00:00:00.000Z",
                ],
                "type": "temporal",
            },
            {
                "name": "bands_name",
                "labels": ["B01", "B02", "B03"],
                "type": "bands",
            },
        ],
        "data": {
            "data": [val if el == None else el for el in dataArray],
            "shape": [3, 3],
            "stride": [3, 1],
            "offset": 0,
        },
    }


result_added_dim = {
    "TEMPORAL": "temporal",
    "BANDS": "bands",
    "OTHER": "other",
    "bands_dimension_name": "bands_name",
    "temporal_dimension_name": "temporal_name",
    "dimensions": [
        {"name": "test_name", "labels": ["test_label"], "type": "other"},
        {
            "name": "temporal_name",
            "labels": [
                "2022-03-21T00:00:00.000Z",
                "2022-03-19T00:00:00.000Z",
                "2022-03-16T00:00:00.000Z",
            ],
            "type": "temporal",
        },
        {
            "name": "bands_name",
            "labels": ["B01", "B02", "B03"],
            "type": "bands",
        },
    ],
    "data": {
        "data": result_3bands_3dates,
        "shape": [1, 3, 3],
        "stride": [9, 3, 1],
        "offset": 0,
    },
}


@pytest.mark.parametrize(
    "example_input, additional_js_code_specific_to_case, expected_output",
    [
        (  # test different mask values: mask with number values
            {
                "data": data_3bands_3dates,
                "mask": mask_3bands_3dates_num,
                "scenes_data": scenes_3dates,
                "scenes_mask": scenes_3dates,
            },
            None,
            resultWithReplacement(result_3bands_3dates),
        ),
        (  # test different mask values: mask with boolean values
            {
                "data": data_3bands_3dates,
                "mask": mask_3bands_3dates_bool,
                "scenes_data": scenes_3dates,
                "scenes_mask": scenes_3dates,
            },
            None,
            resultWithReplacement(result_3bands_3dates),
        ),
        (  # test different replacement values: replacement = number
            {
                "data": data_3bands_3dates,
                "mask": mask_3bands_3dates_num,
                "scenes_data": scenes_3dates,
                "scenes_mask": scenes_3dates,
                "replacement": replacement_val_num,
            },
            None,
            resultWithReplacement(result_3bands_3dates, replacement_val_num),
        ),
        (  # test different replacement values: replacement = boolean
            {
                "data": data_3bands_3dates,
                "mask": mask_3bands_3dates_num,
                "scenes_data": scenes_3dates,
                "scenes_mask": scenes_3dates,
                "replacement": replacement_val_bool,
            },
            None,
            resultWithReplacement(result_3bands_3dates, replacement_val_bool),
        ),
        (  # test different replacement values: replacement = string
            {
                "data": data_3bands_3dates,
                "mask": mask_3bands_3dates_num,
                "scenes_data": scenes_3dates,
                "scenes_mask": scenes_3dates,
                "replacement": replacement_val_str,
            },
            None,
            resultWithReplacement(result_3bands_3dates, replacement_val_str),
        ),
        (  # test mask parameter missing dimensions: mask parameter with no temporal dimension
            {
                "data": data_3bands_3dates,
                "mask": [mask_3bands_3dates_num[0]],
                "scenes_data": scenes_3dates,
                "scenes_mask": None,
            },
            "maskCube.removeDimension('temporal_name');",
            resultWithReplacement(result_mask_no_temporal),
        ),
        # (  # test mask parameter missing dimensions: mask parameter with no bands dimension
        #     # doesn't work properly: same result as for "mask parameter with no temporal dimension"
        #     {
        #         "data": data_3bands_3dates,
        #         "mask": [{"B01": el["B01"]} for el in mask_3bands_3dates_num],
        #         "scenes_data": scenes_3dates,
        #         "scenes_mask": scenes_3dates,
        #     },
        #     "maskCube.removeDimension('bands_name');",
        #     resultWithReplacement(result_mask_no_bands),
        # ),
        (  # test mask parameter missing dimensions: data parameter with additional dimension
            {
                "data": data_3bands_3dates,
                "mask": mask_3bands_3dates_num,
                "scenes_data": scenes_3dates,
                "scenes_mask": scenes_3dates,
            },
            "dataCube.addDimension('test_name', 'test_label', 'other');",
            result_added_dim,
        ),
    ],
)
def test_mask(
    mask_process_code,
    example_input,
    additional_js_code_specific_to_case,
    expected_output,
):

    data_parameter = json.dumps(example_input["data"])
    mask_parameter = json.dumps(example_input["mask"])
    scenes_data = json.dumps(example_input["scenes_data"])
    scenes_mask = json.dumps(example_input["scenes_mask"])
    replacement_parameter = (
        json.dumps(example_input["replacement"])
        if "replacement" in example_input
        else None
    )

    vars_definitions = (
        f"const dataCube = new DataCube({data_parameter}, 'bands_name', 'temporal_name', true, [], {scenes_data});"
        + f"let maskCube = new DataCube({mask_parameter}, 'bands_name', 'temporal_name', true, [], {scenes_mask});"
    )

    if replacement_parameter:
        vars_definitions = (
            vars_definitions + f"const replacement = {replacement_parameter};"
        )

    additional_js_code_to_run = (
        load_datacube_code()
        + vars_definitions
        + (additional_js_code_specific_to_case or "")
    )

    arguments = f"'data': dataCube, 'mask': maskCube, 'scenes': {scenes_data}"

    if "replacement" in example_input:
        arguments = arguments + f", 'replacement': {replacement_parameter}"

    process_arguments = f"{{" + arguments + f"}}"

    print("input")
    print(example_input)
    print("\n")

    print("vars def")
    print(vars_definitions)
    print("\n")

    print("custom js")
    print(additional_js_code_specific_to_case)
    print("\n")

    print("arguments")
    print(process_arguments)
    print("\n")

    print("expected")
    print(expected_output)
    print("\n")

    try:
        output = run_process(
            mask_process_code + additional_js_code_to_run,
            "mask",
            process_arguments,
        )
        output = json.loads(output)

        print("actual")
        print(output)
        print("\n")

        assert output == expected_output

    except subprocess.CalledProcessError as exc:
        print("error:")
        print(exc.stderr)
        print("\n")

        assert exc.stderr == "OK"
