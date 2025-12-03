import pytest
import uuid
from httpx import HTTPStatusError
from owui_client.models.auths import SigninForm, AddUserForm
from owui_client.models.groups import GroupForm, GroupUpdateForm, UserIdsForm, GroupExportResponse

pytestmark = pytest.mark.asyncio


async def test_group_lifecycle(client):
    """
    Test creating, retrieving, updating, and deleting a group.
    """
    # Create Group
    group_name = f"Test Group {uuid.uuid4()}"
    group_desc = "A test group"
    form = GroupForm(name=group_name, description=group_desc)

    group = await client.groups.create_new_group(form)
    assert group is not None
    assert group.name == group_name
    assert group.description == group_desc
    group_id = group.id

    # Get Group by ID
    fetched_group = await client.groups.get_group_by_id(group_id)
    assert fetched_group.id == group_id
    assert fetched_group.name == group_name

    # Get All Groups
    groups = await client.groups.get_groups()
    assert any(g.id == group_id for g in groups)

    # Update Group
    new_name = f"Updated Group {uuid.uuid4()}"
    update_form = GroupUpdateForm(name=new_name, description=group_desc)
    updated_group = await client.groups.update_group_by_id(group_id, update_form)
    assert updated_group.name == new_name

    # Delete Group
    success = await client.groups.delete_group_by_id(group_id)
    assert success is True

    # Verify Deletion
    with pytest.raises(HTTPStatusError) as exc:
        await client.groups.get_group_by_id(group_id)
    # Backend returns 401 for not found on this endpoint
    assert exc.value.response.status_code == 401


async def test_group_members(client):
    """
    Test adding and removing users from a group.
    """
    # Create a user to add
    user_email = f"groupuser_{uuid.uuid4()}@example.com"
    user_pass = "password123"
    user_name = "Group User"
    user_res = await client.auths.add_user(
        AddUserForm(
            email=user_email, password=user_pass, name=user_name, role="user"
        )
    )
    user_id = user_res.id

    # Create Group
    group = await client.groups.create_new_group(
        GroupForm(name=f"Member Group {uuid.uuid4()}", description="Test members")
    )
    group_id = group.id

    # Add User
    res = await client.groups.add_user_to_group(
        group_id, UserIdsForm(user_ids=[user_id])
    )
    assert res.member_count == 1

    # Check if we can see the group member count update in get_group
    g = await client.groups.get_group_by_id(group_id)
    assert g.member_count == 1

    # Remove User
    res = await client.groups.remove_users_from_group(
        group_id, UserIdsForm(user_ids=[user_id])
    )
    assert res.member_count == 0

    # Cleanup
    await client.groups.delete_group_by_id(group_id)


async def test_group_export_and_users_list(client):
    """
    Test exporting group and listing users in group.
    """
    # Create a user
    user_email = f"exportuser_{uuid.uuid4()}@example.com"
    user_res = await client.auths.add_user(
        AddUserForm(
            email=user_email, password="password123", name="Export User", role="user"
        )
    )
    user_id = user_res.id

    # Create Group
    group = await client.groups.create_new_group(
        GroupForm(name=f"Export Group {uuid.uuid4()}", description="Test export")
    )
    group_id = group.id

    # Add User
    await client.groups.add_user_to_group(group_id, UserIdsForm(user_ids=[user_id]))

    # 1. Test Export
    exported = await client.groups.export_group_by_id(group_id)
    assert exported is not None
    assert isinstance(exported, GroupExportResponse)
    assert exported.id == group_id
    assert user_id in exported.user_ids

    # 2. Test Get Users In Group
    users_in_group = await client.groups.get_users_in_group(group_id)
    assert isinstance(users_in_group, list)
    assert len(users_in_group) == 1
    assert users_in_group[0].id == user_id

    # Cleanup
    await client.groups.delete_group_by_id(group_id)
