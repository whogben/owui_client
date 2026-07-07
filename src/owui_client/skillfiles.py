"""Parsing of local skill markdown files into the fields needed by the client.

A skill file is a Markdown document whose leading YAML frontmatter (between
`---` fences) describes the skill. This module is intentionally pure: it has no
client import and performs no network access, so it can be unit-tested trivially.

Frontmatter keys consumed:
- `name` (str, required): display name of the skill.
- `description` (str, required): short description of the skill.

The full file text (frontmatter fences included) becomes the skill `content`,
which is what gets injected into chat context on the server.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import yaml


class InvalidSkillFileError(ValueError):
    """Raised when a skill file cannot be parsed into a valid skill.

    Causes include: no frontmatter block present, YAML that fails to parse, a
    frontmatter block that does not decode to a mapping, or a missing/empty
    `name` or `description` field.
    """


def normalize_skill_id(name: str) -> str:
    """Normalize a skill name into its Open WebUI id.

    Mirrors the backend normalization applied on create: lowercase the name and
    replace spaces with hyphens. For example ``"My Cool Skill"`` becomes
    ``"my-cool-skill"``.

    Args:
        name: The human-readable skill name.

    Returns:
        The normalized id string.
    """
    return name.lower().replace(" ", "-")


@dataclass(frozen=True)
class ParsedSkillFile:
    """A parsed skill file ready to be synced to Open WebUI.

    Attributes:
        name: Display name of the skill (from frontmatter).
        description: Short description of the skill (from frontmatter).
        id: Normalized Open WebUI id derived from `name`.
        content: The complete file text, frontmatter block included. This is the
            text that Open WebUI stores as the skill content and injects into
            chat context when the skill is referenced.
    """

    name: str
    description: str
    id: str
    content: str


def _split_frontmatter(text: str) -> tuple[str, str] | None:
    """Split leading ``---``-delimited frontmatter from the document body.

    Args:
        text: The raw file text.

    Returns:
        A ``(frontmatter_yaml, full_text)`` tuple where ``full_text`` is the
        original text unchanged, or ``None`` if the document has no leading
        frontmatter fence.

    Raises:
        `InvalidSkillFileError`: If the frontmatter block is opened but never
            closed.
    """
    stripped = text.lstrip("\ufeff")  # tolerate a leading BOM
    # Only a fence as the very first non-empty line counts as frontmatter.
    if not stripped.startswith("---"):
        return None

    # First line must be exactly the opening fence.
    first_newline = stripped.find("\n")
    if first_newline == -1:
        return None

    after_first_fence = stripped[first_newline + 1 :]
    # Find the closing fence on its own line.
    lines = after_first_fence.splitlines(keepends=True)
    fm_lines: list[str] = []
    idx = 0
    while idx < len(lines) and lines[idx].strip() != "---":
        fm_lines.append(lines[idx])
        idx += 1
    if idx >= len(lines):
        raise InvalidSkillFileError(
            "Skill file has an opening '---' frontmatter fence with no closing fence."
        )
    return "".join(fm_lines), text


def parse_skill_file(path: str | Path) -> ParsedSkillFile:
    """Parse a local Markdown skill file into name, description, id, and content.

    Args:
        path: Path to a ``.md`` skill file with leading YAML frontmatter.

    Returns:
        `ParsedSkillFile`: The parsed fields (see `ParsedSkillFile`).

    Raises:
        `InvalidSkillFileError`: If the file has no frontmatter, the frontmatter
            is unparseable, or `name`/`description` is missing or empty.
    """
    file_path = Path(path)
    text = file_path.read_text(encoding="utf-8")

    split = _split_frontmatter(text)
    if split is None:
        raise InvalidSkillFileError(
            f"Skill file {file_path} has no leading YAML frontmatter (expected a '---' block)."
        )
    fm_yaml, full_text = split

    try:
        data: Any = yaml.safe_load(fm_yaml)
    except yaml.YAMLError as e:
        raise InvalidSkillFileError(f"Skill file {file_path} has unparseable YAML frontmatter: {e}") from e

    if not isinstance(data, dict):
        raise InvalidSkillFileError(
            f"Skill file {file_path} frontmatter must be a YAML mapping, got {type(data).__name__}."
        )

    name = data.get("name")
    description = data.get("description")

    if not isinstance(name, str) or not name.strip():
        raise InvalidSkillFileError(
            f"Skill file {file_path} is missing a non-empty 'name' in its frontmatter."
        )
    if not isinstance(description, str) or not description.strip():
        raise InvalidSkillFileError(
            f"Skill file {file_path} is missing a non-empty 'description' in its frontmatter."
        )

    return ParsedSkillFile(
        name=name,
        description=description,
        id=normalize_skill_id(name),
        content=full_text,
    )


@dataclass(frozen=True)
class DiscoveredSkillFile:
    """One entry in a directory skill scan, produced by `discover_skill_files`.

    Invariant: a file is syncable iff `parsed` is not None, in which case
    `skip_reason` is None. Otherwise `parsed` is None and `skip_reason` explains
    why the file was not syncable (e.g. not a skill, unparseable frontmatter, or
    a duplicate normalized id).

    Attributes:
        path: Path to the ``.md`` file.
        parsed: The `ParsedSkillFile` if the file is a valid, non-duplicate
            skill; otherwise None.
        skip_reason: Why this file is not syncable, or None when it is.
    """

    path: Path
    parsed: Optional[ParsedSkillFile]
    skip_reason: Optional[str]


def discover_skill_files(dir_path: str | Path) -> list[DiscoveredSkillFile]:
    """Recursively discover and parse every Markdown skill file under a directory.

    Walks `dir_path` at arbitrary depth (skills commonly live in their own
    subdirs), deterministically sorted by path, and parses each ``.md`` file via
    `parse_skill_file`. Files that are not valid skills (no frontmatter,
    unparseable YAML, missing/empty ``name`` or ``description``) are reported
    with a `skip_reason` rather than raising, so one bad file does not abort the
    whole scan.

    After parsing, duplicate normalized ids among the successfully-parsed files
    are detected: any id claimed by more than one file marks ALL of those files
    as skipped (`parsed` set to None) with a reason naming the other files.

    This function is pure and performs no network access.

    Args:
        dir_path: Directory to scan recursively.

    Returns:
        A list of `DiscoveredSkillFile`, sorted by path.

    Raises:
        `InvalidSkillFileError`: If `dir_path` does not exist or is not a
            directory.
    """
    root = Path(dir_path)
    if not root.exists():
        raise InvalidSkillFileError(f"Skill directory {root} does not exist.")
    if not root.is_dir():
        raise InvalidSkillFileError(f"Skill directory {root} is not a directory.")

    discovered: list[DiscoveredSkillFile] = []
    for file_path in sorted(root.rglob("*.md")):
        try:
            parsed = parse_skill_file(file_path)
        except InvalidSkillFileError as e:
            discovered.append(
                DiscoveredSkillFile(path=file_path, parsed=None, skip_reason=str(e))
            )
            continue
        discovered.append(
            DiscoveredSkillFile(path=file_path, parsed=parsed, skip_reason=None)
        )

    # Detect duplicate normalized ids among successfully-parsed files. Any id
    # claimed by more than one file marks ALL of those files as skipped.
    id_to_paths: dict[str, list[Path]] = {}
    for d in discovered:
        if d.parsed is not None:
            id_to_paths.setdefault(d.parsed.id, []).append(d.path)
    duplicate_ids = {id_ for id_, paths in id_to_paths.items() if len(paths) > 1}

    if duplicate_ids:
        resolved: list[DiscoveredSkillFile] = []
        for d in discovered:
            if d.parsed is not None and d.parsed.id in duplicate_ids:
                others = [str(p) for p in id_to_paths[d.parsed.id] if p != d.path]
                reason = (
                    f"duplicate skill name '{d.parsed.name}' (id '{d.parsed.id}') "
                    f"also defined in: {', '.join(others)}"
                )
                resolved.append(
                    DiscoveredSkillFile(path=d.path, parsed=None, skip_reason=reason)
                )
            else:
                resolved.append(d)
        discovered = resolved

    return discovered
