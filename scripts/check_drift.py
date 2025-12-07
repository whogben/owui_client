import ast
import sys
import re
from pathlib import Path
from typing import Dict, Set, List, Tuple, Any

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
REF_BASE = PROJECT_ROOT / "refs/owui_source_main/backend/open_webui"
CLIENT_BASE = PROJECT_ROOT / "src/owui_client"


class DriftIssue:
    def __init__(self, kind: str, message: str, file: str):
        self.kind = kind
        self.message = message
        self.file = file

    def __repr__(self):
        return f"[{self.kind}] {self.file}: {self.message}"


def extract_string(node: ast.AST) -> str:
    """
    Extracts a string value from an AST node, handling Constants, Strings, and f-strings.
    F-strings are converted to a pattern with {} for expressions.
    """
    if isinstance(node, ast.Constant):
        return str(node.value)
    elif isinstance(node, ast.JoinedStr):
        # Reconstruct f-string but replace expressions with {}
        parts = []
        for value in node.values:
            if isinstance(value, ast.Constant):
                parts.append(extract_string(value))
            else:
                parts.append("{}")
        return "".join(parts)
    return ""


def get_class_details(file_path: Path) -> Dict[str, Dict[str, Any]]:
    """
    Parses a python file and returns a dict of {ClassName: {fields: Set[str], bases: Set[str]}}.
    Parses ALL classes to ensure we catch models defined in routers or elsewhere.
    """
    if not file_path.exists():
        return {}

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return {}

    classes = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            fields = set()
            bases = set()

            # Extract bases
            for base in node.bases:
                if isinstance(base, ast.Name):
                    bases.add(base.id)
                elif isinstance(base, ast.Attribute):
                    bases.add(base.attr)

            # Extract fields
            for item in node.body:
                if isinstance(item, ast.AnnAssign):
                    if isinstance(item.target, ast.Name):
                        fields.add(item.target.id)
            
            classes[node.name] = {"fields": fields, "bases": bases}

    return classes


def get_router_endpoints(file_path: Path) -> List[Tuple[str, str]]:
    """
    Parses a router file and returns list of (method, path) tuples.
    """
    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except Exception:
            return []

    endpoints = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call):
                    func = decorator.func
                    if (
                        isinstance(func, ast.Attribute)
                        and isinstance(func.value, ast.Name)
                        and func.value.id == "router"
                    ):
                        method = func.attr.upper()
                        path = "/"
                        if decorator.args:
                            path = extract_string(decorator.args[0])

                        endpoints.append((method, path))
    return endpoints


def get_client_requests(file_path: Path) -> List[Tuple[str, str]]:
    """
    Parses a client file and returns list of (method, url) called in _request.
    """
    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except Exception:
            return []

    requests = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            is_request = False
            if isinstance(node.func, ast.Attribute) and node.func.attr == "_request":
                is_request = True

            if is_request:
                method = None
                url_node = None

                # Extract args
                if len(node.args) >= 1:
                    method = extract_string(node.args[0])
                if len(node.args) >= 2:
                    url_node = node.args[1]

                # Check keywords
                for kw in node.keywords:
                    if kw.arg == "method":
                        method = extract_string(kw.value)
                    if kw.arg == "url":
                        url_node = kw.value

                if method is not None and url_node:
                    url_str = ""

                    # Handle self._get_url(...)
                    if (
                        isinstance(url_node, ast.Call)
                        and isinstance(url_node.func, ast.Attribute)
                        and url_node.func.attr == "_get_url"
                        and url_node.args
                    ):
                        # Extract the argument to _get_url
                        url_str = extract_string(url_node.args[0])
                    else:
                        # Direct string or f-string
                        url_str = extract_string(url_node)

                    if url_str:
                        requests.append((method.upper(), url_str))
    return requests


def normalize_path(path: str) -> str:
    """
    Normalizes a path for comparison by replacing {param} with {}.
    """
    return re.sub(r"\{[^}]+\}", "{}", path)


def heuristic_search(file_content: str, path: str) -> bool:
    """
    Searches for the path in the file content string (ignoring leading slash and params).
    Used as a fallback for dynamic URL construction.
    """
    # Remove leading slash
    clean_path = path.lstrip("/")

    # If path is empty (root), return False (too ambiguous)
    if not clean_path:
        return False

    # Remove params {id}
    clean_path = re.sub(r"\{[^}]+\}", "", clean_path)

    # Remove trailing slash
    clean_path = clean_path.rstrip("/")

    # If path became empty or too short, skip heuristic
    if len(clean_path) < 3:
        return False

    # Simple substring search
    return clean_path in file_content


