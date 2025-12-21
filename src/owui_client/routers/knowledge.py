from typing import Optional, List
from owui_client.client_base import ResourceBase
from owui_client.models.knowledge import (
    KnowledgeResponse,
    KnowledgeUserResponse,
    KnowledgeFilesResponse,
    KnowledgeForm,
    KnowledgeFileIdForm,
    KnowledgeAccessListResponse,
    KnowledgeFileListResponse,
)


class KnowledgeClient(ResourceBase):
    """
    Client for the Knowledge endpoints.
    """

    async def get_knowledge(self, page: int = 1) -> KnowledgeAccessListResponse:
        """
        Get knowledge bases (read access).

        Args:
            page: Page number (default 1).

        Returns:
            `KnowledgeAccessListResponse`: List of knowledge bases the user has read access to, with pagination.
        """
        return await self._request(
            "GET", "/v1/knowledge/", model=KnowledgeAccessListResponse, params={"page": page}
        )

    async def get_knowledge_list(self) -> List[KnowledgeUserResponse]:
        """
        Get knowledge bases list (write access).

        Returns:
            List[KnowledgeUserResponse]: List of knowledge bases the user has write access to.
        """
        return await self._request(
            "GET", "/v1/knowledge/list", model=KnowledgeUserResponse
        )

    async def search_knowledge_bases(
        self,
        query: Optional[str] = None,
        view_option: Optional[str] = None,
        page: Optional[int] = 1,
    ) -> KnowledgeAccessListResponse:
        """
        Search knowledge bases.

        Args:
            query: Search query string.
            view_option: View option filter (e.g., 'created', 'shared').
            page: Page number (default 1).

        Returns:
            `KnowledgeAccessListResponse`: List of knowledge bases matching criteria.
        """
        params = {}
        if query:
            params["query"] = query
        if view_option:
            params["view_option"] = view_option
        if page:
            params["page"] = page

        return await self._request(
            "GET",
            "/v1/knowledge/search",
            model=KnowledgeAccessListResponse,
            params=params,
        )

    async def search_knowledge_files(
        self,
        query: Optional[str] = None,
        page: Optional[int] = 1,
    ) -> KnowledgeFileListResponse:
        """
        Search files across all knowledge bases.

        Args:
            query: Search query string.
            page: Page number (default 1).

        Returns:
            `KnowledgeFileListResponse`: List of files matching criteria.
        """
        params = {}
        if query:
            params["query"] = query
        if page:
            params["page"] = page

        return await self._request(
            "GET",
            "/v1/knowledge/search/files",
            model=KnowledgeFileListResponse,
            params=params,
        )

    async def create_new_knowledge(
        self, form_data: KnowledgeForm
    ) -> Optional[KnowledgeResponse]:
        """
        Create a new knowledge base.

        Requires `workspace.knowledge` permission.
        If `access_control` is `None` (public), requires `sharing.public_knowledge` permission.
        If the user lacks `sharing.public_knowledge` permission, `access_control` will default to private `{}`.

        Args:
            form_data: The data for the new knowledge base.

        Returns:
            Optional[KnowledgeResponse]: The created knowledge base.
        """
        return await self._request(
            "POST",
            "/v1/knowledge/create",
            model=KnowledgeResponse,
            json=form_data.model_dump(),
        )

    async def get_knowledge_by_id(
        self, id: str
    ) -> Optional[KnowledgeFilesResponse]:
        """
        Get a knowledge base by ID.

        Args:
            id: The ID of the knowledge base.

        Returns:
            Optional[KnowledgeFilesResponse]: The knowledge base details including files.
        """
        return await self._request(
            "GET", f"/v1/knowledge/{id}", model=KnowledgeFilesResponse
        )

    async def update_knowledge_by_id(
        self, id: str, form_data: KnowledgeForm
    ) -> Optional[KnowledgeFilesResponse]:
        """
        Update a knowledge base by ID.

        Requires write access to the knowledge base or admin privileges.
        If `access_control` is `None` (public), requires `sharing.public_knowledge` permission.
        If the user lacks `sharing.public_knowledge` permission, `access_control` will default to private `{}`.

        Args:
            id: The ID of the knowledge base.
            form_data: The updated data.

        Returns:
            Optional[KnowledgeFilesResponse]: The updated knowledge base.
        """
        return await self._request(
            "POST",
            f"/v1/knowledge/{id}/update",
            model=KnowledgeFilesResponse,
            json=form_data.model_dump(),
        )

    async def delete_knowledge_by_id(self, id: str) -> bool:
        """
        Delete a knowledge base by ID.

        Args:
            id: The ID of the knowledge base.

        Returns:
            bool: True if successful.
        """
        return await self._request("DELETE", f"/v1/knowledge/{id}/delete", model=bool)

    async def add_file_to_knowledge(
        self, id: str, file_id: str
    ) -> Optional[KnowledgeFilesResponse]:
        """
        Add a file to a knowledge base.

        Args:
            id: The ID of the knowledge base.
            file_id: The ID of the file to add.

        Returns:
            Optional[KnowledgeFilesResponse]: The updated knowledge base.
        """
        return await self._request(
            "POST",
            f"/v1/knowledge/{id}/file/add",
            model=KnowledgeFilesResponse,
            json={"file_id": file_id},
        )

    async def update_file_from_knowledge(
        self, id: str, file_id: str
    ) -> Optional[KnowledgeFilesResponse]:
        """
        Update a file in a knowledge base (re-process).

        Args:
            id: The ID of the knowledge base.
            file_id: The ID of the file to update.

        Returns:
            Optional[KnowledgeFilesResponse]: The updated knowledge base.
        """
        return await self._request(
            "POST",
            f"/v1/knowledge/{id}/file/update",
            model=KnowledgeFilesResponse,
            json={"file_id": file_id},
        )

    async def remove_file_from_knowledge(
        self, id: str, file_id: str, delete_file: bool = True
    ) -> Optional[KnowledgeFilesResponse]:
        """
        Remove a file from a knowledge base.

        Args:
            id: The ID of the knowledge base.
            file_id: The ID of the file to remove.
            delete_file: Whether to delete the file from the system as well.

        Returns:
            Optional[KnowledgeFilesResponse]: The updated knowledge base.
        """
        return await self._request(
            "POST",
            f"/v1/knowledge/{id}/file/remove",
            model=KnowledgeFilesResponse,
            params={"delete_file": delete_file},
            json={"file_id": file_id},
        )

    async def reset_knowledge_by_id(self, id: str) -> Optional[KnowledgeResponse]:
        """
        Reset a knowledge base by ID (remove all files).

        Args:
            id: The ID of the knowledge base.

        Returns:
            Optional[KnowledgeResponse]: The reset knowledge base.
        """
        return await self._request(
            "POST", f"/v1/knowledge/{id}/reset", model=KnowledgeResponse
        )

    async def reindex_knowledge_files(self) -> bool:
        """
        Reindex all knowledge files.
        
        This is a blocking operation that reprocesses all files in all knowledge bases.
        Requires Admin privileges.

        Returns:
            bool: True if successful.
        """
        return await self._request("POST", "/v1/knowledge/reindex", model=bool)

    async def add_files_to_knowledge_batch(
        self, id: str, file_ids: List[str]
    ) -> Optional[KnowledgeFilesResponse]:
        """
        Add multiple files to a knowledge base in batch.

        This process iterates through files and adds them to the vector database.
        Failures are collected in the response `warnings` field.

        Args:
            id: The ID of the knowledge base.
            file_ids: List of file IDs to add.

        Returns:
            Optional[KnowledgeFilesResponse]: The updated knowledge base.
            Check `warnings` field for any processing errors.
        """
        data = [{"file_id": fid} for fid in file_ids]
        return await self._request(
            "POST",
            f"/v1/knowledge/{id}/files/batch/add",
            model=KnowledgeFilesResponse,
            json=data,
        )
