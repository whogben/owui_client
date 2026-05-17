import pytest
import time
from owui_client.models.skills import (
    SkillForm,
    SkillMeta,
    SkillAccessGrantsForm,
)

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio


async def test_skills_client_initialization(client):
    assert client.skills is not None


async def test_skills_lifecycle(client):
    """
    Test create, get, list, export, update, toggle, delete skill.
    """
    unique_id = f"test_skill_{int(time.time())}"

    skill_form = SkillForm(
        id=unique_id,
        name="Test Skill",
        content="You are a helpful assistant that summarizes text.",
        meta=SkillMeta(tags=["test"]),
    )

    # 1. Create skill
    created_skill = await client.skills.create_new_skill(skill_form)
    assert created_skill is not None
    assert created_skill.id == unique_id
    assert created_skill.name == "Test Skill"

    # 2. Get skills (full list)
    skills_list = await client.skills.get_skills()
    assert isinstance(skills_list, list)
    found_skill = next((s for s in skills_list if s.id == unique_id), None)
    assert found_skill is not None
    assert found_skill.id == unique_id

    # 3. Get skill list (paginated with access info)
    paged = await client.skills.get_skill_list()
    assert paged.total >= 1
    found_paged = next((s for s in paged.items if s.id == unique_id), None)
    assert found_paged is not None
    assert found_paged.id == unique_id

    # 4. Get skill by ID
    fetched_skill = await client.skills.get_skill_by_id(unique_id)
    assert fetched_skill is not None
    assert fetched_skill.id == unique_id

    # 5. Export skills
    exported = await client.skills.export_skills()
    assert isinstance(exported, list)
    found_export = next((s for s in exported if s.id == unique_id), None)
    assert found_export is not None
    assert found_export.id == unique_id

    # 6. Update skill
    update_form = SkillForm(
        id=unique_id,
        name="Updated Test Skill",
        content="You are a helpful assistant that translates text.",
        meta=SkillMeta(tags=["test", "updated"]),
    )
    updated_skill = await client.skills.update_skill_by_id(unique_id, update_form)
    assert updated_skill is not None
    assert updated_skill.name == "Updated Test Skill"

    # 7. Toggle skill
    toggled_skill = await client.skills.toggle_skill_by_id(unique_id)
    assert toggled_skill is not None
    assert toggled_skill.is_active is False

    # Toggle back to active
    toggled_back = await client.skills.toggle_skill_by_id(unique_id)
    assert toggled_back is not None
    assert toggled_back.is_active is True

    # 8. Delete skill
    delete_result = await client.skills.delete_skill_by_id(unique_id)
    assert delete_result is True

    # 9. Verify deletion
    try:
        await client.skills.get_skill_by_id(unique_id)
        assert False, "Should have raised exception"
    except Exception:
        pass


async def test_update_skill_access(client):
    """Test updating skill access grants."""
    unique_id = f"test_skill_access_{int(time.time())}"

    # Create a skill
    skill_form = SkillForm(
        id=unique_id,
        name="Test Skill for Access",
        content="You are a helpful assistant.",
        meta=SkillMeta(),
        access_control=None,
    )

    created_skill = await client.skills.create_new_skill(skill_form)
    assert created_skill is not None
    assert created_skill.id == unique_id

    # Update access grants
    access_form = SkillAccessGrantsForm(
        access_grants=[
            {
                "principal_type": "user",
                "principal_id": "*",
                "permission": "read",
            }
        ]
    )

    updated_skill = await client.skills.update_skill_access_by_id(unique_id, access_form)
    assert updated_skill is not None
    assert updated_skill.id == unique_id
    assert hasattr(updated_skill, "access_grants")

    # Clean up
    await client.skills.delete_skill_by_id(unique_id)
