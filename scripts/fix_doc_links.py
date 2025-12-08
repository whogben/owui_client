import ast
import os
import re
from typing import Set, Dict, Optional

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")


class ImportCollector(ast.NodeVisitor):
    def __init__(self):
        self.imports: Dict[str, str] = {}  # alias -> full_path
        self.classes: Set[str] = set()  # locally defined classes

    def visit_Import(self, node: ast.Import):
        for name in node.names:
            alias = name.asname or name.name
            self.imports[alias] = name.name

    def visit_ImportFrom(self, node: ast.ImportFrom):
        module = node.module or ""
        for name in node.names:
            alias = name.asname or name.name
            full_name = f"{module}.{name.name}" if module else name.name
            self.imports[alias] = full_name

    def visit_ClassDef(self, node: ast.ClassDef):
        self.classes.add(node.name)
        self.generic_visit(node)


def get_module_path(file_path: str) -> str:
    rel_path = os.path.relpath(file_path, SRC_ROOT)
    return rel_path.replace(os.sep, ".").replace(".py", "")


def fix_docstrings_in_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except:
        return

    collector = ImportCollector()
    collector.visit(tree)

    current_module = get_module_path(file_path)

    def replacer(match):
        full_match = match.group(0)  # `Reference`
        inner = match.group(1)  # Reference

        if "." not in inner:
            return full_match

        parts = inner.split(".")
        root_obj = parts[0]

        if inner.startswith("owui_client"):
            return full_match

        if root_obj in collector.classes:
            return f"[{current_module}.{inner}][]"

        if root_obj in collector.imports:
            imported_path = collector.imports[root_obj]
            remaining = ".".join(parts[1:])
            return f"[{imported_path}.{remaining}][]"

        return full_match

    new_content = re.sub(r"`([a-zA-Z_]\w*\.[a-zA-Z0-9_.]+)`", replacer, content)

    if new_content != content:
        print(f"Updating {file_path}")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)


def main():
    target_dir = os.path.join(SRC_ROOT, "owui_client")
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".py"):
                fix_docstrings_in_file(os.path.join(root, file))


if __name__ == "__main__":
    main()
