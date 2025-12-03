from typing import Optional, List, Dict, Any
from owui_client.client_base import ResourceBase
from owui_client.models.memories import (
    MemoryModel,
    AddMemoryForm,
    MemoryUpdateModel,
    QueryMemoryForm,
)


class MemoriesClient(ResourceBase):
    async def get_memories(self) -> List[MemoryModel]:
        """
        Get all memories for the current user.

        :return: List of memories
        """
        return await self._request(
            "GET",
            "/v1/memories/",
            model=MemoryModel,
        )

    async def add_memory(self, form_data: AddMemoryForm) -> Optional[MemoryModel]:
        """
        Add a new memory.

        :param form_data: The memory content
        :return: The created memory
        """
        return await self._request(
            "POST",
            "/v1/memories/add",
            model=Optional[MemoryModel],
            json=form_data.model_dump(),
        )

    async def query_memory(self, form_data: QueryMemoryForm) -> Any:
        """
        Query memories.

        :param form_data: The query content
        :return: Query results
        """
        return await self._request(
            "POST",
            "/v1/memories/query",
            json=form_data.model_dump(),
        )

    async def reset_memory_from_vector_db(self) -> bool:
        """
        Reset memory from vector DB.

        :return: True if successful
        """
        return await self._request(
            "POST",
            "/v1/memories/reset",
            model=bool,
        )

    async def delete_memory_by_user_id(self) -> bool:
        """
        Delete all memories for the current user.

        :return: True if successful
        """
        return await self._request(
            "DELETE",
            "/v1/memories/delete/user",
            model=bool,
        )

    async def update_memory_by_id(
        self, memory_id: str, form_data: MemoryUpdateModel
    ) -> Optional[MemoryModel]:
        """
        Update a memory by ID.

        :param memory_id: The ID of the memory
        :param form_data: The update data
        :return: The updated memory
        """
        return await self._request(
            "POST",
            f"/v1/memories/{memory_id}/update",
            model=Optional[MemoryModel],
            json=form_data.model_dump(),
        )

    async def delete_memory_by_id(self, memory_id: str) -> bool:
        """
        Delete a memory by ID.

        :param memory_id: The ID of the memory
        :return: True if successful
        """
        return await self._request(
            "DELETE",
            f"/v1/memories/{memory_id}",
            model=bool,
        )

    async def get_embeddings(self) -> dict:
        """
        Test embedding function.
        
        :return: Dictionary containing the embedding result for "hello world"
        """
        return await self._request(
            "GET",
            "/v1/memories/ef",
        )
