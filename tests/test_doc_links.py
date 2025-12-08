import ast
import os
import re
import pytest
from typing import Set, Tuple, Generator, List

# Paths
# Assumes this test file is in owui_client/tests/
# and source is in owui_client/src/owui_client
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src", "owui_client")

class SymbolCollector(ast.NodeVisitor):
    def __init__(self):
        self.classes: Set[str] = set()
        self.methods: Set[str] = set() # Class.method
        self.functions: Set[str] = set() # Top level functions
        self.current_class = None

    def visit_ClassDef(self, node: ast.ClassDef):
        self.classes.add(node.name)
        prev_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = prev_class

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if self.current_class:
            self.methods.add(f"{self.current_class}.{node.name}")
        else:
            self.functions.add(node.name)
        self.generic_visit(node)
        
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.visit_FunctionDef(node)

def get_all_symbols() -> SymbolCollector:
    collector = SymbolCollector()
    if not os.path.exists(SRC_ROOT):
        # Fallback or error if path is wrong
        print(f"Warning: Source root not found at {SRC_ROOT}")
        return collector
        
    for root, _, files in os.walk(SRC_ROOT):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    try:
                        tree = ast.parse(f.read(), filename=path)
                        collector.visit(tree)
                    except Exception as e:
                        print(f"Failed to parse {path}: {e}")
    return collector

def find_docstrings(node: ast.AST) -> Generator[Tuple[str, str, int], None, None]:
    """Generator that yields (docstring, node_name, lineno)"""
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
        doc = ast.get_docstring(node)
        if doc:
            name = getattr(node, "name", "module")
            # If it's a method, we might want context, but for now simple name is ok for reporting
            yield (doc, name, getattr(node, "lineno", 0))
    
    for child in ast.iter_child_nodes(node):
        yield from find_docstrings(child)

def test_docstring_missing_backticks():
    """
    Scans all docstrings in the codebase for references to known Classes, 
    Methods (Class.method), or Functions that are NOT backticked.
    """
    collector = get_all_symbols()
    
    # Define targets to look for
    # We focus on:
    # 1. Class names (e.g. AuthsClient)
    # 2. Fully qualified methods (e.g. AuthsClient.get_session)
    # 3. Top level functions (e.g. verify_token) - filtering out common words
    
    targets = collector.classes.union(collector.methods)
    
    # Add top level functions if they are not generic words
    # A simple heuristic: ignore if length < 4 or is common verb
    common_verbs = {"get", "set", "list", "create", "update", "delete", "run", "call", "main"}
    for fn in collector.functions:
        if fn not in common_verbs and len(fn) > 3:
            targets.add(fn)

    errors = []
    
    for root, _, files in os.walk(SRC_ROOT):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, PROJECT_ROOT)
                
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    try:
                        tree = ast.parse(content, filename=path)
                    except:
                        continue
                        
                    for doc, name, line in find_docstrings(tree):
                        # Find all words/tokens in doc that match a known target
                        
                        # Optimization: Extract potential candidates from doc first
                        # We look for word sequences that look like our targets.
                        # Symbols are either "Word" or "Word.word" or "word_word"
                        
                        # Regex to catch:
                        # - Words: \b\w+\b
                        # - Dotted words: \b\w+\.\w+\b
                        
                        candidates = set(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_.]*\b', doc))
                        
                        # Filter candidates that are actually in our targets
                        found_targets = candidates.intersection(targets)
                        
                        for ref in found_targets:
                            # Verify context (missing backticks)
                            escaped_ref = re.escape(ref)
                            
                            # Pattern: Not preceded by `, not followed by `
                            # Also check we are not inside a link [Ref](...)
                            # But regex lookaround is limited for variable length.
                            
                            # We iterate matches to check context
                            pattern = r'(?<!`)\b' + escaped_ref + r'\b(?!`)'
                            
                            for m in re.finditer(pattern, doc):
                                start, end = m.span()
                                
                                # Check for Markdown Link [Ref](...)
                                # Look backwards for '[' and forwards for ']'
                                # Simple check: if immediate surrounding is [...]
                                
                                # Also check if it's "See [Ref]" or similar
                                # A simplified check: scan 1 char before/after
                                
                                pre = doc[start-1] if start > 0 else ""
                                post = doc[end] if end < len(doc) else ""
                                
                                if pre == '[' and post == ']':
                                    continue # It's linked like [Ref]
                                
                                # Exclusion: "OpenWebUI" - name of the project often used in text
                                if ref == "OpenWebUI":
                                    continue
                                    
                                # Report error
                                errors.append(f"{rel_path}:{line} - Missing backticks for reference '{ref}' in docstring of '{name}'")

    if errors:
        # Sort errors for readability
        errors.sort()
        pytest.fail(f"Found {len(errors)} documentation link issues:\n" + "\n".join(errors))

if __name__ == "__main__":
    # Allow running directly
    try:
        test_docstring_missing_backticks()
        print("No issues found.")
    except Exception as e:
        print(e)

