import pytest
import time
from owui_client.models.skills import SkillForm, SkillMeta, SkillAccessGrantsForm
from owui_client.models.auths import SigninForm

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio


async def test_skill_lifecycle(client):
    """
    Test creating, retrieving, updating, toggling, and deleting a skill.
    """
    # 1. Sign in as admin (Already authenticated by fixture)
    # form = SigninForm(email="admin@example.com", password="password123")
    # await client.auths.signin(form)

    # 2. Create a skill
    skill_id = f"test_skill_{int(time.time())}"
    skill_content = "You are a helpful assistant specialized in testing."
    form_data = SkillForm(
        id=skill_id,
        name="Test Skill",
        description="A test skill for integration testing",
        content=skill_content,
        meta=SkillMeta(tags=["test", "integration"]),
    )

    created_skill = await client.skills.create_new_skill(form_data)
    assert created_skill is not None
    assert created_skill.id == skill_id
    assert created_skill.name == "Test Skill"

    # 3. Get skill by ID
    fetched_skill = await client.skills.get_skill_by_id(skill_id)
    assert fetched_skill is not None
    assert fetched_skill.id == skill_id
    assert fetched_skill.write_access is True

    # 4. Get all skills
    skills = await client.skills.get_skills()
    assert len(skills) > 0
    ids = [s.id for s in skills]
    assert skill_id in ids

    # 5. Get skill list
    skill_list = await client.skills.get_skill_list()
    assert skill_list.total > 0
    list_ids = [s.id for s in skill_list.items]
    assert skill_id in list_ids
    assert hasattr(skill_list.items[0], "write_access")

    # 6. Update skill
    new_name = "Updated Test Skill"
    form_data.name = new_name
    updated_skill = await client.skills.update_skill_by_id(skill_id, form_data)
    assert updated_skill is not None
    assert updated_skill.name == new_name

    # 7. Toggle skill
    toggled_skill = await client.skills.toggle_skill_by_id(skill_id)
    assert toggled_skill is not None
    assert toggled_skill.is_active is False

    # Toggle back
    toggled_back = await client.skills.toggle_skill_by_id(skill_id)
    assert toggled_back is not None
    assert toggled_back.is_active is True

    # 8. Export skills
    exported = await client.skills.export_skills()
    assert len(exported) > 0
    exported_ids = [s.id for s in exported]
    assert skill_id in exported_ids

    # 9. Delete skill
    deleted = await client.skills.delete_skill_by_id(skill_id)
    assert deleted is True

    from httpx import HTTPStatusError

    try:
        await client.skills.get_skill_by_id(skill_id)
        assert False, "Skill should have been deleted"
    except HTTPStatusError as e:
        assert e.response.status_code == 404
