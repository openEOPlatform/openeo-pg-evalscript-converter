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
            {"data": [{"B04": 21, "B08": 13}]},
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {"labels": [], "name": "t", "type": "temporal"},
                ],
                "data": {"data": [-0.23529411764705882], "offset": 0, "shape": [1], "stride": [1]},
            },
        ),
        (
            {"data": [{"B04": 2, "B08": 2}, {"B04": 1, "B08": 4}]},
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {"labels": [], "name": "t", "type": "temporal"},
                ],
                "data": {"data": [0, 0.6], "offset": 0, "shape": [2], "stride": [1]},
            },
        ),
        (
            {"data": [{"B01": 21, "B02": 13}], "nir": "blue", "red": "coastal"},
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {"labels": [], "name": "t", "type": "temporal"},
                ],
                "data": {"data": [-0.23529411764705882], "offset": 0, "shape": [1], "stride": [1]},
            },
        ),
        (
            {"data": [{"B04": 21, "B08": 13}], "target_band": "ndvi_new_name"},
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {"labels": [], "name": "t", "type": "temporal"},
                    {"labels": ["B04", "B08", "ndvi_new_name"], "name": "bands", "type": "bands"},
                ],
                "data": {"data": [21, 13, -0.23529411764705882], "offset": 0, "shape": [1, 3], "stride": [3, 1]},
            },
        ),
        (
            {"data": [{"B01": 21, "B02": 13}], "nir": "blue", "red": "coastal", "target_band": "ndvi_new_name"},
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {"labels": [], "name": "t", "type": "temporal"},
                    {"labels": ["B01", "B02", "ndvi_new_name"], "name": "bands", "type": "bands"},
                ],
                "data": {"data": [21, 13, -0.23529411764705882], "offset": 0, "shape": [1, 3], "stride": [3, 1]},
            },
        ),
        (
            {"data": [{"B04": 2, "B08": 2}, {"B04": 1, "B08": 4}], "target_band": "ndvi"},
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {"labels": [], "name": "t", "type": "temporal"},
                    {"labels": ["B04", "B08", "ndvi"], "name": "bands", "type": "bands"},
                ],
                "data": {"data": [2, 2, 0, 1, 4, 0.6], "offset": 0, "shape": [2, 3], "stride": [3, 1]},
            },
        ),
        (
            {"data": [{"abc": 1, "B04": 2, "B08": 2}, {"abc": 12, "B04": 1, "B08": 4}], "target_band": "ndvi"},
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands",
                "temporal_dimension_name": "t",
                "dimensions": [
                    {"labels": [], "name": "t", "type": "temporal"},
                    {"labels": ["abc", "B04", "B08", "ndvi"], "name": "bands", "type": "bands"},
                ],
                "data": {"data": [1, 2, 2, 0, 12, 1, 4, 0.6], "offset": 0, "shape": [2, 4], "stride": [4, 1]},
            },
        ),
    ],
)
def test_ndvi(ndvi_code, example_input, expected_output):
    bands_metadata = [
        {
            "name": "B01",
            "common_name": "coastal",
            "center_wavelength": 0.4427,
            "full_width_half_max": 0.021,
            "openeo:gsd": {"value": [60, 60], "unit": "m"},
        },
        {
            "name": "B02",
            "common_name": "blue",
            "center_wavelength": 0.4924,
            "full_width_half_max": 0.066,
            "openeo:gsd": {"value": [10, 10], "unit": "m"},
        },
        {
            "name": "B03",
            "common_name": "green",
            "center_wavelength": 0.5598,
            "full_width_half_max": 0.036,
            "openeo:gsd": {"value": [10, 10], "unit": "m"},
        },
        {
            "name": "B04",
            "common_name": "red",
            "center_wavelength": 0.6646,
            "full_width_half_max": 0.031,
            "openeo:gsd": {"value": [10, 10], "unit": "m"},
        },
        {
            "name": "B05",
            "center_wavelength": 0.7041,
            "full_width_half_max": 0.015,
            "openeo:gsd": {"value": [20, 20], "unit": "m"},
        },
        {
            "name": "B06",
            "center_wavelength": 0.7405,
            "full_width_half_max": 0.015,
            "openeo:gsd": {"value": [20, 20], "unit": "m"},
        },
        {
            "name": "B07",
            "center_wavelength": 0.7828,
            "full_width_half_max": 0.02,
            "openeo:gsd": {"value": [20, 20], "unit": "m"},
        },
        {
            "name": "B08",
            "common_name": "nir",
            "center_wavelength": 0.8328,
            "full_width_half_max": 0.106,
            "openeo:gsd": {"value": [10, 10], "unit": "m"},
        },
        {
            "name": "B8A",
            "common_name": "nir08",
            "center_wavelength": 0.8647,
            "full_width_half_max": 0.021,
            "openeo:gsd": {"value": [20, 20], "unit": "m"},
        },
        {
            "name": "B09",
            "common_name": "nir09",
            "center_wavelength": 0.9451,
            "full_width_half_max": 0.02,
            "openeo:gsd": {"value": [60, 60], "unit": "m"},
        },
        {
            "name": "B11",
            "common_name": "swir16",
            "center_wavelength": 1.6137,
            "full_width_half_max": 0.091,
            "openeo:gsd": {"value": [20, 20], "unit": "m"},
        },
        {
            "name": "B12",
            "common_name": "swir22",
            "center_wavelength": 2.2024,
            "full_width_half_max": 0.175,
            "openeo:gsd": {"value": [20, 20], "unit": "m"},
        },
        {
            "description": "Aerosol Optical Thickness map, based on Sen2Cor processor",
            "name": "AOT",
            "openeo:gsd": {"value": [10, 10], "unit": "m"},
        },
        {
            "description": "Scene classification data, based on Sen2Cor processor, codelist",
            "name": "SCL",
            "openeo:gsd": {"value": [20, 20], "unit": "m"},
        },
        {
            "description": "Snow probability, based on Sen2Cor processor",
            "name": "SNW",
            "openeo:gsd": {"value": [20, 20], "unit": "m"},
        },
        {
            "description": "Cloud probability, based on Sen2Cor processor",
            "name": "CLD",
            "openeo:gsd": {"value": [20, 20], "unit": "m"},
        },
        {
            "description": "Cloud probability, based on s2cloudless",
            "name": "CLP",
            "openeo:gsd": {"value": [160, 160], "unit": "m"},
        },
        {"description": "Cloud masks", "name": "CLM", "openeo:gsd": {"value": [160, 160], "unit": "m"}},
        {
            "description": "Sun azimuth angle",
            "name": "sunAzimuthAngles",
            "openeo:gsd": {"value": [5000, 5000], "unit": "m"},
        },
        {
            "description": "Sun zenith angle",
            "name": "sunZenithAngles",
            "openeo:gsd": {"value": [5000, 5000], "unit": "m"},
        },
        {
            "description": "Viewing azimuth angle",
            "name": "viewAzimuthMean",
            "openeo:gsd": {"value": [5000, 5000], "unit": "m"},
        },
        {
            "description": "Viewing zenith angle",
            "name": "viewZenithMean",
            "openeo:gsd": {"value": [5000, 5000], "unit": "m"},
        },
        {"description": "The mask of data/no data pixels.", "name": "dataMask"},
    ]
    js_code = (
        load_datacube_code()
        + f"const cube = new DataCube({example_input['data']}, 'bands', 't', true, {bands_metadata});"
    )
    process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube}}"
    output = run_process(ndvi_code + js_code, "ndvi", process_arguments)
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,additional_js_code_specific_to_case,raises_exception,error_name",
    [
        ({"data": [{"B04": 2, "B08": 2}], "target_band": "ndvi_name"}, None, False, None),
        ({"data": [{"B04": 2, "B08": 2}]}, "cube = undefined;", True, "MISSING_PARAMETER"),
        ({"data": [{"B04": 2, "B08": 2}], "nir": [123]}, None, True, "WRONG_TYPE"),
        ({"data": [{"B04": 2, "B08": 2}], "nir": {"name": "John", "surname": "Doe"}}, None, True, "WRONG_TYPE"),
        ({"data": [{"B04": 2, "B08": 2}], "red": False}, None, True, "WRONG_TYPE"),
        ({"data": [{"B04": 2, "B08": 2}], "target_band": 123}, None, True, "WRONG_TYPE"),
        (
            {"data": [{"B04": 2, "B08": 2}]},
            "cube.getDimensionByName(cube.bands_dimension_name).type = 'fake_wrong_type';",
            True,
            "DimensionAmbiguous",
        ),
        (
            {"data": [{"B04": 2, "B08": 2}], "nir": "false_nir_name"},
            None,
            True,
            "NirBandAmbiguous",
        ),
        (
            {"data": [{"B04": 2, "B08": 2}], "red": "false_red_name"},
            None,
            True,
            "RedBandAmbiguous",
        ),
        (
            {"data": [{"B04": 2, "B08": 2, "ndvi": 1234}], "target_band": "ndvi"},
            None,
            True,
            "BandExists",
        ),
    ],
)
def test_input_validation(ndvi_code, example_input, additional_js_code_specific_to_case, raises_exception, error_name):
    bands_metadata = [
        {
            "name": "B01",
            "common_name": "coastal",
            "center_wavelength": 0.4427,
            "full_width_half_max": 0.021,
            "openeo:gsd": {"value": [60, 60], "unit": "m"},
        },
        {
            "name": "B02",
            "common_name": "blue",
            "center_wavelength": 0.4924,
            "full_width_half_max": 0.066,
            "openeo:gsd": {"value": [10, 10], "unit": "m"},
        },
        {
            "name": "B03",
            "common_name": "green",
            "center_wavelength": 0.5598,
            "full_width_half_max": 0.036,
            "openeo:gsd": {"value": [10, 10], "unit": "m"},
        },
        {
            "name": "B04",
            "common_name": "red",
            "center_wavelength": 0.6646,
            "full_width_half_max": 0.031,
            "openeo:gsd": {"value": [10, 10], "unit": "m"},
        },
        {
            "name": "B05",
            "center_wavelength": 0.7041,
            "full_width_half_max": 0.015,
            "openeo:gsd": {"value": [20, 20], "unit": "m"},
        },
        {
            "name": "B06",
            "center_wavelength": 0.7405,
            "full_width_half_max": 0.015,
            "openeo:gsd": {"value": [20, 20], "unit": "m"},
        },
        {
            "name": "B07",
            "center_wavelength": 0.7828,
            "full_width_half_max": 0.02,
            "openeo:gsd": {"value": [20, 20], "unit": "m"},
        },
        {
            "name": "B08",
            "common_name": "nir",
            "center_wavelength": 0.8328,
            "full_width_half_max": 0.106,
            "openeo:gsd": {"value": [10, 10], "unit": "m"},
        },
        {
            "name": "B8A",
            "common_name": "nir08",
            "center_wavelength": 0.8647,
            "full_width_half_max": 0.021,
            "openeo:gsd": {"value": [20, 20], "unit": "m"},
        },
        {
            "name": "B09",
            "common_name": "nir09",
            "center_wavelength": 0.9451,
            "full_width_half_max": 0.02,
            "openeo:gsd": {"value": [60, 60], "unit": "m"},
        },
        {
            "name": "B11",
            "common_name": "swir16",
            "center_wavelength": 1.6137,
            "full_width_half_max": 0.091,
            "openeo:gsd": {"value": [20, 20], "unit": "m"},
        },
        {
            "name": "B12",
            "common_name": "swir22",
            "center_wavelength": 2.2024,
            "full_width_half_max": 0.175,
            "openeo:gsd": {"value": [20, 20], "unit": "m"},
        },
        {
            "description": "Aerosol Optical Thickness map, based on Sen2Cor processor",
            "name": "AOT",
            "openeo:gsd": {"value": [10, 10], "unit": "m"},
        },
        {
            "description": "Scene classification data, based on Sen2Cor processor, codelist",
            "name": "SCL",
            "openeo:gsd": {"value": [20, 20], "unit": "m"},
        },
        {
            "description": "Snow probability, based on Sen2Cor processor",
            "name": "SNW",
            "openeo:gsd": {"value": [20, 20], "unit": "m"},
        },
        {
            "description": "Cloud probability, based on Sen2Cor processor",
            "name": "CLD",
            "openeo:gsd": {"value": [20, 20], "unit": "m"},
        },
        {
            "description": "Cloud probability, based on s2cloudless",
            "name": "CLP",
            "openeo:gsd": {"value": [160, 160], "unit": "m"},
        },
        {"description": "Cloud masks", "name": "CLM", "openeo:gsd": {"value": [160, 160], "unit": "m"}},
        {
            "description": "Sun azimuth angle",
            "name": "sunAzimuthAngles",
            "openeo:gsd": {"value": [5000, 5000], "unit": "m"},
        },
        {
            "description": "Sun zenith angle",
            "name": "sunZenithAngles",
            "openeo:gsd": {"value": [5000, 5000], "unit": "m"},
        },
        {
            "description": "Viewing azimuth angle",
            "name": "viewAzimuthMean",
            "openeo:gsd": {"value": [5000, 5000], "unit": "m"},
        },
        {
            "description": "Viewing zenith angle",
            "name": "viewZenithMean",
            "openeo:gsd": {"value": [5000, 5000], "unit": "m"},
        },
        {"description": "The mask of data/no data pixels.", "name": "dataMask"},
    ]
    js_code = (
        load_datacube_code()
        + f"let cube = new DataCube({example_input['data']}, 'bands', 't', true, {bands_metadata});"
        + (additional_js_code_specific_to_case or "")
    )
    process_arguments = f"{{...{json.dumps(example_input)}, 'data': cube}}"
    run_input_validation(ndvi_code + js_code, "ndvi", process_arguments, raises_exception, error_name)
