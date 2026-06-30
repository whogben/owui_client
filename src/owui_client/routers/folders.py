from typing import Optional, List
from owui_client.client_base import ResourceBase
from owui_client.models.folders import (
    FolderForm,
    FolderUpdateForm,
    FolderModel,
    FolderNameIdResponse,
    FolderParentIdForm,
    FolderIsExpandedForm,
    FolderAccessGrantsForm,
    SharedFolderResponse,
)


class FoldersClient(ResourceBase):
    """
    Client for the Folders endpoints.
    """

    async def get_folders(self) -> List[FolderNameIdResponse]:
        """
        Get all folders for the current user.

        Returns:
            List[FolderNameIdResponse]: A list of folders with basic information.
        """
        return await self._request(
            "GET",
            "/v1/folders/",
            model=List[FolderNameIdResponse],
        )

    async def get_shared_folders(self) -> List[SharedFolderResponse]:
        """
        Get all folders shared with the current user (not owned by them).

        Lists folders the caller can access via direct user grants, group membership, or
        public (`user:*`) grants. Each entry includes the owner's display name and the
        highest permission the caller holds (`'read'` or `'write'`). Child folders of a
        shared root inherit the root's permission. Folders owned by the caller are excluded.

        Requires the folders feature to be enabled and the `features.folders` permission.

        Returns:
            List[SharedFolderResponse]: Folders shared with the current user. Empty if none.
        """
        return await self._request(
            "GET",
            "/v1/folders/shared",
            model=List[SharedFolderResponse],
        )

    async def create_folder(self, form_data: FolderForm) -> FolderModel:
        """
        Create a new root folder.

        To create a nested folder, create a root folder and then move it using `update_folder_parent_id_by_id`.

        Args:
            form_data: The form data for creating the folder.

        Returns:
            `FolderModel`: The created folder model.
        """
        return await self._request(
            "POST",
            "/v1/folders/",
            json=form_data.model_dump(exclude_none=True),
            model=FolderModel,
        )

    async def get_folder_by_id(self, id: str) -> Optional[FolderModel]:
        """
        Get a folder by ID.

        Args:
            id: The folder ID.

        Returns:
            Optional[FolderModel]: The folder model, or None if not found.
        """
        return await self._request(
            "GET",
            f"/v1/folders/{id}",
            model=Optional[FolderModel],
        )

    async def update_folder_name_by_id(
        self, id: str, form_data: FolderUpdateForm
    ) -> FolderModel:
        """
        Update a folder's details (name, data, meta) by ID.

        Args:
            id: The folder ID.
            form_data: The update form data.

        Returns:
            `FolderModel`: The updated folder model.
        """
        return await self._request(
            "POST",
            f"/v1/folders/{id}/update",
            json=form_data.model_dump(exclude_unset=True, exclude_none=True),
            model=FolderModel,
        )

    async def update_folder_parent_id_by_id(
        self, id: str, form_data: FolderParentIdForm
    ) -> FolderModel:
        """
        Move a folder to a new parent folder.

        Args:
            id: The folder ID.
            form_data: The parent ID form data.

        Returns:
            `FolderModel`: The updated folder model with the new parent ID.
        """
        return await self._request(
            "POST",
            f"/v1/folders/{id}/update/parent",
            json=form_data.model_dump(exclude_none=True),
            model=FolderModel,
        )

    async def update_folder_is_expanded_by_id(
        self, id: str, form_data: FolderIsExpandedForm
    ) -> FolderModel:
        """
        Update a folder's expansion status (is_expanded) by ID.

        Args:
            id: The folder ID.
            form_data: The is_expanded form data.

        Returns:
            `FolderModel`: The updated folder model.
        """
        return await self._request(
            "POST",
            f"/v1/folders/{id}/update/expanded",
            json=form_data.model_dump(exclude_none=True),
            model=FolderModel,
        )

    async def update_folder_access_by_id(
        self, id: str, form_data: FolderAccessGrantsForm
    ) -> FolderModel:
        """
        Replace the access grants on a folder (share it with users, groups, or everyone).

        The supplied `access_grants` list fully replaces the folder's existing grants.
        Only the folder owner, an admin, or a user with write access may call this. For
        non-admin users, grants that exceed their sharing permissions are silently stripped
        (e.g. public or individual-user grants); admins are not filtered.

        Args:
            id: The folder ID.
            form_data: The access grants form. Each grant dict uses keys `principal_type`
                ('user' or 'group'), `principal_id` (a user/group ID or '*' for public),
                `permission` ('read' or 'write'), and optional `id`.

        Returns:
            `FolderModel`: The updated folder, including its `access_grants`
            (the resulting grant dicts). `get_folder_by_id` also returns them.
        """
        return await self._request(
            "POST",
            f"/v1/folders/{id}/access/update",
            json=form_data.model_dump(exclude_none=True),
            model=FolderModel,
        )

    async def get_shared_folder_chats(self, id: str) -> dict:
        """
        List the chats inside a shared folder.

        Returns chats across all users who placed a chat in the folder, each annotated
        with `owner_name` and a `readonly` flag (True for chats not owned by the caller).
        The caller needs at least read access to the folder; owners and admins get write.

        Args:
            id: The folder ID.

        Returns:
            dict: The shared-folder chats payload.

            Dict Fields:
                - `chats` (list[dict], required): Chats in the folder. Each dict has:
                  `id` (str), `title` (str), `user_id` (str), `updated_at` (int),
                  `created_at` (int), `last_read_at` (int or None), `owner_name` (str),
                  and `readonly` (bool, True when the chat is not owned by the caller).
                - `folder_permission` (str, required): The caller's access level on the
                  folder: `'read'` or `'write'`.
        """
        return await self._request(
            "GET",
            f"/v1/folders/{id}/shared/chats",
            model=dict,
        )

    async def delete_folder_by_id(
        self, id: str, delete_contents: Optional[bool] = True
    ) -> bool:
        """
        Delete a folder by ID.

        Args:
            id: The folder ID.
            delete_contents: Whether to delete the contents of the folder (chats, etc). Defaults to True.
                             If False, contents might be moved or handled differently depending on the backend logic (usually chats are moved to root or detached).

        Returns:
            bool: True if successful.
        """
        params = {"delete_contents": delete_contents}
        return await self._request(
            "DELETE",
            f"/v1/folders/{id}",
            params=params,
            model=bool,
        )
