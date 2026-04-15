"""Tests for the Skills endpoints."""

import pytest
import time
from httpx import HTTPStatusError
from owui_client.models.skills import SkillForm, SkillMeta

pytestmark = pytest.mark.asyncio


async def test_get_skills(client):
    """Test retrieving all skills for the current user."""
    result = await client.skills.get_skills()
    assert result is not None
    assert isinstance(result, list)


async def test_get_skill_list(client):
    """Test retrieving paginated skill list with access info."""
    result = await client.skills.get_skill_list()
    assert result is not None
    assert hasattr(result, "items")
    assert hasattr(result, "total")
    assert isinstance(result.items, list)


async def test_export_skills(client):
    """Test exporting all skills."""
    result = await client.skills.export_skills()
    assert result is not None
    assert isinstance(result, list)


async def test_create_skill(client):
    """Test creating a new skill."""
    skill_id = f"test_skill_{int(time.time())}"
    form_data = SkillForm(
        id=skill_id,
        name="Test Skill",
        content="This is a test skill.",
        meta=SkillMeta(tags=["test"]),
    )

    created = await client.skills.create_skill(form_data)
    assert created is not None
    assert created.id == skill_id
    assert created.name == "Test Skill"

    await client.skills.delete_skill_by_id(skill_id)


async def test_get_skill_by_id(client):
    """Test retrieving a skill by ID."""
    skill_id = f"test_getbyid_{int(time.time())}"
    form_data = SkillForm(
        id=skill_id,
        name="Get By ID Skill",
        content="Content for get by id test.",
    )

    created = await client.skills.create_skill(form_data)
    assert created is not None

    try:
        fetched = await client.skills.get_skill_by_id(skill_id)
        assert fetched is not None
        assert fetched.id == skill_id
        assert fetched.name == "Get By ID Skill"
        assert hasattr(fetched, "write_access")
    finally:
        await client.skills.delete_skill_by_id(skill_id)


async def test_update_skill_by_id(client):
    """Test updating a skill by ID."""
    skill_id = f"test_update_{int(time.time())}"
    form_data = SkillForm(
        id=skill_id,
        name="Original Name",
        content="Original content.",
    )

    created = await client.skills.create_skill(form_data)
    assert created is not None

    try:
        updated_form = SkillForm(
            id=skill_id,
            name="Updated Name",
            content="Updated content.",
        )
        updated = await client.skills.update_skill_by_id(skill_id, updated_form)
        assert updated is not None
        assert updated.name == "Updated Name"
        assert updated.content == "Updated content."
    finally:
        await client.skills.delete_skill_by_id(skill_id)


async def test_update_skill_access_by_id(client):
    """Test updating skill access grants."""
    skill_id = f"test_access_{int(time.time())}"
    form_data = SkillForm(
        id=skill_id,
        name="Access Test Skill",
        content="Content for access test.",
    )

    created = await client.skills.create_skill(form_data)
    assert created is not None

    try:
        access_grants = [
            {
                "principal_type": "user",
                "principal_id": "*",
                "permission": "read",
            }
        ]
        updated = await client.skills.update_skill_access_by_id(
            skill_id, access_grants
        )
        assert updated is not None
        assert updated.id == skill_id
    finally:
        await client.skills.delete_skill_by_id(skill_id)


async def test_toggle_skill_by_id(client):
    """Test toggling a skill's active status."""
    skill_id = f"test_toggle_{int(time.time())}"
    form_data = SkillForm(
        id=skill_id,
        name="Toggle Test Skill",
        content="Content for toggle test.",
        is_active=True,
    )

    created = await client.skills.create_skill(form_data)
    assert created is not None

    try:
        toggled = await client.skills.toggle_skill_by_id(skill_id)
        assert toggled is not None
        assert toggled.is_active is False
    finally:
        await client.skills.delete_skill_by_id(skill_id)


async def test_delete_skill_by_id(client):
    """Test deleting a skill by ID."""
    skill_id = f"test_delete_{int(time.time())}"
    form_data = SkillForm(
        id=skill_id,
        name="Delete Test Skill",
        content="Content for delete test.",
    )

    created = await client.skills.create_skill(form_data)
    assert created is not None

    deleted = await client.skills.delete_skill_by_id(skill_id)
    assert deleted is True

    try:
        await client.skills.get_skill_by_id(skill_id)
        assert False, "Skill should have been deleted"
    except HTTPStatusError as e:
        assert e.response.status_code == 404
