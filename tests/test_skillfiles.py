"""Unit tests for owui_client.skillfiles (pure, no network)."""

from pathlib import Path

import pytest

from owui_client.skillfiles import (
    DiscoveredSkillFile,
    InvalidSkillFileError,
    discover_skill_files,
    normalize_skill_id,
    parse_skill_file,
)


def _write(tmp_path: Path, body: str, name: str = "skill.md") -> Path:
    path = tmp_path / name
    path.write_text(body, encoding="utf-8")
    return path


def test_valid_frontmatter_parses(tmp_path):
    path = _write(
        tmp_path,
        "---\nname: Summarizer\ndescription: Summarizes text concisely.\n---\n\nYou summarize input text.\n",
    )
    parsed = parse_skill_file(path)

    assert parsed.name == "Summarizer"
    assert parsed.description == "Summarizes text concisely."
    assert parsed.id == "summarizer"


def test_id_normalization():
    assert normalize_skill_id("My Cool Skill") == "my-cool-skill"
    assert normalize_skill_id("Summarizer") == "summarizer"


def test_content_includes_frontmatter(tmp_path):
    body = "---\nname: Summarizer\ndescription: Summarizes text.\n---\n\nBody here.\n"
    path = _write(tmp_path, body)
    parsed = parse_skill_file(path)

    # Full file text (frontmatter fences included) becomes the content.
    assert parsed.content == body
    assert parsed.content.startswith("---\n")
    assert "Body here." in parsed.content


def test_missing_name_raises(tmp_path):
    path = _write(tmp_path, "---\ndescription: A skill with no name.\n---\nbody\n")
    with pytest.raises(InvalidSkillFileError):
        parse_skill_file(path)


def test_empty_name_raises(tmp_path):
    path = _write(tmp_path, "---\nname: ' '\ndescription: A skill.\n---\nbody\n")
    with pytest.raises(InvalidSkillFileError):
        parse_skill_file(path)


def test_missing_description_raises(tmp_path):
    path = _write(tmp_path, "---\nname: Skill\n---\nbody\n")
    with pytest.raises(InvalidSkillFileError):
        parse_skill_file(path)


def test_empty_description_raises(tmp_path):
    path = _write(tmp_path, "---\nname: Skill\ndescription: ''\n---\nbody\n")
    with pytest.raises(InvalidSkillFileError):
        parse_skill_file(path)


def test_no_frontmatter_raises(tmp_path):
    path = _write(tmp_path, "# Just a markdown file\n\nNo frontmatter here.\n")
    with pytest.raises(InvalidSkillFileError):
        parse_skill_file(path)


def test_unparseable_yaml_raises(tmp_path):
    path = _write(tmp_path, "---\nname: Skill\n: : : bad yaml\n---\nbody\n")
    with pytest.raises(InvalidSkillFileError):
        parse_skill_file(path)


def test_extra_frontmatter_keys_are_ignored(tmp_path):
    path = _write(
        tmp_path,
        "---\nname: Skill\ndescription: A skill.\ntags: [a, b]\nauthor: someone\n---\nbody\n",
    )
    parsed = parse_skill_file(path)
    assert parsed.name == "Skill"
    assert parsed.description == "A skill."


def test_unclosed_frontmatter_fence_raises(tmp_path):
    path = _write(tmp_path, "---\nname: Skill\ndescription: A skill.\nbody with no closing fence\n")
    with pytest.raises(InvalidSkillFileError):
        parse_skill_file(path)


def test_non_mapping_frontmatter_raises(tmp_path):
    # A YAML list (not a mapping) is not valid skill frontmatter.
    path = _write(tmp_path, "---\n- item one\n- item two\n---\nbody\n")
    with pytest.raises(InvalidSkillFileError):
        parse_skill_file(path)


# --- discover_skill_files ---


