import time
from types import SimpleNamespace

import pytest
from httpx import HTTPStatusError, Request

from owui_client.models.skills import SkillForm, SkillMeta, SkillModel
from owui_client.shortcuts import Shortcuts, SkillSyncResult, _is_id_taken


async def test_shortcuts_initialization(client):
    """
    Test that the shortcuts layer is correctly initialized on the client.
    """
    assert hasattr(client, "shortcuts")
    assert isinstance(client.shortcuts, Shortcuts)
    # Ensure the shortcuts instance has a reference back to the client
    assert client.shortcuts.client == client


async def test_shortcut_sync_skill(client, tmp_path):
    """
    Test the full create / unchanged / updated lifecycle of sync_skill.
    """
    # Timestamp-suffixed id avoids collisions with skills left behind by prior
    # (possibly crashed) runs, which would otherwise flip "created" -> "unchanged".
    uid = int(time.time())
    name = f"Sync Test Skill {uid}"
    expected_id = f"sync-test-skill-{uid}"

    skill_path = tmp_path / "summarizer.md"
    skill_path.write_text(
        f"---\nname: {name}\ndescription: Summarizes text.\n---\n\nYou summarize input text.\n",
        encoding="utf-8",
    )

    try:
        # 1. First sync -> created.
        created = await client.shortcuts.sync_skill(skill_path)
        assert isinstance(created, SkillSyncResult)
        assert created.action == "created"
        assert created.id == expected_id
        assert created.name == name

        # 2. Second sync (identical) -> unchanged, no API write.
        unchanged = await client.shortcuts.sync_skill(skill_path)
        assert unchanged.action == "unchanged"
        assert unchanged.id == created.id

        # 3. Edit the file content -> updated.
        skill_path.write_text(
            f"---\nname: {name}\ndescription: Summarizes text.\n---\n\nYou summarize input text very concisely.\n",
            encoding="utf-8",
        )
        updated = await client.shortcuts.sync_skill(skill_path)
        assert updated.action == "updated"
        assert updated.id == created.id
    finally:
        # Clean up the created skill regardless of outcome.
        try:
            await client.skills.delete_skill_by_id(expected_id)
        except Exception:
            pass


async def test_shortcut_sync_skills(client, tmp_path):
    """Directory sync: nested new skill -> created, pre-seeded -> unchanged, README -> skipped."""
    uid = int(time.time())
    new_name = f"Dir New Skill {uid}"
    new_id = f"dir-new-skill-{uid}"
    seed_name = f"Dir Seed Skill {uid}"
    seed_id = f"dir-seed-skill-{uid}"

    # Nested new skill file (lives in its own subdir).
    (tmp_path / "new").mkdir()
    (tmp_path / "new" / "SKILL.md").write_text(
        f"---\nname: {new_name}\ndescription: a new nested skill.\n---\n\nNew body.\n",
        encoding="utf-8",
    )
    # Seeded skill file: pre-created on the server, then re-synced unchanged.
    seed_body = f"---\nname: {seed_name}\ndescription: a seeded skill.\n---\n\nSeed body.\n"
    (tmp_path / "seed.md").write_text(seed_body, encoding="utf-8")
    # A non-skill markdown file.
    (tmp_path / "README.md").write_text("# Readme\n\nNot a skill.\n", encoding="utf-8")

    try:
        # Pre-create the seeded skill so the first dir sync sees it as unchanged.
        await client.skills.create_new_skill(
            SkillForm(
                id=seed_id,
                name=seed_name,
                description="a seeded skill.",
                content=seed_body,
                meta=SkillMeta(tags=[]),
                is_active=True,
            )
        )

        results = await client.shortcuts.sync_skills(tmp_path)
        by_action: dict[str, list[SkillSyncResult]] = {}
        for r in results:
            by_action.setdefault(r.action, []).append(r)

        # Nested new skill -> created.
        assert any(r.id == new_id and r.name == new_name for r in by_action.get("created", []))
        # Pre-seeded skill -> unchanged (no write).
        assert any(r.id == seed_id for r in by_action.get("unchanged", []))
        # README -> skipped.
        skipped = by_action.get("skipped", [])
        assert len(skipped) == 1
        assert skipped[0].path.endswith("README.md")
        assert skipped[0].error is not None
        # No failures.
        assert by_action.get("failed", []) == []

        # Re-run: nothing newly created; seeded still unchanged.
        results2 = await client.shortcuts.sync_skills(tmp_path)
        by_action2: dict[str, list[SkillSyncResult]] = {}
        for r in results2:
            by_action2.setdefault(r.action, []).append(r)
        assert by_action2.get("created", []) == []
        assert any(r.id == seed_id for r in by_action2.get("unchanged", []))
    finally:
        for sid in (new_id, seed_id):
            try:
                await client.skills.delete_skill_by_id(sid)
            except Exception:
                pass


# ---------------------------------------------------------------------------
# No-Docker unit tests for the reconcile logic and the ID_TAKEN heuristic.
# These use a fake client so they exercise the trickiest paths deterministically
# without spinning up the Open WebUI container.
# ---------------------------------------------------------------------------


