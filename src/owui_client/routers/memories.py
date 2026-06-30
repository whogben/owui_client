from typing import Optional, List, Dict, Any
from owui_client.client_base import ResourceBase
from owui_client.models.memories import (
    MemoryModel,
    AddMemoryForm,
    MemoryUpdateModel,
    QueryMemoryForm,
    ListMemoryPathsForm,
    ReadMemoryPathForm,
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
            json=form_data.model_dump(exclude_none=True),
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
            json=form_data.model_dump(exclude_none=True),
        )

    async def list_memory_paths(self, form_data: ListMemoryPathsForm) -> dict:
        """
        List the user's memories grouped into a path/type tree.

        Groups memories by `(path, type)` and returns one summary entry per
        group (with member count, most-recent `updated_at`, and up to 20
        immediate child paths). Useful for browsing/navigating scoped
        memories; counterpart to `read_memory_path`, which returns the actual
        memory rows at a single path.

        Args:
            form_data: Filtering/grouping options (`query`, `type`, `limit`).

        Returns:
            A dict shaped as `{'paths': [ {path, type, count, updated_at,
            children: [str, ...]}, ...], 'count': int}`. `path` may be `None`
            for unscoped memories.
        """
        return await self._request(
            "POST",
            "/v1/memories/paths",
            json=form_data.model_dump(exclude_none=True),
        )

    async def read_memory_path(self, form_data: ReadMemoryPathForm) -> dict:
        """
        Read the memories located at a specific path.

        Returns memories at exactly `path` plus ancestor-path memories and,
        when `include_children=True`, memories in descendant paths. Also
        returns the ancestor (`parents`) and immediate child paths for
        navigation. Counterpart to `list_memory_paths`, which summarizes all
        paths as groups rather than returning rows.

        Args:
            form_data: Read options (`path` required, plus `type`,
                `include_children`, `limit`).

        Returns:
            A dict shaped as `{'path': str, 'parents': [str, ...],
            'children': [str, ...], 'memories': [`MemoryModel` as dict, ...]}`.
        """
        return await self._request(
            "POST",
            "/v1/memories/path",
            json=form_data.model_dump(exclude_none=True),
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
            json=form_data.model_dump(exclude_none=True),
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