def find_drift(ignore_files: List[str] = None) -> List[DriftIssue]:
    if ignore_files is None:
        ignore_files = []

    issues = []

    # 1. Check Models
    ref_models_dir = REF_BASE / "models"
    ref_routers_dir = REF_BASE / "routers"
    client_models_dir = CLIENT_BASE / "models"

    if not ref_models_dir.exists():
        issues.append(
            DriftIssue(
                "ERROR",
                f"Reference models directory not found at {ref_models_dir}",
                "general",
            )
        )
        return issues

    # Drive check from Client Models (what we have implemented)
    for client_file in client_models_dir.glob("*.py"):
        if client_file.name == "__init__.py":
            continue
        if client_file.name in ignore_files:
            continue

        ref_model_file = ref_models_dir / client_file.name
        ref_router_file = ref_routers_dir / client_file.name
        
        # Get details from client
        client_classes = get_class_details(client_file)
        
        # Build reference classes map by combining Model and Router files
        ref_classes = {}
        if ref_model_file.exists():
            ref_classes.update(get_class_details(ref_model_file))
        if ref_router_file.exists():
            # Router definitions take precedence or augment if they exist in both (unlikely)
            ref_classes.update(get_class_details(ref_router_file))

        for cls_name, client_details in client_classes.items():
            if cls_name in ref_classes:
                ref_details = ref_classes[cls_name]
                
                # Check for Missing Fields
                missing_fields = ref_details['fields'] - client_details['fields']
                if missing_fields:
                    issues.append(
                        DriftIssue(
                            "MISSING_FIELDS",
                            f"Model {cls_name} missing fields: {', '.join(missing_fields)}",
                            client_file.name,
                        )
                    )
                
                # Check for Missing Bases
                # We filter out common bases that aren't relevant for drift like 'BaseModel'
                ignored_bases = {'BaseModel', 'object'}
                missing_bases = ref_details['bases'] - client_details['bases'] - ignored_bases
                
                if missing_bases:
                     issues.append(
                        DriftIssue(
                            "MISSING_BASE",
                            f"Model {cls_name} missing base classes: {', '.join(missing_bases)}",
                            client_file.name,
                        )
                    )

    # 2. Check Routers
    client_routers_dir = CLIENT_BASE / "routers"

    for ref_file in ref_routers_dir.glob("*.py"):
        if ref_file.name == "__init__.py":
            continue
        if ref_file.name in ignore_files:
            continue

        client_file = client_routers_dir / ref_file.name

        ref_endpoints = get_router_endpoints(ref_file)
        if not ref_endpoints:
            continue

        if not client_file.exists():
            # Skip completely unimplemented routers
            continue

        client_requests = get_client_requests(client_file)
        client_content = client_file.read_text(encoding="utf-8")

        for method, path in ref_endpoints:
            # Normalize Ref Path: /{id}/valves -> / {} / valves
            norm_ref_path = normalize_path(path)

            found = False

            # 1. Exact/Pattern match in requests
            for c_method, c_url in client_requests:
                if c_method == method:
                    norm_client_url = normalize_path(c_url)

                    # Check if client url ends with the normalized ref path
                    if norm_ref_path == "/" or norm_ref_path == "":
                        # Special case for root
                        if norm_client_url.endswith(
                            f"/{ref_file.stem}/"
                        ) or norm_client_url.endswith(f"/{ref_file.stem}"):
                            found = True
                    elif norm_client_url.endswith(norm_ref_path):
                        found = True

            # 2. Heuristic fallback (search for path string in file)
            if not found:
                if heuristic_search(client_content, path):
                    found = True

            # 3. Special case for API_ROUTE (backend uses @router.api_route, client often uses dynamic method in _request)
            if not found and method == "API_ROUTE":
                # If we have a client request with dynamic method (empty string) and matching URL, assume it's the one.
                for c_method, c_url in client_requests:
                     if c_method == "":
                        norm_client_url = normalize_path(c_url)
                        if norm_ref_path == "/" or norm_ref_path == "":
                             if norm_client_url.endswith(f"/{ref_file.stem}/") or norm_client_url.endswith(f"/{ref_file.stem}"):
                                 found = True
                        elif norm_client_url.endswith(norm_ref_path):
                             found = True

            if not found:
                issues.append(
                    DriftIssue(
                        "MISSING_ENDPOINT",
                        f"Endpoint {method} {path} not called in client",
                        client_file.name,
                    )
                )

    return issues


if __name__ == "__main__":
    print(f"🔍 Checking drift between refs and client...")
    print(f"REF: {REF_BASE}")
    print(f"CLIENT: {CLIENT_BASE}\n")

    issues = find_drift()

    if issues:
        print(f"⚠️  Found {len(issues)} drift issues:")
        for issue in issues:
            print(issue)
        sys.exit(1)
    else:
        print("✅ No drift detected in implemented files.")
        sys.exit(0)
