from typing import Optional, List
from owui_client.client_base import ResourceBase
from owui_client.models.folders import (
    FolderForm,
    FolderUpdateForm,
    FolderModel,
    FolderNameIdResponse,
    FolderParentIdForm,
    FolderIsExpandedForm,
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

    async def create_folder(self, form_data: FolderForm) -> FolderModel:
        """
        Create a new root folder.

        To create a nested folder, create a root folder and then move it using `update_folder_parent_id_by_id`.

        Args:
            form_data: The form data for creating the folder.

        Returns:
            FolderModel: The created folder model.
        """
        return await self._request(
            "POST",
            "/v1/folders/",
            json=form_data.model_dump(),
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
            FolderModel: The updated folder model.
        """
        return await self._request(
            "POST",
            f"/v1/folders/{id}/update",
            json=form_data.model_dump(exclude_unset=True),
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
            FolderModel: The updated folder model with the new parent ID.
        """
        return await self._request(
            "POST",
            f"/v1/folders/{id}/update/parent",
            json=form_data.model_dump(),
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
            FolderModel: The updated folder model.
        """
        return await self._request(
            "POST",
            f"/v1/folders/{id}/update/expanded",
            json=form_data.model_dump(),
            model=FolderModel,
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
