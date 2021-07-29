import os
import uuid
import textwrap
import json
from collections import defaultdict

from process_graph_utils import iterate, copy_dictionary


class ProcessDefinitionMissing(Exception):
    error_code = "ProcessDefinitionMissing"

    def __init__(self, process_id):
        super().__init__(f"Process '{process_id}' doesn't have a definition file.")


def pprint_dict(dictionary):
    return "\n".join("{}\t{}".format(k, v) for k, v in dictionary.items())


class Node:
    def __init__(
        self,
        node_id,
        process_id,
        arguments,
        child_nodes,
        dependencies,
        dependents,
        level,
        process_definitions_directory="./javascript_processes",
    ):
        self.variable_wrapper_string = uuid.uuid4().hex
        self.node_id = node_id
        self.level = level
        self.process_definitions_directory = process_definitions_directory

        if self.is_process_defined(process_id):
            self.process_id = process_id
        else:
            raise ProcessDefinitionMissing(process_id)

        self.dependencies = dependencies
        self.dependents = dependents
        self._original_arguments = arguments
        self.arguments = self.prepare_arguments(arguments)
        self.process_function_name = f"{self.process_id}_{uuid.uuid4().hex}"

        if child_nodes is None:
            self.child_nodes = []
        else:
            self.child_nodes = child_nodes

    def __str__(self):
        delimiter = "-" * 80
        arguments = textwrap.indent(json.dumps(self._original_arguments, indent=4), "\t")
        return f"{delimiter}\nNode {self.node_id} ({self.process_id})\n\n\tArguments:\n{arguments}\n{delimiter}"

    def __repr__(self):
        return f"Node {self.node_id} ({self.process_id})\n"

    def get_process_definition_path(self, process_id):
        path = f"{self.process_definitions_directory}/{process_id}.js"
        return os.path.abspath(path)

    def is_process_defined(self, process_id):
        special_processes_without_definition = [
            "reduce_dimension",
            "load_collection",
            "save_result",
        ]
        if process_id in special_processes_without_definition:
            return True
        path = self.get_process_definition_path(process_id)
        return os.path.isfile(path)

    def indent_by_level(self, string):
        return textwrap.indent(string, "\t" * self.level)

    def prepare_arguments(self, arguments):
        json_string = json.dumps(self.replace_arguments_source(copy_dictionary(arguments)))
        return json_string.replace(f'"{self.variable_wrapper_string}', "").replace(
            f'{self.variable_wrapper_string}"', ""
        )

    def replace_arguments_source(self, arguments):
        for k, v in iterate(arguments):
            if isinstance(v, dict) and len(v) == 1 and "process_graph" in v:
                continue
            elif isinstance(v, dict) and len(v) == 1 and "from_node" in v:
                arguments[k] = self.variable_wrapper_string + v["from_node"] + self.variable_wrapper_string
            elif isinstance(v, dict) and len(v) == 1 and "from_parameter" in v:
                arguments[k] = (
                    self.variable_wrapper_string + f'arguments.{v["from_parameter"]}' + self.variable_wrapper_string
                )
            elif isinstance(v, dict) or isinstance(v, list):
                self.replace_arguments_source(v)
        return arguments

    def load_process_code(self):
        path = self.get_process_definition_path(self.process_id)
        try:
            with open(path, "r") as f:
                return f.read()
        except IOError as error:
            return None

    def write_process(self):
        if self.process_id == "reduce_dimension":
            process_definition = self.write_reduce_dimension()
        else:
            process_definition = self.load_process_code()

        if process_definition is None:
            return f"""function {self.process_id}(arguments) {{
    const {{lmao}} = arguments;
    return lmao + 42;
}}"""
        return self.indent_by_level(process_definition)

    def write_call(self):
        return self.indent_by_level(f"let {self.node_id} = {self.process_function_name}({self.arguments})")

    def write_function(self):
        newline = "\n"
        tab = "\t"
        return self.indent_by_level(
            f"""
function {self.process_function_name}(arguments) {{
{self.write_process()}
    return {self.process_id}(arguments)
}}
"""
        )

    def write_reduce_dimension(self):
        newline = "\n"
        tab = "\t"
        return f"""
function reduce_dimension(arguments) {{
    function reducer(arguments) {{
    {newline.join(node.write_function() for node in self.child_nodes)}
    {newline.join(node.write_call() for node in self.child_nodes)}
        return {self.child_nodes[-1].node_id};
    }}

    const {{data, dimension}} = arguments; 
    const newData = data.clone()
    newData.reduceByDimension(reducer, dimension)
    return newData;
}}
"""

    def get_dimensions_change(self, dimensions_of_inputs):
        # print(dimensions_of_inputs)
        def remove_dimension(name, dims):
            return list(filter(lambda x: x["name"] != name, dims))

        if self.process_id == "reduce_dimension":
            return remove_dimension(self._original_arguments["dimension"], dimensions_of_inputs[0])
        elif self.process_id == "add_dimension":
            return [*dimensions_of_inputs[0], {"name": self._original_arguments["name"], "size": 1}]
        elif self.process_id == "merge_cubes":
            """
            merge_cubes process expects datacubes to have different labels in a single dimension.
            We can't know which dimension is it and what the new size will be.
            We can arbitrarily choose one and set its size to the sum, as it might get removed/reduced by later nodes
            So we set new sizes to the sums for *all* dimensions
            """
            dim_size_sums = defaultdict(int)

            for dimensions_of_input in dimensions_of_inputs:
                for dim in dimensions_of_input:
                    if dim["size"] is not None:
                        dim_size_sums[dim["name"]] += dim["size"]
                    else:
                        dim_size_sums[dim["name"]] = None

            output_dimensions = []
            for dim in dim_size_sums:
                output_dimensions.append({"name": dim, "size": dim_size_sums[dim]})

            return output_dimensions
        return dimensions_of_inputs[0]
