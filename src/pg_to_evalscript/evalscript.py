import os
import json
import pkgutil
from functools import reduce
from collections import defaultdict
from operator import mul


def reshape(lst, shape):
    if len(shape) == 1:
        if len(lst) != shape[0]:
            raise Exception("Incorrect shape for input list.")
        return lst
    n = reduce(mul, shape[1:])
    return [reshape(lst[i * n : (i + 1) * n], shape[1:]) for i in range(shape[0])]


class Evalscript:
    def __init__(
        self,
        input_bands,
        nodes,
        initial_data_names,
        n_output_bands=1,
        sample_type="AUTO",
        units=None,
        mosaicking="ORBIT",
        bands_dimension_name="bands",
        temporal_dimension_name="t",
        datacube_definition_directory="javascript_datacube",
        output_dimensions=None,
        encode_result=True,
        bands_metadata={},
    ):
        self.input_bands = input_bands
        self.nodes = nodes
        self.initial_data_names = initial_data_names
        self.n_output_bands = n_output_bands
        self.sample_type = sample_type
        self.units = units
        self.mosaicking = mosaicking
        self.datacube_definition_directory = datacube_definition_directory
        self.bands_dimension_name = bands_dimension_name
        self.temporal_dimension_name = temporal_dimension_name
        self._output_dimensions = output_dimensions
        self.encode_result = encode_result
        self.bands_metadata = bands_metadata

    def write(self):
        if any(datasource_with_bands["bands"] is None for datasource_with_bands in self.input_bands):
            raise Exception("input_bands must be set!")
        newline = "\n"
        tab = "\t"
        return f"""
//VERSION=3
function setup() {{
  return {{
    input: [{",".join([f"{datasource_with_bands}" for datasource_with_bands in self.input_bands])}],
    output: {{ bands: {self.n_output_bands}, sampleType: "{self.sample_type}"{f", units: '{self.units}'" if self.units is not None else ''} }},
    mosaicking: "{self.mosaicking}"
  }};
}}
{self.write_update_output()}
{self.write_runtime_global_constants()}
{self.write_common_definition()}
{self.write_ndarray_definition()}
{self.write_datacube_definition()}
{newline.join([node.write_function() for node in self.nodes])}

// this var gets metadata about the dimensions of the datacube for postprocessing
// it is saved as userdata.json 
let forUserData = {{}};

function evaluatePixel(samples, scenes) {{
    {self.write_datacube_creation()}
    {(newline + tab).join([node.write_call() for node in self.nodes])}

    forUserData = {{
        outputDimensions: {self.write_output_variable()}.dimensions,
        outputDatacubeMetadata: {{
            shape: {self.write_output_variable()}.data.shape, 
            stride: {self.write_output_variable()}.data.stride, 
            offset: {self.write_output_variable()}.data.offset
        }}
    }}

    const finalOutput = {self.write_output_variable()}{".encodeData()" if self.encode_result else '.flattenToArray()'}
    return Array.isArray(finalOutput) ? finalOutput : [finalOutput];
}}

function updateOutputMetadata(scenes, inputMetadata, outputMetadata) {{
  outputMetadata.userData = forUserData;
}}
"""

    def write_datacube_definition(self):
        return pkgutil.get_data("pg_to_evalscript", f"{self.datacube_definition_directory}/DataCube.js").decode("utf-8")

    def write_common_definition(self):
        return pkgutil.get_data("pg_to_evalscript", f"javascript_common/common.js").decode("utf-8")

    def write_ndarray_definition(self):
        return pkgutil.get_data("pg_to_evalscript", f"javascript_datacube/ndarray.js").decode("utf-8")

    def write_datacube_creation(self):
        datacube_creation = ""
        if len(self.input_bands) > 1:
            for datasource_with_bands in self.input_bands:
                datasource_name = datasource_with_bands["datasource"]
                datacube_creation += f"let {datasource_name} = new DataCube(samples.{datasource_name}, '{self.bands_dimension_name}', '{self.temporal_dimension_name}', true, {json.dumps(self.bands_metadata[datasource_name] if self.bands_metadata is not None and len(self.bands_metadata) > 0 else None)}, scenes)\n\t"
        else:
            datasource_with_bands = self.input_bands[0]
            datasource_name = datasource_with_bands["datasource"]
            datacube_creation += f"let {datasource_name} = new DataCube(samples, '{self.bands_dimension_name}', '{self.temporal_dimension_name}', true, {json.dumps(self.bands_metadata[datasource_name] if self.bands_metadata is not None and len(self.bands_metadata) > 0 else None)}, scenes)\n\t"

        return datacube_creation

    def write_runtime_global_constants(self):
        all_bands = []
        for datasource_with_bands in self.input_bands:
            all_bands.extend(datasource_with_bands["bands"])

        return f"const INPUT_BANDS = {list(set(all_bands))};"

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
            lambda x, y: x * y, sizes_without_original_temporal_dimensions, 1
        )
        if len(self.input_bands) > 1:
            collection_scenes_length = (
                "* Object.values(collection).reduce((acc, val) => acc + val.scenes.length, 0)"
                * number_of_original_temporal_dimensions
            )
        else:
            collection_scenes_length = "* collection.scenes.length" * number_of_original_temporal_dimensions
        number_of_final_dimensions = len(self._output_dimensions) + 1 if self.encode_result else 0
        return f"""
function updateOutput(outputs, collection) {{
    Object.values(outputs).forEach((output) => {{
        output.bands = {number_of_final_dimensions} + {size_without_original_temporal_dimensions} {collection_scenes_length};
    }});
}}"""

    def write_output_variable(self):
        if len(self.nodes) == 0:
            return "_".join(self.initial_data_names.values())
        return self.nodes[-1].node_varname_prefix + self.nodes[-1].node_id

    def determine_output_dimensions(self):
        dimensions_of_inputs_per_node = defaultdict(list)
        all_bands = []
        for datasource_with_bands in self.input_bands:
            if datasource_with_bands is not None and datasource_with_bands["bands"] is not None:
                all_bands.extend(datasource_with_bands["bands"])

        initial_output_dimensions = [
            {"name": self.bands_dimension_name, "size": len(set(all_bands)) if self.input_bands is not None else 0},
            {"name": self.temporal_dimension_name, "size": None, "original_temporal": True},
        ]

        if len(self.nodes) == 0:
            return initial_output_dimensions

        dimensions_of_inputs_per_node[self.nodes[0].node_id].append(initial_output_dimensions)

        for node in self.nodes:
            output_dimensions = node.get_dimensions_change(dimensions_of_inputs_per_node[node.node_id] if len(dimensions_of_inputs_per_node[node.node_id]) > 0 else [initial_output_dimensions])
            for dependent in node.dependents:
                dimensions_of_inputs_per_node[dependent].append(output_dimensions)

        return output_dimensions

    def set_output_dimensions(self, output_dimensions):
        self._output_dimensions = output_dimensions

    def set_input_bands(self, input_bands):
        self.input_bands = input_bands
        output_dimensions = self.determine_output_dimensions()
        self.set_output_dimensions(output_dimensions)

    def get_decoding_function(self):
        """
        Returns a function, which accepts data produced by this evalscript, and converts it to the correct format.
        This function might change depending on sampleType and other optimisations in the future (not implemented yet).
        """

        if not self.encode_result:
            return lambda x: x

        def decode_data(data):
            n_dimensions = len(self._output_dimensions)
            for i in range(len(data)):
                for j in range(len(data[0])):
                    data_start_ind = n_dimensions
                    dimension_sizes = data[i][j][0:data_start_ind]
                    data_length = int(reduce(lambda x, y: x * y, dimension_sizes))
                    values = data[i][j][data_start_ind : data_start_ind + data_length]
                    data[i][j] = reshape(values, dimension_sizes)
            return data

        return decode_data
