from versioning import (
    derive_target_owui_version,
    read_changelog_text,
    read_client_version_from_pyproject,
    read_readme_text,
    read_refs_owui_version,
    read_runtime_client_version,
)


def test_package_version_matches_runtime_version():
    pyproject_version = read_client_version_from_pyproject()
    runtime_version = read_runtime_client_version()

    assert pyproject_version == runtime_version, (
        "Version mismatch detected.\n"
        f"- pyproject.toml version: {pyproject_version}\n"
        f"- owui_client.__version__: {runtime_version}\n"
        "Keep these values in sync before release."
    )


def test_refs_source_matches_targeted_owui_version():
    client_version = read_client_version_from_pyproject()
    expected_owui_version = derive_target_owui_version(client_version)
    refs_owui_version = read_refs_owui_version()

    assert refs_owui_version == expected_owui_version, (
        "Reference source version does not match package-derived OWUI target.\n"
        f"- client package version: {client_version}\n"
        f"- expected refs OWUI version (0.client_major.client_minor): {expected_owui_version}\n"
        f"- refs version (refs/owui_source_main/package.json): {refs_owui_version}\n"
        "Update refs checkout to the expected Open WebUI version."
    )


def test_readme_mentions_targeted_owui_version():
    client_version = read_client_version_from_pyproject()
    expected_owui_version = derive_target_owui_version(client_version)
    readme = read_readme_text()

    assert expected_owui_version in readme, (
        "README target version is stale or missing.\n"
        f"- expected Open WebUI target version from package mapping: {expected_owui_version}\n"
        "Update README Target Open WebUI Version section to include the current target."
    )


def test_readme_mentions_client_package_version():
    client_version = read_client_version_from_pyproject()
    readme = read_readme_text()

    assert client_version in readme, (
        "README does not mention the current package version string.\n"
        f"- expected client version from pyproject.toml: {client_version}\n"
        "Update README (e.g. Target Open WebUI Version / examples) to include this version."
    )


def test_changelog_has_heading_for_package_version():
    client_version = read_client_version_from_pyproject()
    changelog = read_changelog_text()
    expected_heading = f"## [{client_version}]"

    assert expected_heading in changelog, (
        "CHANGELOG.md is missing a Keep a Changelog-style section for the current package version.\n"
        f"- expected heading line: {expected_heading!r}\n"
        "Add a dated release section when you bump [project].version in pyproject.toml."
    )
