import os
import uuid
import textwrap
import json

from process_graph_utils import iterate, copy_dictionary


class ProcessDefinitionMissing(Exception):
    error_code = "ProcessDefinitionMissing"

    def __init__(self, process_id):
        super().__init__(f"Process '{process_id}' doesn't have a definition file.")


class Node:
    def __init__(
        self,
        node_id,
        process_id,
        arguments,
        child_nodes,
        dependencies,
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
        self.arguments = self.prepare_arguments(arguments)
        self.process_function_name = f"{self.process_id}_{uuid.uuid4().hex}"

        if child_nodes is None:
            self.child_nodes = []
        else:
            self.child_nodes = child_nodes

    def __str__(self):
        return f"Node {self.node_id} ({self.process_id})"

    def __repr__(self):
        return f"Node {self.node_id} ({self.process_id})"

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
        json_string = json.dumps(
            self.replace_arguments_source(copy_dictionary(arguments))
        )
        return json_string.replace(f'"{self.variable_wrapper_string}', "").replace(
            f'{self.variable_wrapper_string}"', ""
        )

    def replace_arguments_source(self, arguments):
        for k, v in iterate(arguments):
            if isinstance(v, dict) and len(v) == 1 and "process_graph" in v:
                continue
            elif isinstance(v, dict) and len(v) == 1 and "from_node" in v:
                arguments[k] = (
                    self.variable_wrapper_string
                    + v["from_node"]
                    + self.variable_wrapper_string
                )
            elif isinstance(v, dict) and len(v) == 1 and "from_parameter" in v:
                arguments[k] = (
                    self.variable_wrapper_string
                    + f'arguments.{v["from_parameter"]}'
                    + self.variable_wrapper_string
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
        return self.indent_by_level(
            f"let {self.node_id} = {self.process_function_name}({self.arguments})"
        )

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
