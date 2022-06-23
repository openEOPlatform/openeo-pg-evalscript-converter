import pkg_resources


def list_supported_processes():
    process_definitions_directory = "javascript_processes"
    implicitly_supported_processes = ["load_collection", "save_result", "reduce_dimension", "apply"]
    process_definition_files = pkg_resources.resource_listdir("pg_to_evalscript", f"{process_definitions_directory}")
    supported_processes_with_files = [
        process_definition_file.replace(".js", "") for process_definition_file in process_definition_files
    ]
    return [*implicitly_supported_processes, *supported_processes_with_files]


def convert_defaultdict_to_dict(default_dict):
    new_dict = dict()
    for key, value in default_dict.items():
        if value != default_dict.default_factory():
            new_dict[key] = value
    return new_dict
