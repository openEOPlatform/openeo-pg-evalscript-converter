import os
from functools import reduce
from collections import defaultdict


class Evalscript:
    def __init__(
        self,
        input_bands,
        nodes,
        initial_data_name,
        n_output_bands=1,
        sample_type="AUTO",
        units=None,
        mosaicking="ORBIT",
        bands_dimension_name="bands",
        temporal_dimension_name="t",
        datacube_definition_directory="./javascript_datacube",
        output_dimensions=None,
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
        self._output_dimensions = output_dimensions

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
{self.write_update_output()}
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

    def write_update_output(self):
        if self._output_dimensions is None:
            return ""
        number_of_original_temporal_dimensions = len(
            [dim for dim in self._output_dimensions if dim.get("original_temporal", False)]
        )
        sizes_without_original_temporal_dimensions = [
            dim["size"] for dim in self._output_dimensions if not dim.get("original_temporal", False)
        ]
        size_without_original_temporal_dimensions = reduce(
            lambda x, y: x * y, sizes_without_original_temporal_dimensions
        )
        collection_scenes_length = "* collection.scenes.length" * number_of_original_temporal_dimensions
        return f"""
function updateOutput(outputs, collection) {{
    Object.values(outputs).forEach((output) => {{
        output.bands = {size_without_original_temporal_dimensions} {collection_scenes_length};
    }});
}}"""

    def determine_output_dimensions(self):
        dimensions_of_inputs_per_node = defaultdict(list)
        initial_output_dimensions = [
            {"name": self.bands_dimension_name, "size": len(self.input_bands)},
            {"name": self.temporal_dimension_name, "size": None, "original_temporal": True},
        ]
        dimensions_of_inputs_per_node[self.nodes[0].node_id].append(initial_output_dimensions)

        for node in self.nodes:
            output_dimensions = node.get_dimensions_change(dimensions_of_inputs_per_node[node.node_id])
            for dependent in node.dependents:
                dimensions_of_inputs_per_node[dependent].append(output_dimensions)

        return output_dimensions

    def set_output_dimensions(self, output_dimensions):
        self._output_dimensions = output_dimensions
