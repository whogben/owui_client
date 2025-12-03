import pytest
from owui_client.models.folders import (
    FolderForm,
    FolderUpdateForm,
    FolderParentIdForm,
    FolderIsExpandedForm,
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

