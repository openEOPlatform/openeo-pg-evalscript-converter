import os
import json

from conversion import convert_from_process_graph


def load_pg_json(path):
    path = os.path.abspath(path)
    with open(path, "r") as f:
        pg = json.load(f)
    return pg


pg = load_pg_json("../../tests/process_graphs/gee_uc1_pol.json")

evalscripts = convert_from_process_graph(pg)
# evalscripts[0]['evalscript'].determine_output_dimensions()
print(evalscripts[0]["evalscript"].write())
