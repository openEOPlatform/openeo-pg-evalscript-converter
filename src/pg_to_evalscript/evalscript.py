import os


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
