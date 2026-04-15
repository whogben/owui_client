import json
import re
import tomllib
from pathlib import Path


PROJECT_ROOT = Path(__file__).parents[1]
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
REFS_PACKAGE_JSON_PATH = PROJECT_ROOT / "refs/owui_source_main/package.json"
README_PATH = PROJECT_ROOT / "README.md"
CHANGELOG_PATH = PROJECT_ROOT / "CHANGELOG.md"

SEMVER_RE = re.compile(r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$")


def _parse_semver(version: str) -> tuple[int, int, int]:
    match = SEMVER_RE.match(version.strip())
    if not match:
        raise ValueError(f"Invalid semantic version '{version}'. Expected X.Y.Z format.")
    return int(match.group("major")), int(match.group("minor")), int(match.group("patch"))


def read_client_version_from_pyproject() -> str:
    data = tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))
    version = data.get("project", {}).get("version")
    if not isinstance(version, str) or not version:
        raise ValueError("Could not read [project].version from pyproject.toml.")
    _parse_semver(version)
    return version


def read_runtime_client_version() -> str:
    from owui_client import __version__

    _parse_semver(__version__)
    return __version__


def derive_target_owui_version(client_version: str) -> str:
    major, minor, _patch = _parse_semver(client_version)
    return f"0.{major}.{minor}"


def read_refs_owui_version() -> str:
    package_data = json.loads(REFS_PACKAGE_JSON_PATH.read_text(encoding="utf-8"))
    version = package_data.get("version")
    if not isinstance(version, str) or not version:
        raise ValueError("Could not read version from refs/owui_source_main/package.json.")
    # Upstream may prefix tags/versions with 'v' in some contexts.
    normalized = version[1:] if version.startswith("v") else version
    _parse_semver(normalized)
    return normalized


def read_readme_text() -> str:
    return README_PATH.read_text(encoding="utf-8")


def read_changelog_text() -> str:
    return CHANGELOG_PATH.read_text(encoding="utf-8")
