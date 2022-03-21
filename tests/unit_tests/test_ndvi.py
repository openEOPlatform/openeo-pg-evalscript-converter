import json

import pytest

from tests.utils import load_process_code, load_datacube_code, run_process, run_input_validation


@pytest.fixture
def ndvi_code():
    return load_process_code("ndvi")


# @pytest.mark.parametrize(
#     "example_input,expected_output",
#     [
#         (
#             {"data": [{"nir": 2, "red": 2}], "target_band": "ndvi"},
#             {
#                 "BANDS": "bands",
#                 "OTHER": "other",
#                 "TEMPORAL": "temporal",
#                 "bands_dimension_name": "bands",
#                 "temporal_dimension_name": "temporal",
#                 "dimensions": [
#                     {"labels": [], "name": "t", "type": "temporal"},
#                     {"labels": ["nir", "red", "ndvi"], "name": "bands", "type": "bands"},
#                 ],
#                 "data": [[2, 2, 0]],
#             },
#         )
#     ],
# )
# def test_ndvi(ndvi_code, example_input, expected_output):
#     js_code = load_datacube_code() + f"const cube = new DataCube({example_input['data']}, 'bands', 't', true);"
#     process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube}}"
#     output = run_process(ndvi_code + js_code, "ndvi", process_arguments)
#     output = json.loads(output)
#     assert output == expected_output


@pytest.mark.parametrize(
    "example_input,additional_js_code_specific_to_case,raises_exception,error_name",
    [
        ({"data": [{"nir": 2, "red": 2}], "target_band": "ndvi_name"}, None, False, None),
        ({"data": [{"nir": 2, "red": 2}]}, "cube = undefined;", True, "MISSING_PARAMETER"),
        ({"data": [{"nir": 2, "red": 2}], "nir": [123]}, None, True, "WRONG_TYPE"),
        ({"data": [{"nir": 2, "red": 2}], "nir": {"name": "John", "surname": "Doe"}}, None, True, "WRONG_TYPE"),
        ({"data": [{"nir": 2, "red": 2}], "red": False}, None, True, "WRONG_TYPE"),
        ({"data": [{"nir": 2, "red": 2}], "target_band": 123}, None, True, "WRONG_TYPE"),
        (
            {"data": [{"nir": 2, "red": 2}]},
            "cube.getDimensionByName(cube.bands_dimension_name).type = 'fake_wrong_type';",
            True,
            "Dimension of type `bands` is not available or is ambiguous.",
        ),
        (
            {"data": [{"nir_fake_label": 2, "red": 2}]},
            None,
            True,
            "The NIR band can't be resolved, please specify the specific NIR band name.",
        ),
        (
            {"data": [{"nir": 2, "red_fake_label": 2}]},
            None,
            True,
            "The red band can't be resolved, please specify the specific red band name.",
        ),
        (
            {"data": [{"nir": 2, "red": 2, "ndvi": 1234}], "target_band": "ndvi"},
            None,
            True,
            "A band with the specified target name exists.",
        ),
    ],
)
def test_input_validation(ndvi_code, example_input, additional_js_code_specific_to_case, raises_exception, error_name):
    js_code = (
        load_datacube_code()
        + f"let cube = new DataCube({example_input['data']}, 'bands', 't', true);"
        + (additional_js_code_specific_to_case or "")
    )
    process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube}}"
    run_input_validation(ndvi_code + js_code, "ndvi", process_arguments, raises_exception, error_name)
