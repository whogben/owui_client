from typing import Optional, List
from owui_client.client_base import ResourceBase
from owui_client.models.knowledge import (
    KnowledgeResponse,
    KnowledgeUserResponse,
    KnowledgeFilesResponse,
    KnowledgeForm,
    KnowledgeFileIdForm,
)


class KnowledgeClient(ResourceBase):
    async def get_knowledge(self) -> List[KnowledgeUserResponse]:
        """
        Get knowledge bases (read access).
        """
        return await self._request(
            "GET", "/v1/knowledge/", model=KnowledgeUserResponse
        )

    async def get_knowledge_list(self) -> List[KnowledgeUserResponse]:
        """
        Get knowledge bases list (write access).
        """
        return await self._request(
            "GET", "/v1/knowledge/list", model=KnowledgeUserResponse
        )

    async def create_new_knowledge(
        self, form_data: KnowledgeForm
    ) -> Optional[KnowledgeResponse]:
        """
        Create a new knowledge base.
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
        """
        return await self._request(
            "GET", f"/v1/knowledge/{id}", model=KnowledgeFilesResponse
        )

    async def update_knowledge_by_id(
        self, id: str, form_data: KnowledgeForm
    ) -> Optional[KnowledgeFilesResponse]:
        """
        Update a knowledge base by ID.
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
        """
        return await self._request("DELETE", f"/v1/knowledge/{id}/delete", model=bool)

    async def add_file_to_knowledge(
        self, id: str, file_id: str
    ) -> Optional[KnowledgeFilesResponse]:
        """
        Add a file to a knowledge base.
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
        """
        return await self._request(
            "POST", f"/v1/knowledge/{id}/reset", model=KnowledgeResponse
        )

    async def reindex_knowledge_files(self) -> bool:
        """
        Reindex all knowledge files.
        """
        return await self._request("POST", "/v1/knowledge/reindex", model=bool)

    async def add_files_to_knowledge_batch(
        self, id: str, file_ids: List[str]
    ) -> Optional[KnowledgeFilesResponse]:
        """
        Add multiple files to a knowledge base in batch.
        """
        data = [{"file_id": fid} for fid in file_ids]
        return await self._request(
            "POST",
            f"/v1/knowledge/{id}/files/batch/add",
            model=KnowledgeFilesResponse,
            json=data,
        )

