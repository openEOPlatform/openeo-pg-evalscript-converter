import os
import json
import glob
import subprocess


def get_process_graph_json(name):
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, f"process_graphs/{name}.json")
    with open(abs_file_path) as f:
        return json.load(f)


def get_execute_test_script(example_input):
    return f"""
process.stdout.write(JSON.stringify(evaluatePixel({json.dumps(example_input)})));
"""


def run_evalscript(evalscript, example_input):
    return run_javacript(evalscript + get_execute_test_script(example_input))


def run_process(process_code, process_name, example_input):
    return run_javacript(
        process_code + f"process.stdout.write(JSON.stringify({process_name}({json.dumps(example_input)})))"
    )


def run_process_with_additional_js_code(
    process_code,
    process_name,
    process_arguments,
    additional_js_code_to_run,
):
    return run_javacript(
        process_code
        + additional_js_code_to_run
        + f"process.stdout.write(JSON.stringify({process_name}({process_arguments})));"
    )


def get_evalscript_input_object(evalscript):
    return json.loads(run_javacript(evalscript + f"\nprocess.stdout.write(JSON.stringify(setup()))"))


def run_javacript(javascript_code):
    return subprocess.check_output(["node", "-e", javascript_code], stderr=subprocess.PIPE)


def load_script(source_file_folder, source_file_name):
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, f"{source_file_folder}/{source_file_name}.js")
    with open(abs_file_path) as f:
        return f.read()


def load_datacube_code():
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, f"../src/pg_to_evalscript/javascript_datacube/DataCube.js")
    with open(abs_file_path) as f:
        return f.read()


def load_process_code(process_id):
    source_files = [
        load_script("../src/pg_to_evalscript/javascript_common/", "common"),
        load_script("../src/pg_to_evalscript/javascript_processes/", process_id),
    ]
    return "\n".join(source_files)


def get_defined_processes_from_files():
    return [
        os.path.splitext(os.path.basename(file_path))[0]
        for file_path in glob.glob(f"../src/pg_to_evalscript/javascript_processes/*.js")
    ]


# helper function used for testing process inputs validation
def run_input_validation(code, process, example_input, raises_exception, error_code=None, error_message=None):
    if raises_exception:
        expected = f"code: '{error_code}'" if error_code else error_message
        assert expected != None
        try:
            run_process(code, process, example_input)
        except subprocess.CalledProcessError as exc:
            assert expected in str(exc.stderr)

    else:
        run_process(code, process, example_input)
