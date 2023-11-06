import pkg_resources

implicitly_supported_processes = ["load_collection", "save_result"]

def list_supported_processes():
    process_definitions_directory = "javascript_processes"
    process_definition_files = pkg_resources.resource_listdir("pg_to_evalscript", f"{process_definitions_directory}")
    supported_processes_with_files = [
        process_definition_file.replace(".js", "") for process_definition_file in process_definition_files
    ]
    unique_supported_processes = list(set([*implicitly_supported_processes, *supported_processes_with_files]))
    return unique_supported_processes
