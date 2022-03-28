import json

import pytest

from tests.utils import load_process_code, load_datacube_code, run_process, run_input_validation


@pytest.fixture
def ndvi_code():
    return load_process_code("ndvi")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        (
            {"data": [{"nir": 21, "red": 13}]},
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {"labels": [], "name": "t", "type": "temporal"},
                ],
                "data": {"data": [0.23529411764705882], "offset": 0, "shape": [1], "stride": [1]},
            },
        ),
        (
            {"data": [{"nir": 2, "red": 2}, {"nir": 1, "red": 4}]},
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {"labels": [], "name": "t", "type": "temporal"},
                ],
                "data": {"data": [0, -0.6], "offset": 0, "shape": [2], "stride": [1]},
            },
        ),
        (
            {"data": [{"a": 21, "b": 13}], "nir": "a", "red": "b"},
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {"labels": [], "name": "t", "type": "temporal"},
                ],
                "data": {"data": [0.23529411764705882], "offset": 0, "shape": [1], "stride": [1]},
            },
        ),
        (
            {"data": [{"nir": 21, "red": 13}], "target_band": "ndvi_new_name"},
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {"labels": [], "name": "t", "type": "temporal"},
                    {"labels": ["nir", "red", "ndvi_new_name"], "name": "bands", "type": "bands"},
                ],
                "data": {"data": [21, 13, 0.23529411764705882], "offset": 0, "shape": [1, 3], "stride": [3, 1]},
            },
        ),
        (
            {"data": [{"a": 21, "b": 13}], "nir": "a", "red": "b", "target_band": "ndvi_new_name"},
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {"labels": [], "name": "t", "type": "temporal"},
                    {"labels": ["a", "b", "ndvi_new_name"], "name": "bands", "type": "bands"},
                ],
                "data": {"data": [21, 13, 0.23529411764705882], "offset": 0, "shape": [1, 3], "stride": [3, 1]},
            },
        ),
        (
            {"data": [{"nir": 2, "red": 2}, {"nir": 1, "red": 4}], "target_band": "ndvi"},
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {"labels": [], "name": "t", "type": "temporal"},
                    {"labels": ["nir", "red", "ndvi"], "name": "bands", "type": "bands"},
                ],
                "data": {"data": [2, 2, 0, 1, 4, -0.6], "offset": 0, "shape": [2, 3], "stride": [3, 1]},
            },
        ),
        (
            {"data": [{"abc": 1, "nir": 2, "red": 2}, {"abc": 12, "nir": 1, "red": 4}], "target_band": "ndvi"},
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {"labels": [], "name": "t", "type": "temporal"},
                    {"labels": ["abc", "nir", "red", "ndvi"], "name": "bands", "type": "bands"},
                ],
                "data": {"data": [1, 2, 2, 0, 12, 1, 4, -0.6], "offset": 0, "shape": [2, 4], "stride": [4, 1]},
            },
        ),
    ],
)
def test_ndvi(ndvi_code, example_input, expected_output):
    js_code = load_datacube_code() + f"const cube = new DataCube({example_input['data']}, 'bands', 't', true);"
    process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube}}"
    output = run_process(ndvi_code + js_code, "ndvi", process_arguments)
    output = json.loads(output)
    assert output == expected_output


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
            "DimensionAmbiguous",
        ),
        (
            {"data": [{"nir_fake_label": 2, "red": 2}]},
            None,
            True,
            "NirBandAmbiguous",
        ),
        (
            {"data": [{"nir": 2, "red_fake_label": 2}]},
            None,
            True,
            "RedBandAmbiguous",
        ),
        (
            {"data": [{"nir": 2, "red": 2, "ndvi": 1234}], "target_band": "ndvi"},
            None,
            True,
            "BandExists",
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
