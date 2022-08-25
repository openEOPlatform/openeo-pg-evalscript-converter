user_defined_processes = {
    # https://open-eo.github.io/openeo-python-client/udp.html
    "fahrenheit_to_celsius": {
        "subtract1": {"process_id": "subtract", "arguments": {"x": {"from_parameter": "f"}, "y": 32}},
        "divide1": {
            "process_id": "divide",
            "arguments": {"x": {"from_node": "subtract1"}, "y": 1.8},
            "result": True,
        },
    },
    # https://github.com/Open-EO/openeo-community-examples/blob/9ad1b59740a54d06d46b3d6b07c7b93946853d70/processes/array_find_nodata.json
    "array_find_nodata": {
        "apply": {
            "process_id": "array_apply",
            "arguments": {
                "data": {"from_parameter": "data"},
                "process": {
                    "process_graph": {
                        "is_null": {
                            "process_id": "is_nodata",
                            "arguments": {"x": {"from_parameter": "x"}},
                            "result": True,
                        }
                    }
                },
            },
        },
        "find": {
            "process_id": "array_find",
            "arguments": {"data": {"from_node": "apply"}, "value": True},
            "result": True,
        },
    },
    # User-defined processes can be constructed from other user-defined processes
    "find_nodata_convert_to_celsius": {
        "findnodata": {
            "process_id": "array_find_nodata",
            "arguments": {"data": {"from_parameter": "x"}},
            "result": True,
        },
        "convert": {
            "process_id": "fahrenheit_to_celsius",
            "arguments": {"f": {"from_node": "findnodata"}},
            "result": True,
        },
    },
}


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