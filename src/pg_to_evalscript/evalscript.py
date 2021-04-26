from pprint import pprint
import os

from process_graph_utils import get_dependencies, get_dependents, get_execution_order

from node import Node


class Evalscript:
    def __init__(
        self,
        input_bands,
        nodes,
        initial_data_name,
        n_output_bands=1,
        sample_type="AUTO",
        units=None,
        mosaicking="mosaicking",
        bands_dimension_name="bands",
        temporal_dimension_name="t",
        datacube_definition_directory="./javascript_datacube",
    ):
        self.input_bands = input_bands
        self.nodes = nodes
        self.initial_data_name = initial_data_name
        self.n_output_bands = n_output_bands
        self.sample_type = sample_type
        self.units = units
        self.mosaicking = mosaicking
        self.datacube_definition_directory = datacube_definition_directory
        self.bands_dimension_name = bands_dimension_name
        self.temporal_dimension_name = temporal_dimension_name

    def write(self):
        newline = "\n"
        tab = "\t"
        return f"""
//VERSION=3
function setup() {{
  return {{
    input: [{",".join([f"'{band}'" for band in self.input_bands])}],
    output: {{ bands: {self.n_output_bands}, sampleType: "{self.sample_type}"{f", units: '{self.units}'" if self.units is not None else ''} }},
    mosaicking: "{self.mosaicking}"
  }};
}}
{self.write_datacube_definition()}
{newline.join([node.write_function() for node in self.nodes])}
function evaluatePixel(samples) {{
    {self.write_datacube_creation()}
    {(newline + tab).join([node.write_call() for node in self.nodes])}
    return {self.nodes[-1].node_id}.data
}}
"""

    def write_datacube_definition(self):
        path = f"{self.datacube_definition_directory}/DataCube.js"
        path = os.path.abspath(path)
        with open(path, "r") as f:
            return f.read()

    def write_datacube_creation(self):
        return f"let {self.initial_data_name} = new DataCube(samples, '{self.bands_dimension_name}', '{self.temporal_dimension_name}', true)"

    @classmethod
    def generate_nodes_from_process_graph(self, process_graph, level=1):
        dependency_graph = get_dependencies(process_graph)
        # print("dependency_graph   =>")
        # pprint(dependency_graph)
        dependents = get_dependents(dependency_graph)
        # print("dependents   =>")
        # pprint(dependents)
        execution_order = get_execution_order(dependency_graph, dependents)
        # print("execution_order   =>")
        # pprint(execution_order)

        nodes = []
        input_bands = None
        initial_data_name = None

        for node_id in execution_order:
            process_id = process_graph[node_id]["process_id"]
            arguments = process_graph[node_id]["arguments"]
            child_nodes = None

            if process_id == "load_collection":
                input_bands = arguments["bands"]
                initial_data_name = node_id
                continue
            elif process_id == "save_result":
                continue
            elif process_id == "reduce_dimension":
                child_nodes, _, _ = self.generate_nodes_from_process_graph(
                    arguments["reducer"]["process_graph"], level=level + 1
                )

            node = Node(
                node_id,
                process_id,
                arguments,
                child_nodes,
                dependency_graph[node_id],
                level,
            )
            nodes.append(node)

        return nodes, input_bands, initial_data_name

    @classmethod
    def from_process_graph(
        self, process_graph, n_output_bands=1, sample_type="AUTO", units=None
    ):
        nodes, input_bands, initial_data_name = self.generate_nodes_from_process_graph(
            process_graph
        )

        return Evalscript(
            input_bands,
            nodes,
            initial_data_name,
            n_output_bands=n_output_bands,
            sample_type=sample_type,
            units=units,
        )
