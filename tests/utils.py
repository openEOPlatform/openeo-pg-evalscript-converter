import os
import json
import glob
import uuid
import platform
import subprocess


def get_abs_file_path(rel_file_path):
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, rel_file_path)


def get_process_graph_json(name):
    abs_file_path = get_abs_file_path(f"process_graphs/{name}.json")
    with open(abs_file_path) as f:
        return json.load(f)


def with_stdout_call(code):
    return f"\nprocess.stdout.write(JSON.stringify({code}))"


def get_execute_test_script(example_input, scenes=None):
    return with_stdout_call(f"evaluatePixel({json.dumps(example_input)}, {json.dumps(scenes)})")


def run_evalscript(evalscript, example_input, scenes=None):
    return run_javascript(evalscript + get_execute_test_script(example_input, scenes))


def run_process(process_code, process_name, example_input):
    input_arguments = json.dumps(example_input) if type(example_input) is dict else example_input
    return run_javascript(process_code + with_stdout_call(f"{process_name}({input_arguments})"))


def get_evalscript_input_object(evalscript):
    return json.loads(run_javascript(evalscript + with_stdout_call("setup()")))

def get_n_output_bands(evalscript,n_scenes=1):
    return json.loads(run_javascript(evalscript + f"""
const outputs={{'default':{{'bands':1}}}};
const collections = {{"scenes": {{"length":{n_scenes}}}}};
updateOutput(outputs,collections);\n"""
    + with_stdout_call("outputs ['default']")
    ))

def run_javascript(javascript_code):
    if platform.system() == "Windows":
        abs_file_path = get_abs_file_path(f"test_code_{uuid.uuid4()}.js")
        with open(abs_file_path, "w") as f:
            f.write(javascript_code)

        try:
            return subprocess.check_output(["node", abs_file_path], stderr=subprocess.PIPE)
        finally:
            os.remove(abs_file_path)
    else:
        return subprocess.check_output(["node", "-e", javascript_code], stderr=subprocess.PIPE)


def load_script(source_file_folder, source_file_name):
    abs_file_path = get_abs_file_path(f"{source_file_folder}/{source_file_name}.js")
    with open(abs_file_path) as f:
        return f.read()


def load_datacube_code():
    ndarray_code = load_script("../src/pg_to_evalscript/javascript_datacube/", "ndarray")
    datacube_code = load_script("../src/pg_to_evalscript/javascript_datacube/", "DataCube")
    return ndarray_code + datacube_code


def load_process_code(process_id):
    source_files = [
        load_script("../src/pg_to_evalscript/javascript_common/", "common"),
        load_script("../src/pg_to_evalscript/javascript_processes/", process_id),
    ]
    return "\n".join(source_files)


def load_dependency_processes_code(process_ids):
    path = "../src/pg_to_evalscript/javascript_processes/"
    source_files = [load_script(path, process_id) for process_id in process_ids]
    return "\n".join(source_files)


def get_defined_processes_from_files():
    return [
        os.path.splitext(os.path.basename(file_path))[0]
        for file_path in glob.glob(f"../src/pg_to_evalscript/javascript_processes/*.js")
    ]


# helper function used for testing process inputs validation
def run_input_validation(code, process, example_input, raises_exception, error_name=None, error_message=None):
    if raises_exception:
        expected = error_name if error_name else error_message
        assert expected != None
        try:
            run_process(code, process, example_input)
            # it should always throw an exception
            assert False, "Process was expected to raise an error, but did not."
        except subprocess.CalledProcessError as exc:
            assert expected in str(exc.stderr), f"assert {expected} in {str(exc.stderr)}"

    else:
        run_process(code, process, example_input)
