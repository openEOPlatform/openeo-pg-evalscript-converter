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
