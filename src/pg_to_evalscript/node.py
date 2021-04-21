import os
import uuid
import textwrap

from process_graph_utils import iterate, copy_dictionary


class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


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
        self.node_id = node_id
        self.process_id = process_id
        self.dependencies = dependencies
        self.arguments = self.replace_arguments_source(copy_dictionary(arguments))
        self.process_function_name = f"{self.process_id}_{uuid.uuid4()}"
        self.level = level
        self.process_definitions_directory = process_definitions_directory

        if child_nodes is None:
            self.child_nodes = []
        else:
            self.child_nodes = child_nodes

    def __str__(self):
        return f"Node {self.node_id} ({self.process_id})"

    def __repr__(self):
        return f"Node {self.node_id} ({self.process_id})"

    def replace_arguments_source(self, arguments):
        for k, v in iterate(arguments):
            if isinstance(v, dict) and len(v) == 1 and "from_node" in v:
                arguments[k] = Variable(v["from_node"])
            elif isinstance(v, dict) or isinstance(v, list):
                self.replace_arguments_source(v)
        return arguments

    def load_process_code(self):
        path = f"{self.process_definitions_directory}/{self.process_id}.js"
        path = os.path.abspath(path)
        try:
            with open(path, "r") as f:
                return f.read()
        except IOError as error:
            return None

    def write_process(self):
        process_definition = self.load_process_code()

        if process_definition is None:
            return ""
        return textwrap.indent(process_definition, "\t" * self.level)

    def write_call(self):
        return f"let {self.node_id} = {self.process_function_name}({self.arguments})"

    def write_function(self):
        newline = "\n"
        tab = "\t"
        return f"""
function {self.process_function_name}(arguments) {{
{self.write_process()}
    {(newline + self.level*tab).join(node.write_function() for node in self.child_nodes)}
    {(newline + self.level*tab).join(node.write_call() for node in self.child_nodes)}
    return {self.process_id}(arguments)
}}
"""
