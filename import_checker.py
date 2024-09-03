import ast
import os
import json

from anytree import RenderTree, NodeMixin

import_dict = {}

ref_dict = {
    "Property": [
        "math",
        "enum",
        "typing",
        "Compare",
        "Convert",
        "Unit"
    ],
    "Compare": [
        "math",
        "ctypes"
    ],
    "Convert": [
        "math",
        "re",
        "typing",
        "numpy",
        "Aggregate",
        "Converted",
        "Object",
        "Output",
        "Property",
        "Unit"
    ],
    "Aggregate": [
        "math",
        "re",
        "enum"
    ],
    "Object": [
        "math",
        "re",
        "threading",
        "time",
        "datetime",
        "enum",
        "typing",
        "ElementTree",
        "numpy",
        "Class",
        "Exec",
        "GridLabD",
        "Platform",
        "Property",
        "TimeStamp"
    ],
    "Class": [
        "json",
        "warnings",
        "enum",
        "typing",
        "ElementTree",
        "Globals",
        "Property"
    ],
    "Exec": [
        "subprocess",
        "signal",
        "select",
        "datetime",
        "enum",
        "socket",
        "Globals",
        "GridLabD",
        "Output",
        "Local",
        "gldcore",
        "Class",
        "Cmdarg",
        "CppThreadPool",
        "Debug",
        "DeltaMode",
        "Enduse",
        "Gui",
        "Instance",
        "Loadshape",
        "Module",
        "Object",
        "Realtime",
        "Schedule",
        "Stream",
        "Test",
        "TimeStamp",
        "Realtime",
        "Threadpool",
        "Transform"
    ],
    "Cmdarg": [
        "sched",
        "ctypes",
        "time",
        "logging",
        "sys",
        "os",
        "platform",
        "QJsonValue",
        "Class",
        "Globals",
        "Output",
        "Property",
        "Job",
        "Legal",
        "Validate",
        "Cmex",
        "Enduse",
        "Exec",
        "GldRandom",
        "GridLabD",
        "Loadshape",
        "Module",
        "Sanitize",
        "Schedule",
        "Test",
        "TimeStamp",
        "Unit",
        "json"
    ],
    "Cmex": [
        "ctypes",
        "util",
        "enum",
        "numpy",
        "os",
        "gldcore",
        "Class",
        "Cmdarg",
        "Object",
        "Convert",
        "Exec",
        "Find",
        "Globals",
        "Property",
        "TimeStamp"
    ],
    "Enduse": [
        "math",
        "re",
        "CsvReader",
        "Class",
        "Convert",
        "Exec",
        "TimeStamp",
        "Output",
        "Property",
        "enum",
        "ctypes",
        "Globals"
    ],
    "Globals": [
        "copy",
        "math",
        "threading",
        "random",
        "time",
        "re",
        "sys",
        "os",
        "enum",
        "Output",
        "Property",
        "Version"
    ],
    "GldRandom": [],
    "GridLabD": [
        "errno",
        "logging",
        "os",
        "ctypes",
        "math",
        "time",
        "datetime",
        "inspect",
        "Output",
        "gldcore",
        "Version",
        "glob"
    ],
    "Version": [],
    "Loadshape": [],
    "Module": [
        "io",
        "threading",
        "subprocess",
        "errno",
        "os",
        "typing",
        "gldcore",
        "Globals",
        "Output",
        "Load",
        "Find",
        "GridLabD",
        "Transform",
        "Version"
    ],
    "Find": [
        "os",
        "enum",
        "re",
        "typing"
    ],
    "Transform": [
        "enum",
        "numpy",
        "Object",
        "Output",
        "Module",
        "Property"
    ],
    "Sanitize": [
        "math",
        "enum",
        "gldcore",
        "Object"
    ],
    "Schedule": [
        "datetime",
        "threading",
        "time",
        "CsvReader",
        "Test",
        "Convert",
        "Globals",
        "GridLabD",
        "Output"
    ],
    "Test": [],
    "TimeStamp": [
        "re",
        "time",
        "datetime",
        "pytz",
        "typing"
    ],
    "Unit": [
        "math",
        "re"
    ],
    "CppThreadPool": [
        "os",
        "threading",
        "queue",
        "time"
    ],
    "Debug": [
        "enum",
        "numpy",
        "os",
        "subprocess",
        "Convert",
        "Output",
        "Property",
        "Object",
        "TimeStamp",
        "gldcore",
        "Class",
        "Cmdarg",
        "Exec",
        "Find",
        "Globals",
        "datetime"
    ],
    "DeltaMode": [
        "typing",
        "time",
        "math",
        "Globals",
        "TimeStamp",
        "GridLabD",
        "Module",
        "Object"
    ],
    "Gui": [
        "os",
        "time",
        "enum",
        "sys",
        "ctypes",
        "Class",
        "Cmex",
        "Convert",
        "Globals",
        "Output",
        "GridLabD",
        "Object",
        "Environment",
        "Find"
    ],
    "Environment": [
        "Exec",
        "Output",
        "Gui",
        "Globals",
        "Matlab",
        "Xcore"
    ],
    "Instance": [
        "time",
        "os",
        "typing",
        "threading",
        "Connection",
        "Exec",
        "GldRandom",
        "Globals",
        "Output",
        "enum",
        "socket",
        "random"
    ],
    "Connection": [
        "GridLabD",
        "ctypes",
        "re",
        "sys",
        "enum",
        "traceback"
    ],
    "Output": [
        "sys",
        "os",
        "atexit",
        "enum",
        "typing"
    ],
    "Realtime": [
        "time",
        "Globals"
    ],
    "Stream": [
        "Class",
        "Globals",
        "Output",
        "Module",
        "Object",
        "struct"
    ],
    "Platform": [
        "math",
        "sys"
    ]
}