def _make_skill(
    id: str,
    name: str,
    *,
    content: str = "content",
    description: str = "description",
    is_active: bool = True,
) -> SkillModel:
    return SkillModel(
        id=id,
        user_id="user-id",
        name=name,
        description=description,
        content=content,
        meta=SkillMeta(tags=[]),
        is_active=is_active,
        access_grants=[],
        updated_at=0,
        created_at=0,
    )


def _http_error(status_code: int, text: str = "") -> HTTPStatusError:
    request = Request("POST", "http://localhost/api/v1/skills/create")
    response = SimpleNamespace(status_code=status_code, text=text)
    return HTTPStatusError("error", request=request, response=response)


class _FakeSkills:
    def __init__(self, existing=None, create_exc=None, update_exc=None):
        self.existing = existing or []
        self.create_exc = create_exc
        self.update_exc = update_exc
        self.created: list[SkillForm] = []
        self.updated: list[tuple[str, SkillForm]] = []

    async def export_skills(self):
        return list(self.existing)

    async def create_new_skill(self, form):
        if self.create_exc:
            raise self.create_exc
        self.created.append(form)
        return None

    async def update_skill_by_id(self, id, form):
        if self.update_exc:
            raise self.update_exc
        self.updated.append((id, form))
        return None


def _shortcuts(existing=None, create_exc=None, update_exc=None):
    fake = _FakeSkills(existing, create_exc, update_exc)
    return Shortcuts(SimpleNamespace(skills=fake)), fake


def _write_skill(tmp_path, name="Summarizer", description="d", body="content", filename="s.md"):
    path = tmp_path / filename
    path.write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n{body}\n", encoding="utf-8"
    )
    return path


def test_is_id_taken_matches_id_taken():
    assert _is_id_taken(_http_error(400, '{"detail":"ID_TAKEN"}')) is True


def test_is_id_taken_matches_already_registered():
    assert _is_id_taken(_http_error(400, "Uh-oh! This id is already registered.")) is True


def test_is_id_taken_rejects_other_400():
    assert _is_id_taken(_http_error(400, '{"detail":"some other problem"}')) is False


def test_is_id_taken_rejects_non_400():
    assert _is_id_taken(_http_error(500, "ID_TAKEN")) is False


async def test_sync_skill_creates_when_absent(tmp_path):
    path = _write_skill(tmp_path)
    sc, fake = _shortcuts(existing=[])
    result = await sc.sync_skill(path)
    assert result.action == "created"
    assert result.id == "summarizer"
    assert len(fake.created) == 1
    assert fake.updated == []


async def test_sync_skill_unchanged_makes_no_write(tmp_path):
    path = _write_skill(tmp_path)
    existing = [_make_skill("summarizer", "Summarizer", content=path.read_text(), description="d")]
    sc, fake = _shortcuts(existing=existing)
    result = await sc.sync_skill(path)
    assert result.action == "unchanged"
    assert fake.created == [] and fake.updated == []


async def test_sync_skill_update_preserves_is_active(tmp_path):
    path = _write_skill(tmp_path, body="new body")
    existing = [_make_skill("summarizer", "Summarizer", content="old", description="d", is_active=False)]
    sc, fake = _shortcuts(existing=existing)
    result = await sc.sync_skill(path)
    assert result.action == "updated"
    assert len(fake.updated) == 1
    updated_id, updated_form = fake.updated[0]
    assert updated_id == "summarizer"
    # is_active must be preserved, not forced back to True by the update.
    assert updated_form.is_active is False


async def test_sync_skill_id_taken_falls_back_to_update(tmp_path):
    path = _write_skill(tmp_path)
    sc, fake = _shortcuts(existing=[], create_exc=_http_error(400, "ID_TAKEN"))
    result = await sc.sync_skill(path)
    assert result.action == "created"
    assert fake.created == []
    assert len(fake.updated) == 1


async def test_sync_skill_re_raises_non_id_taken_error(tmp_path):
    path = _write_skill(tmp_path)
    sc, _ = _shortcuts(existing=[], create_exc=_http_error(500, "boom"))
    with pytest.raises(HTTPStatusError):
        await sc.sync_skill(path)


async def test_sync_skills_records_failed_and_continues(tmp_path):
    (tmp_path / "new").mkdir()
    _write_skill(tmp_path / "new", name="New One", body="x", filename="SKILL.md")
    (tmp_path / "other").mkdir()
    _write_skill(tmp_path / "other", name="Other One", body="y", filename="SKILL.md")

    existing = [_make_skill("other-one", "Other One", content="stale", description="d")]
    sc, _ = _shortcuts(existing=existing, update_exc=_http_error(500, "boom"))
    results = await sc.sync_skills(tmp_path)

    by_action = {}
    for r in results:
        by_action.setdefault(r.action, []).append(r)
    assert set(by_action) == {"created", "failed"}
    assert len(by_action["created"]) == 1
    assert len(by_action["failed"]) == 1
    assert by_action["failed"][0].id == "other-one"


