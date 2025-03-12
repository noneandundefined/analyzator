# *---------------------------------------------------------------------------------------------
# *  Copyright (c). All rights reserved.
# *  Licensed under the LICENSE-APACHE. See License.txt in the project root for license information.
# *--------------------------------------------------------------------------------------------*


import os
import re
import ast

SUPPORTED_EXTENSIONS = (".scala", ".go", ".js", ".ts")


def unused_python(code):
    tree = ast.parse(code)
    defined_vars = set()
    used_vars = set()
    defined_funcs = set()
    used_funcs = set()

    class Visitor(ast.NodeVisitor):
        def visit_Assign(self, node):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    defined_vars.add(target.id)
            self.generic_visit(node)

        def visit_Name(self, node):
            used_vars.add(node.id)
            self.generic_visit(node)

        def visit_FunctionDef(self, node):
            defined_funcs.add(node.name)
            self.generic_visit(node)

        def visit_Call(self, node):
            if isinstance(node.func, ast.Name):
                used_funcs.add(node.func.id)
            self.generic_visit(node)

    Visitor().visit(tree)

    unused_vars = defined_vars - used_vars
    unused_funcs = defined_funcs - used_funcs

    return unused_vars, unused_funcs


def extract_unused_with_treesitter(file_path):
    """Analyzes the file and finds unused variables and functions"""
    with open(file_path, "rb") as f:
        code = f.readlines()

    patterns = {
        "scala": [r"val (\w+)", r"def (\w+)\("],
        "go": [r"var (\w+)", r"func (\w+)\("],
        "js": [r"const (\w+)", r"let (\w+)", r"function (\w+)\("],
        "ts": [r"const (\w+)", r"let (\w+)", r"function (\w+)\("],
    }

    ext = os.path.splitext(file_path)[1][1:]
    if ext not in patterns:
        return

    unused = []
    for pattern in patterns[ext]:
        matches = re.findall(pattern, "\n".join(code))
        for match in matches:
            if sum(1 for line in code if match in line) == 1:
                unused.append(match)

    if unused:
        print(
            f"\033[93mFile {file_path} unused elements found: {', '.join(unused)}\033[0m"
        )


def analyze_file(filepath):
    """Analyzes the file for unused variables and functions."""
    ext = os.path.splitext(filepath)[1]
    unused_vars = []
    unused_funcs = []

    with open(filepath, "rb") as f:
        code = f.read()

    if ext == ".py":
        unused_vars, unused_funcs = unused_python(code)
    else:
        extract_unused_with_treesitter(filepath)

    if unused_vars or unused_funcs:
        print(f"\nФайл: {filepath}")
        if unused_vars:
            print(f"\033[93m[UNUSED] Unused variables: {', '.join(unused_vars)}\033[0m")
        if unused_funcs:
            print(
                f"\033[93m[UNUSED] Unused public functions: {', '.join(unused_funcs)}\033[0m"
            )


def traverse_directory(directory, ignore=[""]):
    """Recursively traverses the directory and analyzes the code files."""
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignore]
        for file in files:
            if file in ignore:
                continue
            analyze_file(os.path.join(root, file))