class MyCustomNode(NodeMixin):
    RED = '\033[31m'  # Red text
    GREEN = '\033[32m'  # Green text
    YELLOW = '\033[33m'  # Yellow text
    BLUE = '\033[34m'  # Blue text
    RESET = '\033[0m'  # Reset to default color
    def __init__(self, name, parent=None, children=None, color=None):
        super().__init__()
        self.name = name
        self.parent = parent
        self.color = color  # should be MyCustomNode.RED, MyCustomNode.GREEN, MyCustomNode.BLUE
        if children:
            self.children = children

    def __str__(self):
        if self.color:
            s = f"{self.color}{self.name}{self.RESET}"
        else:
            s = f"{self.name}"
        return s


def render_tree(my_dict):
    recommendations = []
    all_nodes = []
    keys = list(my_dict.keys())
    root = MyCustomNode(keys[0])
    children = my_dict[keys[0]]
    visited_nodes = [keys[0]]
    for child in children:
        if child in visited_nodes:
            if child[0]==child[0].upper():
                color = MyCustomNode.RED
                recommendations.append(
                    f"Pull out the {child} components needed for {root} and place them in a separate file.")
            else:
                color = MyCustomNode.BLUE
        else:
            visited_nodes.append(child)
            color = None
        child_node = MyCustomNode(child, parent=root, color=color)
        all_nodes.append(child_node)
        if child in keys:
            for grandchild in my_dict[child]:
                if grandchild in visited_nodes:
                    if grandchild[0] == grandchild[0].upper():
                        color = MyCustomNode.RED
                        recommendations.append(
                            f"Pull out the {grandchild} components needed for {child} and place them in a separate file.")
                    else:
                        color = MyCustomNode.BLUE
                else:
                    visited_nodes.append(grandchild)
                    color = None
                grandchild_node = MyCustomNode(grandchild, parent=child_node, color=color)
                all_nodes.append(grandchild_node)
                if grandchild in keys:
                    for greatgrandchild in my_dict[grandchild]:
                        if greatgrandchild in visited_nodes:
                            if greatgrandchild[0] == greatgrandchild[0].upper():
                                color = MyCustomNode.RED
                                recommendations.append(
                                    f"Pull out the {greatgrandchild} components needed for {grandchild} and place them in a separate file.")
                            else:
                                color = MyCustomNode.BLUE
                        else:
                            visited_nodes.append(greatgrandchild)
                            color = None
                        greatgrandchild_node = MyCustomNode(greatgrandchild, parent=grandchild_node, color=color)
                        all_nodes.append(greatgrandchild_node)

    print(f"Color legend: {MyCustomNode.RED}\n    RED: Circular dependencies{MyCustomNode.RESET}\n{MyCustomNode.BLUE}    BLUE: Standard library reimport{MyCustomNode.RESET}\n")
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node))
    print("Recommendations:")
    for i, r in enumerate(recommendations):
        print(f"{i+1}: {r}")


def parse_file(filename, base_path):
    global import_dict
    """Parse a Python file and return a list of its imports."""
    full_path = os.path.join(base_path, filename)
    imports = []
    if os.path.exists(full_path):
        with open(full_path, "r") as file:
            tree = ast.parse(file.read(), filename=full_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.append(name.name)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module)
    this_key = filename.split('/')[-1].replace('.py','')
    if this_key not in import_dict.keys():
        import_dict[this_key] = []
        for imp in imports:
            new_filename = f"{imp.replace('.','/')}.py"
            next_file = os.path.join(base_path, new_filename)
            if os.path.exists(next_file):
                # print("next file: ", next_file)
                if next_file:
                    # recurse into the next file
                    parse_file(new_filename, base_path)
            if imp not in import_dict[this_key]:
                import_item = imp.split('.')[-1]
                import_dict[this_key].append(import_item)
    else:
        pass
        # print(f"skipped: {this_key} (already in the dict)")

    return imports


if __name__ == '__main__':

    # Example usage
    root = "./gov_pnnl_goss/"
    start_file = "gridlab/gldcore/Property.py"

    parse_file(start_file, root)
    # print(json.dumps(import_dict, indent=4))
    render_tree(import_dict)
    pass
