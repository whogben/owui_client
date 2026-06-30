"""Client for knowledge base endpoints including directories and file sync."""

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
    KnowledgeAccessGrantsForm,
    KnowledgeDirectoryModel,
    KnowledgeDirectoryCreateForm,
    KnowledgeDirectoryUpdateForm,
    KnowledgeFileMoveForm,
    SyncDiffForm,
    SyncDiffResponse,
    SyncCleanupForm,
    ExternalKnowledgeConnectionForm,
    ExternalKnowledgeSourceForm,
    ExternalKnowledgeCreateForm,
    ExternalKnowledgeSourceCreateForm,
    ExternalKnowledgeSourceUpdateForm,
    ExternalKnowledgeSourceTestForm,
    ExternalKnowledgeRetrieveTestForm,
    ExternalKnowledgeConnectionListResponse,
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
            "GET",
            "/v1/knowledge/",
            model=KnowledgeAccessListResponse,
            params={"page": page},
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
            json=form_data.model_dump(exclude_none=True),
        )

    async def get_knowledge_by_id(self, id: str) -> Optional[KnowledgeFilesResponse]:
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
            json=form_data.model_dump(exclude_none=True),
        )

    async def update_knowledge_access(
        self, id: str, access_grants: list[dict]
    ) -> Optional[KnowledgeFilesResponse]:
        """
        Update access grants for a knowledge base.

        Requires write access to the knowledge base or admin privileges.
        If setting public access (principal_id='*'), requires `sharing.public_knowledge` permission.
        If the user lacks permission, public grants will be stripped.

        Args:
            id: The ID of the knowledge base.
            access_grants: List of access grant dictionaries. Each dict should contain:
                - `principal_type` (str): 'user' or 'group'
                - `principal_id` (str): User/group ID, or '*' for public access
                - `permission` (str): 'read' or 'write'

        Returns:
            Optional[KnowledgeFilesResponse]: The updated knowledge base with files.
        """
        return await self._request(
            "POST",
            f"/v1/knowledge/{id}/access/update",
            model=KnowledgeFilesResponse,
            json={"access_grants": access_grants},
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
        self, id: str, file_id: str, directory_id: Optional[str] = None
    ) -> Optional[KnowledgeFilesResponse]:
        """
        Add a file to a knowledge base.

        Args:
            id: The ID of the knowledge base.
            file_id: The ID of the file to add.
            directory_id: Optional directory ID to place the file in. None for root level.

        Returns:
            Optional[KnowledgeFilesResponse]: The updated knowledge base.
        """
        data = {"file_id": file_id}
        if directory_id is not None:
            data["directory_id"] = directory_id
        return await self._request(
            "POST",
            f"/v1/knowledge/{id}/file/add",
            model=KnowledgeFilesResponse,
            json=data,
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

    # ── Directory endpoints ──────────────────────────────────────────

    async def create_knowledge_directory(
        self, id: str, form_data: KnowledgeDirectoryCreateForm
    ) -> KnowledgeDirectoryModel:
        """
        Create a new directory in a knowledge base.

        Args:
            id: The ID of the knowledge base.
            form_data: The directory creation form with name and optional parent_id.

        Returns:
            `KnowledgeDirectoryModel`: The created directory.
        """
        return await self._request(
            "POST",
            f"/v1/knowledge/{id}/dirs/create",
            model=KnowledgeDirectoryModel,
            json=form_data.model_dump(exclude_none=True),
        )

    async def update_knowledge_directory(
        self, id: str, dir_id: str, form_data: KnowledgeDirectoryUpdateForm
    ) -> KnowledgeDirectoryModel:
        """
        Update (rename or move) a directory in a knowledge base.

        Args:
            id: The ID of the knowledge base.
            dir_id: The ID of the directory to update.
            form_data: The update form with optional name and parent_id.

        Returns:
            `KnowledgeDirectoryModel`: The updated directory.
        """
        return await self._request(
            "POST",
            f"/v1/knowledge/{id}/dirs/{dir_id}/update",
            model=KnowledgeDirectoryModel,
            json=form_data.model_dump(exclude_none=True),
        )

    async def delete_knowledge_directory(
        self, id: str, dir_id: str, move_files: bool = True
    ) -> bool:
        """
        Delete a directory from a knowledge base.

        Args:
            id: The ID of the knowledge base.
            dir_id: The ID of the directory to delete.
            move_files: If True, contained files are moved to the parent directory.
                If False, files are also deleted. Defaults to True.

        Returns:
            bool: True if successful.
        """
        return await self._request(
            "DELETE",
            f"/v1/knowledge/{id}/dirs/{dir_id}/delete",
            model=bool,
            params={"move_files": move_files},
        )

    async def move_file_in_knowledge(
        self, id: str, form_data: KnowledgeFileMoveForm
    ) -> bool:
        """
        Move a file to a different directory within a knowledge base.

        Args:
            id: The ID of the knowledge base.
            form_data: The move form with file_id and optional directory_id.
                Set directory_id to None to move the file to the root.

        Returns:
            bool: True if successful.
        """
        return await self._request(
            "POST",
            f"/v1/knowledge/{id}/file/move",
            model=bool,
            json=form_data.model_dump(exclude_none=True),
        )

    # ── Pending files ────────────────────────────────────────────────

    async def get_pending_knowledge_files(self, id: str) -> list[dict]:
        """
        Get files that are still being processed for a knowledge base.

        After a file is uploaded with a knowledge_id, the backend processes it
        in a background task before linking it to the knowledge_file join table.
        This endpoint exposes those in-flight files so they can be displayed
        with a processing indicator.

        Args:
            id: The ID of the knowledge base.

        Returns:
            list[dict]: List of pending file objects (each a file dict as
            returned by the backend).
        """
        return await self._request(
            "GET",
            f"/v1/knowledge/{id}/files/pending",
            model=list[dict],
        )

    # ── Sync endpoints ───────────────────────────────────────────────

    async def sync_knowledge_diff(
        self, id: str, form_data: SyncDiffForm
    ) -> SyncDiffResponse:
        """
        Compute a diff between a local file manifest and the knowledge base.

        Returns which files need uploading, which are modified, which should be
        deleted, and which directories need to be created or removed.

        Args:
            id: The ID of the knowledge base.
            form_data: The sync diff form containing the local file manifest.

        Returns:
            `SyncDiffResponse`: The diff result with added, modified, deleted,
                mkdir, rmdir, and directory_map fields.
        """
        return await self._request(
            "POST",
            f"/v1/knowledge/{id}/sync/diff",
            model=SyncDiffResponse,
            json=form_data.model_dump(exclude_none=True),
        )

    async def sync_knowledge_cleanup(
        self, id: str, form_data: SyncCleanupForm
    ) -> bool:
        """
        Clean up stale files and orphaned directories after a sync.

        Removes the specified file IDs and directory IDs from the knowledge base,
        including their embeddings from the vector database.

        Args:
            id: The ID of the knowledge base.
            form_data: The cleanup form with file_ids and dir_ids to remove.

        Returns:
            bool: True if successful.
        """
        return await self._request(
            "POST",
            f"/v1/knowledge/{id}/sync/cleanup",
            model=bool,
            json=form_data.model_dump(exclude_none=True),
        )

    async def reindex_metadata(self) -> dict:
        """
        Reindex knowledge base metadata embeddings.

        Requires Admin privileges.

        Returns:
            dict: Statistics about the reindexing process (total, success).
        """
        return await self._request("POST", "/v1/knowledge/metadata/reindex", model=dict)

    async def export(self, id: str) -> bytes:
        """
        Export a knowledge base as a zip file.

        Requires Admin privileges.

        Args:
            id: The ID of the knowledge base.

        Returns:
            bytes: The zip file content.
        """
        return await self._request("GET", f"/v1/knowledge/{id}/export", model=bytes)

    # ── External knowledge connections & sources ─────────────────────
    # External knowledge bases are backed by an external vector DB
    # (qdrant / milvus / pgvector) instead of Open WebUI's built-in store.
    # A "connection" is the reusable endpoint+credentials; a "source" is a
    # specific collection inside it. All endpoints here are admin-only.

    async def get_external_knowledge_connections(
        self,
    ) -> ExternalKnowledgeConnectionListResponse:
        """
        List all external knowledge connections.

        Returns connections with their secret `auth_config` stripped (replaced
        by an `auth_configured` boolean). Admin only.

        Returns:
            `ExternalKnowledgeConnectionListResponse`: Sanitized connections and total count.
        """
        return await self._request(
            "GET",
            "/v1/knowledge/external/connections",
            model=ExternalKnowledgeConnectionListResponse,
        )

    async def create_external_knowledge_connection(
        self, form_data: ExternalKnowledgeConnectionForm
    ) -> dict:
        """
        Create a new external knowledge connection.

        Stores the connection under the `external_knowledge.connections` config
        key. `provider` must be `qdrant`, `milvus`, or `pgvector`. Admin only.

        Args:
            form_data: Connection definition (`provider`, `endpoint`, `name`,
                optional `auth_config`, `config`, `capabilities`, `enabled`).

        Returns:
            dict: The created connection, sanitized (`auth_config` removed,
                `auth_configured` flag added). Keys: `id`, `name`, `provider`,
                `endpoint`, `config`, `capabilities`, `health`, `enabled`,
                `created_by`, `created_at`, `updated_at`, `auth_configured`.

        Raises:
            HTTPException: 400 if `provider` is unsupported or name/endpoint empty.
        """
        return await self._request(
            "POST",
            "/v1/knowledge/external/connections",
            model=dict,
            json=form_data.model_dump(exclude_none=True),
        )

    async def get_external_knowledge_connection(self, id: str) -> dict:
        """
        Get a single external knowledge connection by id.

        Admin only.

        Args:
            id: The connection id.

        Returns:
            dict: The sanitized connection (same shape as
                `create_external_knowledge_connection`).

        Raises:
            HTTPException: 404 if the connection does not exist.
        """
        return await self._request(
            "GET",
            f"/v1/knowledge/external/connections/{id}",
            model=dict,
        )

    async def update_external_knowledge_connection(
        self, id: str, form_data: ExternalKnowledgeConnectionForm
    ) -> dict:
        """
        Update an existing external knowledge connection.

        Fully replaces name/provider/endpoint/config/capabilities/enabled.
        Pass `auth_config=None` to preserve the existing stored credentials, or
        a dict to overwrite them. Admin only.

        Args:
            id: The connection id.
            form_data: New connection definition.

        Returns:
            dict: The updated sanitized connection.

        Raises:
            HTTPException: 404 if the connection does not exist; 400 on invalid provider/fields.
        """
        return await self._request(
            "PATCH",
            f"/v1/knowledge/external/connections/{id}",
            model=dict,
            json=form_data.model_dump(exclude_none=True),
        )

    async def delete_external_knowledge_connection(self, id: str) -> bool:
        """
        Delete an external knowledge connection.

        Refuses deletion while any knowledge base still references it. Admin only.

        Args:
            id: The connection id.

        Returns:
            bool: True if deleted.

        Raises:
            HTTPException: 404 if not found; 400 if still mapped to a knowledge base.
        """
        return await self._request(
            "DELETE",
            f"/v1/knowledge/external/connections/{id}",
            model=bool,
        )

    async def test_external_knowledge_connection(self, id: str) -> dict:
        """
        Record a health check for a connection.

        Note: this does NOT actually connect to the external system. It records
        `ok = enabled and endpoint present`, stamps `checked_at`, persists the
        `health` dict on the connection, and returns it. Admin only.

        Args:
            id: The connection id.

        Returns:
            dict: Health record. Keys: `ok` (bool), `provider` (str),
                `checked_at` (int, epoch).

        Raises:
            HTTPException: 404 if the connection does not exist.
        """
        return await self._request(
            "POST",
            f"/v1/knowledge/external/connections/{id}/test",
            model=dict,
        )

    async def test_external_knowledge_source(
        self, form_data: ExternalKnowledgeSourceTestForm
    ) -> dict:
        """
        Run an ad-hoc retrieval test against a connection+source definition.

        Does not persist anything. If `connection_id` is set, the stored
        connection is loaded and merged with the supplied `connection`. The
        backend embeds `query`, queries the external system, and normalizes the
        results. Requires a working RAG embedding function. Admin only.

        Args:
            form_data: `connection_id` (optional), `connection`, `source`,
                `query`, `count`.

        Returns:
            dict: Normalized retrieval result. Keys: `documents` (list[str]),
                `metadatas` (list[dict]), `distances` (list[float]).

        Raises:
            HTTPException: 400 on bad source mapping or empty query; 404 if a
                given `connection_id` is not found.
        """
        return await self._request(
            "POST",
            "/v1/knowledge/external/source/test",
            model=dict,
            json=form_data.model_dump(exclude_none=True),
        )

    async def test_external_knowledge_retrieval(
        self, id: str, form_data: ExternalKnowledgeRetrieveTestForm
    ) -> dict:
        """
        Run an ad-hoc retrieval test against an existing connection by id.

        Like `test_external_knowledge_source` but resolves the connection from
        `id` instead of an inline definition. `source` is optional (defaults to
        a `test`/`payload.text` source). Requires a working RAG embedding
        function. Admin only.

        Args:
            id: The connection id.
            form_data: `query`, optional `source`, `count`.

        Returns:
            dict: Normalized retrieval result (`documents`, `metadatas`, `distances`).

        Raises:
            HTTPException: 404 if the connection does not exist; 400 on empty query / bad source.
        """
        return await self._request(
            "POST",
            f"/v1/knowledge/external/connections/{id}/retrieve-test",
            model=dict,
            json=form_data.model_dump(exclude_none=True),
        )

    async def create_external_knowledge(
        self, form_data: ExternalKnowledgeCreateForm
    ) -> Optional[KnowledgeResponse]:
        """
        Create a read-only knowledge base backed by an EXISTING connection.

        `connection_id` must already exist. Does not run a retrieval test. The
        resulting knowledge base has `meta.source == 'external'` and
        `meta.read_only == True`; local file operations are rejected. Note:
        deleting this knowledge base also removes the referenced connection
        (cascade). Admin only.

        Args:
            form_data: `name`, `description`, `connection_id`, `source`,
                optional `access_grants`.

        Returns:
            Optional[KnowledgeResponse]: The created (read-only, external-backed) knowledge base.

        Raises:
            HTTPException: 404 if `connection_id` is unknown; 400 if the name is empty or a KB already exists.
        """
        return await self._request(
            "POST",
            "/v1/knowledge/external/knowledge/create",
            model=KnowledgeResponse,
            json=form_data.model_dump(exclude_none=True),
        )

    async def create_external_knowledge_source(
        self, form_data: ExternalKnowledgeSourceCreateForm
    ) -> Optional[KnowledgeResponse]:
        """
        Create a connection AND a read-only external knowledge base in one step.

        Before persisting, the backend runs a retrieval `test` using `test_query`
        / `test_count`; if it returns no documents the request fails with 400.
        On success a new connection is stored and a read-only knowledge base is
        created referencing it. Deleting the resulting knowledge base also
        removes that connection (cascade). Requires a working RAG embedding
        function. Admin only.

        Args:
            form_data: `name`, `description`, `connection`, `source`,
                optional `access_grants`, `test_query`, `test_count`.

        Returns:
            Optional[KnowledgeResponse]: The created read-only external knowledge base.

        Raises:
            HTTPException: 400 if name is empty, the test returns no results, or a KB already exists.
        """
        return await self._request(
            "POST",
            "/v1/knowledge/external/source/create",
            model=KnowledgeResponse,
            json=form_data.model_dump(exclude_none=True),
        )

    async def update_external_knowledge_source(
        self, id: str, form_data: ExternalKnowledgeSourceUpdateForm
    ) -> Optional[KnowledgeResponse]:
        """
        Replace the connection+source backing an existing external knowledge base.

        Resolves the knowledge base by `id` (must be external / read-only), then
        re-runs a retrieval `test` (`test_query` / `test_count`); no documents =>
        400. Updates the stored connection (same id, in place) and the knowledge
        base meta. Requires a working RAG embedding function. Admin only.

        Args:
            id: The external knowledge base id.
            form_data: Full `connection` + `source` + `test_query` (+ optional
                `test_count`, `access_grants`, `name`, `description`).

        Returns:
            Optional[KnowledgeResponse]: The updated external knowledge base.

        Raises:
            HTTPException: 404 if the knowledge base or its connection is missing; 400 if the test returns no results.
        """
        return await self._request(
            "PATCH",
            f"/v1/knowledge/external/source/{id}",
            model=KnowledgeResponse,
            json=form_data.model_dump(exclude_none=True),
        )