def _write_rel(tmp_path: Path, rel: str, body: str) -> Path:
    """Write a file at a relative (possibly nested) path under tmp_path."""
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_discover_recursive_finds_nested_skills(tmp_path):
    _write_rel(tmp_path, "top.md", "---\nname: Top\ndescription: top.\n---\nbody\n")
    _write_rel(tmp_path, "a/b/SKILL.md", "---\nname: Nested\ndescription: nested.\n---\nbody\n")
    _write_rel(tmp_path, "a/b/c/deep.md", "---\nname: Deep\ndescription: deep.\n---\nbody\n")

    discovered = discover_skill_files(tmp_path)

    syncable = [d for d in discovered if d.parsed is not None]
    assert {d.parsed.name for d in syncable} == {"Top", "Nested", "Deep"}
    assert len(syncable) == 3
    # Output is sorted by path.
    paths = [d.path for d in discovered]
    assert paths == sorted(paths)
    # Invariant: parsed is None iff skip_reason is not None.
    for d in discovered:
        assert isinstance(d, DiscoveredSkillFile)
        assert (d.parsed is None) == (d.skip_reason is not None)


def test_discover_parses_a_valid_skill(tmp_path):
    _write_rel(tmp_path, "x.md", "---\nname: MySkill\ndescription: a skill.\n---\nbody\n")

    discovered = discover_skill_files(tmp_path)

    assert len(discovered) == 1
    assert discovered[0].parsed is not None
    assert discovered[0].parsed.name == "MySkill"
    assert discovered[0].parsed.id == "myskill"
    assert discovered[0].skip_reason is None


def test_discover_skips_non_skill_markdown(tmp_path):
    # No frontmatter at all.
    _write_rel(tmp_path, "README.md", "# Readme\n\nJust docs.\n")
    # Frontmatter present but missing description.
    _write_rel(tmp_path, "nodesc.md", "---\nname: NoDesc\n---\nbody\n")
    # A valid skill alongside.
    _write_rel(tmp_path, "ok.md", "---\nname: Ok\ndescription: ok.\n---\nbody\n")

    discovered = discover_skill_files(tmp_path)
    by_name = {d.path.name: d for d in discovered}

    assert by_name["ok.md"].parsed is not None
    assert by_name["ok.md"].skip_reason is None

    assert by_name["README.md"].parsed is None
    assert by_name["README.md"].skip_reason is not None

    assert by_name["nodesc.md"].parsed is None
    assert by_name["nodesc.md"].skip_reason is not None


def test_discover_marks_all_duplicate_ids_skipped(tmp_path):
    # Two distinct files that normalize to the same id "dup".
    _write_rel(tmp_path, "one.md", "---\nname: Dup\ndescription: first.\n---\nbody\n")
    _write_rel(tmp_path, "two.md", "---\nname: Dup\ndescription: second.\n---\nbody\n")

    discovered = discover_skill_files(tmp_path)

    assert len(discovered) == 2
    for d in discovered:
        assert d.parsed is None
        assert d.skip_reason is not None
        assert "duplicate" in d.skip_reason
        assert "dup" in d.skip_reason  # the normalized id
    # Each reason names the *other* file.
    reasons = {d.path.name: d.skip_reason for d in discovered}
    assert "one.md" in reasons["two.md"]
    assert "two.md" in reasons["one.md"]


def test_discover_output_sorted_by_path(tmp_path):
    _write_rel(tmp_path, "z.md", "---\nname: Z\ndescription: z.\n---\nbody\n")
    _write_rel(tmp_path, "a.md", "---\nname: A\ndescription: a.\n---\nbody\n")
    _write_rel(tmp_path, "m.md", "---\nname: M\ndescription: m.\n---\nbody\n")

    discovered = discover_skill_files(tmp_path)

    assert [d.path.name for d in discovered] == ["a.md", "m.md", "z.md"]


def test_discover_missing_dir_raises(tmp_path):
    with pytest.raises(InvalidSkillFileError):
        discover_skill_files(tmp_path / "does-not-exist")


def test_discover_path_is_not_dir_raises(tmp_path):
    f = tmp_path / "notadir.md"
    f.write_text("hi", encoding="utf-8")
    with pytest.raises(InvalidSkillFileError):
        discover_skill_files(f)
