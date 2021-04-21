import os
from pprint import pprint
import json

from evalscript import Evalscript


def load_pg_json(path):
    path = os.path.abspath(path)
    with open(path, "r") as f:
        pg = json.load(f)
    return pg


pg = load_pg_json("../../tests/process_graphs/max_ndvi.json")


evalscript = Evalscript.from_process_graph(pg)
print(evalscript.write())
