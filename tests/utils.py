import os
import json
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


def run_javacript(javascript_code):
    return subprocess.check_output(["node", "-e", javascript_code])


def load_process_code(process_id):
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, f"../src/pg_to_evalscript/javascript_processes/{process_id}.js")
    with open(abs_file_path) as f:
        return f.read()
