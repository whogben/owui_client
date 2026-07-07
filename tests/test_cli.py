"""Tests for owui_client.cli (no Docker, no network).

These exercise Cyclopts' argument/env-var parsing and help output without ever
constructing an `OpenWebUI` client or making a network call.
"""

import subprocess
import sys
from pathlib import Path

import pytest

from owui_client.cli import _format_skill_result_line, app, sync_skill, sync_skills
from owui_client.shortcuts import SkillSyncResult


def test_sync_skill_command_is_registered():
    # app["sync-skill"] retrieves the registered command sub-app (KeyError if absent).
    cmd = app["sync-skill"]
    assert cmd.default_command is sync_skill


def test_help_mentions_sync_skill():
    result = subprocess.run(
        [sys.executable, "-m", "owui_client.cli", "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    combined = result.stdout + result.stderr
    assert "sync-skill" in combined


def test_parse_args_yields_expected_path(tmp_path, monkeypatch):
    monkeypatch.delenv("OWUI_SERVER", raising=False)
    monkeypatch.delenv("OWUI_API_KEY", raising=False)

    target = tmp_path / "my-skill.md"
    target.write_text("---\nname: X\ndescription: Y\n---\n", encoding="utf-8")

    fn, bound, _ = app.parse_args(["sync-skill", str(target)])

    assert fn is sync_skill
    assert bound.arguments["path"] == Path(str(target))
    # With no env and no flag, server/api_key fall back to their declared
    # defaults, so Cyclopts does not surface them in bound.arguments.
    assert "server" not in bound.arguments
    assert "api_key" not in bound.arguments


def test_parse_args_reads_env_vars(tmp_path, monkeypatch):
    monkeypatch.setenv("OWUI_SERVER", "http://envhost:9090/api")
    monkeypatch.setenv("OWUI_API_KEY", "env-key")

    target = tmp_path / "my-skill.md"
    target.write_text("---\nname: X\ndescription: Y\n---\n", encoding="utf-8")

    _, bound, _ = app.parse_args(["sync-skill", str(target)])

    assert bound.arguments["server"] == "http://envhost:9090/api"
    assert bound.arguments["api_key"] == "env-key"


def test_parse_args_explicit_flags_override_env(tmp_path, monkeypatch):
    monkeypatch.setenv("OWUI_API_KEY", "env-key")

    target = tmp_path / "my-skill.md"
    target.write_text("---\nname: X\ndescription: Y\n---\n", encoding="utf-8")

    _, bound, _ = app.parse_args(
        ["sync-skill", str(target), "--server", "http://explicit/api", "--api-key", "explicit-key"]
    )

    assert bound.arguments["server"] == "http://explicit/api"
    assert bound.arguments["api_key"] == "explicit-key"


# --- sync-skills ---


def test_sync_skills_command_is_registered():
    cmd = app["sync-skills"]
    assert cmd.default_command is sync_skills


def test_help_mentions_sync_skills():
    result = subprocess.run(
        [sys.executable, "-m", "owui_client.cli", "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    combined = result.stdout + result.stderr
    assert "sync-skills" in combined


def test_sync_skills_help_mentions_directory_argument():
    result = subprocess.run(
        [sys.executable, "-m", "owui_client.cli", "sync-skills", "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr


def test_sync_skills_parses_directory_argument(tmp_path, monkeypatch):
    monkeypatch.delenv("OWUI_SERVER", raising=False)
    monkeypatch.delenv("OWUI_API_KEY", raising=False)

    d = tmp_path / "skills"
    d.mkdir()

    fn, bound, _ = app.parse_args(["sync-skills", str(d)])

    assert fn is sync_skills
    assert bound.arguments["dir_path"] == Path(str(d))
    assert "server" not in bound.arguments
    assert "api_key" not in bound.arguments


def test_sync_skills_reads_env_vars(tmp_path, monkeypatch):
    monkeypatch.setenv("OWUI_SERVER", "http://envhost:9090/api")
    monkeypatch.setenv("OWUI_API_KEY", "env-key")

    d = tmp_path / "skills"
    d.mkdir()

    _, bound, _ = app.parse_args(["sync-skills", str(d)])

    assert bound.arguments["server"] == "http://envhost:9090/api"
    assert bound.arguments["api_key"] == "env-key"


# --- output formatter ---


def test_format_line_created():
    r = SkillSyncResult(action="created", name="Sum", id="sum", path="s.md")
    assert _format_skill_result_line(r) == "created: Sum (sum) s.md"


def test_format_line_skipped_with_error():
    r = SkillSyncResult(action="skipped", path="README.md", error="no frontmatter")
    assert _format_skill_result_line(r) == "skipped: README.md [no frontmatter]"
