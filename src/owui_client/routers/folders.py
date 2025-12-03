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
    async def get_folders(self) -> List[FolderNameIdResponse]:
        """
        Get all folders.
        """
        return await self._request(
            "GET",
            "/v1/folders/",
            model=List[FolderNameIdResponse],
        )

    async def create_folder(self, form_data: FolderForm) -> FolderModel:
        """
        Create a new folder.
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
        Update a folder name by ID.
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
        Update a folder parent ID by ID.
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
        Update a folder is_expanded by ID.
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
        """
        params = {"delete_contents": delete_contents}
        return await self._request(
            "DELETE",
            f"/v1/folders/{id}",
            params=params,
            model=bool,
        )

