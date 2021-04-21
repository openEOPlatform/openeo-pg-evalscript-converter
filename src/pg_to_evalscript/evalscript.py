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
    ):
        self.input_bands = input_bands
        self.nodes = nodes
        self.initial_data_name = initial_data_name
        self.n_output_bands = n_output_bands
        self.sample_type = sample_type
        self.units = units
        self.mosaicking = mosaicking

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
{newline.join([node.write_function() for node in self.nodes])}
function evaluatePixel({self.initial_data_name}) {{
    {(newline + tab).join([node.write_call() for node in self.nodes])}
    return {self.nodes[-1].node_id}
}}
"""

    @classmethod
    def generate_nodes_from_process_graph(self, process_graph, level=1):
        dependency_graph = get_dependencies(process_graph)
        dependents = get_dependents(dependency_graph)
        execution_order = get_execution_order(dependency_graph, dependents)

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
