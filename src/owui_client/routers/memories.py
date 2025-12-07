from typing import Optional, List, Dict, Any
from owui_client.client_base import ResourceBase
from owui_client.models.memories import (
    MemoryModel,
    AddMemoryForm,
    MemoryUpdateModel,
    QueryMemoryForm,
)


class MemoriesClient(ResourceBase):
    """
    Client for the Memories endpoints.
    """

    async def get_memories(self) -> List[MemoryModel]:
        """
        Retrieve all memories associated with the authenticated user.

        Returns:
            List[MemoryModel]: A list of the user's memories.
        """
        return await self._request(
            "GET",
            "/v1/memories/",
            model=MemoryModel,
        )

    async def add_memory(self, form_data: AddMemoryForm) -> Optional[MemoryModel]:
        """
        Create a new memory for the authenticated user and add it to the vector database.

        Args:
            form_data: The content of the memory to create.

        Returns:
            Optional[MemoryModel]: The created memory object, or None if creation failed.
        """
        return await self._request(
            "POST",
            "/v1/memories/add",
            model=Optional[MemoryModel],
            json=form_data.model_dump(),
        )

    async def query_memory(self, form_data: QueryMemoryForm) -> Any:
        """
        Search for memories using vector similarity search.

        Args:
            form_data: The query parameters, including the search text and limit (k).

        Returns:
            Any: The search results from the vector database.
        """
        return await self._request(
            "POST",
            "/v1/memories/query",
            json=form_data.model_dump(),
        )

    async def reset_memory_from_vector_db(self) -> bool:
        """
        Reset the vector database collection for the user's memories.

        This deletes the existing collection and regenerates embeddings for all current memories.

        Returns:
            bool: True if the reset was successful.
        """
        return await self._request(
            "POST",
            "/v1/memories/reset",
            model=bool,
        )

    async def delete_memory_by_user_id(self) -> bool:
        """
        Delete all memories for the authenticated user.

        This removes all memories from both the primary database and the vector database.

        Returns:
            bool: True if the deletion was successful.
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
        Update a specific memory by its ID.

        Updates the content in both the primary database and the vector database.

        Args:
            memory_id: The unique identifier of the memory to update.
            form_data: The data to update (e.g., new content).

        Returns:
            Optional[MemoryModel]: The updated memory object, or None if the memory was not found.
        """
        return await self._request(
            "POST",
            f"/v1/memories/{memory_id}/update",
            model=Optional[MemoryModel],
            json=form_data.model_dump(),
        )

    async def delete_memory_by_id(self, memory_id: str) -> bool:
        """
        Delete a specific memory by its ID.

        Removes the memory from both the primary database and the vector database.

        Args:
            memory_id: The unique identifier of the memory to delete.

        Returns:
            bool: True if the deletion was successful.
        """
        return await self._request(
            "DELETE",
            f"/v1/memories/{memory_id}",
            model=bool,
        )

    async def get_embeddings(self) -> dict:
        """
        Test the embedding function.

        Generates an embedding for the text "hello world" to verify the embedding function is working.

        Returns:
            dict: A dictionary containing the embedding result.
        """
        return await self._request(
            "GET",
            "/v1/memories/ef",
        )
