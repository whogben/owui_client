import uuid

import pytest
from owui_client.client import OpenWebUI
from owui_client.models.auths import AddUserForm
from owui_client.models.folders import (
    FolderForm,
    FolderUpdateForm,
    FolderParentIdForm,
    FolderIsExpandedForm,
    FolderAccessGrantsForm,
)


@pytest.mark.asyncio
async def test_folders_crud(client):
    # 1. Create a folder
    folder_name = "Test Folder"
    folder_form = FolderForm(name=folder_name)
    folder = await client.folders.create_folder(folder_form)
    assert folder.name == folder_name
    assert folder.id is not None

    # 2. Get all folders
    folders = await client.folders.get_folders()
    assert len(folders) > 0
    assert any(f.id == folder.id for f in folders)

    # 3. Get folder by ID
    fetched_folder = await client.folders.get_folder_by_id(folder.id)
    assert fetched_folder.id == folder.id
    assert fetched_folder.name == folder_name

    # 4. Update folder name
    new_name = "Updated Folder Name"
    update_form = FolderUpdateForm(name=new_name)
    updated_folder = await client.folders.update_folder_name_by_id(
        folder.id, update_form
    )
    assert updated_folder.name == new_name

    # 5. Create another folder to be parent
    parent_folder_form = FolderForm(name="Parent Folder")
    parent_folder = await client.folders.create_folder(parent_folder_form)

    # 6. Update folder parent
    parent_id_form = FolderParentIdForm(parent_id=parent_folder.id)
    updated_folder_parent = await client.folders.update_folder_parent_id_by_id(
        folder.id, parent_id_form
    )
    assert updated_folder_parent.parent_id == parent_folder.id

    # 7. Update folder is_expanded
    is_expanded_form = FolderIsExpandedForm(is_expanded=True)
    updated_folder_expanded = await client.folders.update_folder_is_expanded_by_id(
        folder.id, is_expanded_form
    )
    assert updated_folder_expanded.is_expanded is True

    # 8. Delete folders
    deleted = await client.folders.delete_folder_by_id(folder.id)
    assert deleted is True
    
    # Verify deletion
    folders_after_delete = await client.folders.get_folders()
    assert not any(f.id == folder.id for f in folders_after_delete)

    # Cleanup parent folder
    deleted_parent = await client.folders.delete_folder_by_id(parent_folder.id)
    assert deleted_parent is True


@pytest.mark.asyncio
async def test_update_folder_access_by_id(client):
    """Share a folder with everyone (public read) via the access/update endpoint."""
    folder = await client.folders.create_folder(FolderForm(name="Shared Folder"))

    try:
        # Admin can grant any access (sharing permission filters are bypassed for admins).
        grants = [
            {"principal_type": "user", "principal_id": "*", "permission": "read"}
        ]
        updated = await client.folders.update_folder_access_by_id(
            folder.id, FolderAccessGrantsForm(access_grants=grants)
        )
        assert updated.id == folder.id
        assert updated.name == "Shared Folder"
        # The returned FolderModel surfaces access_grants (not silently dropped).
        assert isinstance(updated.access_grants, list)
        assert len(updated.access_grants) == 1
        assert updated.access_grants[0].principal_id == "*"
        assert updated.access_grants[0].permission == "read"

        # get_folder_by_id also returns the grants.
        fetched = await client.folders.get_folder_by_id(folder.id)
        assert isinstance(fetched.access_grants, list)
        assert len(fetched.access_grants) == 1
        assert fetched.access_grants[0].principal_id == "*"
    finally:
        await client.folders.delete_folder_by_id(folder.id)


@pytest.mark.asyncio
async def test_get_shared_folders(client):
    """A non-owner user sees an admin-shared (public) folder in their shared list."""
    folder = await client.folders.create_folder(FolderForm(name="Owner Shared Folder"))

    # Create a second, non-admin user to act as the share recipient.
    user_email = f"shared-folders-{uuid.uuid4().hex[:8]}@example.com"
    added = await client.auths.add_user(
        AddUserForm(name="Shared Viewer", email=user_email, password="pw", role="user")
    )
    viewer = OpenWebUI(api_url=client.api_url, api_key=added.token)

    try:
        # Owner shares the folder with everyone (public read).
        await client.folders.update_folder_access_by_id(
            folder.id,
            FolderAccessGrantsForm(
                access_grants=[
                    {"principal_type": "user", "principal_id": "*", "permission": "read"}
                ]
            ),
        )

        shared = await viewer.folders.get_shared_folders()
        assert isinstance(shared, list)
        matched = [s for s in shared if s.id == folder.id]
        assert matched, "shared folder not visible to non-owner"
        assert matched[0].permission == "read"
        # The folder is owned by the admin, not by the viewer.
        assert matched[0].user_id != added.id

        # The owner themselves does not see their own folder in the shared list.
        owner_shared = await client.folders.get_shared_folders()
        assert isinstance(owner_shared, list)
        assert not any(s.id == folder.id for s in owner_shared)
    finally:
        await client.folders.delete_folder_by_id(folder.id)
        await client.users.delete_user_by_id(added.id)


@pytest.mark.asyncio
async def test_get_shared_folder_chats(client):
    """Owner view of a shared folder's chats returns the chats payload and permission."""
    folder = await client.folders.create_folder(FolderForm(name="Chats Shared Folder"))

    try:
        result = await client.folders.get_shared_folder_chats(folder.id)
        assert isinstance(result, dict)
        assert "chats" in result and isinstance(result["chats"], list)
        # Owner has write access to their own folder.
        assert result["folder_permission"] == "write"
    finally:
        await client.folders.delete_folder_by_id(folder.id)


async def test_mark_folder_chats_read(client):
    """Marking a folder's chats as read returns the expected summary dict."""
    folder = await client.folders.create_folder(FolderForm(name="Read Test Folder"))
    try:
        result = await client.folders.mark_folder_chats_read(folder.id)
        assert isinstance(result, dict)
        assert result["folder_id"] == folder.id
        assert "updated_count" in result
        assert "folder_unread_counts" in result
    finally:
        await client.folders.delete_folder_by_id(folder.id)

