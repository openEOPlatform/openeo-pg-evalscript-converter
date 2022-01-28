import json
import subprocess


def get_process_graph_json(name):
    with open(f'process_graphs/{name}.json') as f:
        return json.load(f)

def get_execute_test_script(example_input):
    return f"""
process.stdout.write(JSON.stringify(evaluatePixel({json.dumps(example_input)})));
"""

def run_evalscript(evalscript, example_input):
    return subprocess.check_output(["node","-e",evalscript + get_execute_test_script(example_input)])
