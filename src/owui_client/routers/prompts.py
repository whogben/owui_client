"""Client for the Prompts endpoints."""

from typing import Optional, List
from urllib.parse import quote
from owui_client.client_base import ResourceBase
from owui_client.models.prompts import (
    PromptModel,
    PromptUserResponse,
    PromptAccessResponse,
    PromptAccessListResponse,
    PromptForm,
    PromptVersionUpdateForm,
    PromptMetadataForm,
    PromptAccessGrantsForm,
    PromptHistoryModel,
    PromptHistoryResponse,
    PromptDiffResponse,
)


class PromptsClient(ResourceBase):
    """
    Client for the Prompts endpoints.

    Prompts are reusable command templates that can be invoked with `/command` syntax.
    They support versioning, tagging, and access control.
    """

    async def get_prompts(self) -> List[PromptModel]:
        """Get all prompts the user has read access to.

        Returns:
            List[PromptModel]: List of prompts.
        """
        return await self._request("GET", "/v1/prompts/", model=List[PromptModel])

    async def get_prompt_tags(self) -> List[str]:
        """Get all unique tags from prompts the user has access to.

        Returns:
            List[str]: Sorted list of unique tag strings.
        """
        return await self._request("GET", "/v1/prompts/tags", model=List[str])

    async def get_prompt_list(
        self,
        query: Optional[str] = None,
        view_option: Optional[str] = None,
        tag: Optional[str] = None,
        order_by: Optional[str] = None,
        direction: Optional[str] = None,
        page: Optional[int] = None,
    ) -> PromptAccessListResponse:
        """Get paginated list of prompts with access information.

        Supports filtering and pagination for browsing prompts.

        Args:
            query: Search string to filter prompts by name or command.
            view_option: Filter by view option (e.g., 'all', 'owned', 'shared').
            tag: Filter by tag name.
            order_by: Field to order by (e.g., 'name', 'created_at', 'updated_at').
            direction: Sort direction ('asc' or 'desc').
            page: Page number (1-indexed, default 1).

        Returns:
            `PromptAccessListResponse`: Paginated list with access info.
        """
        params = {}
        if query is not None:
            params["query"] = query
        if view_option is not None:
            params["view_option"] = view_option
        if tag is not None:
            params["tag"] = tag
        if order_by is not None:
            params["order_by"] = order_by
        if direction is not None:
            params["direction"] = direction
        if page is not None:
            params["page"] = page

        return await self._request(
            "GET", "/v1/prompts/list", params=params, model=PromptAccessListResponse
        )

    async def create_new_prompt(self, form_data: PromptForm) -> Optional[PromptModel]:
        """Create a new prompt.

        Args:
            form_data: The prompt data. The `command` field must start with a slash (e.g., '/help').

        Returns:
            Optional[PromptModel]: The created prompt.
        """
        return await self._request(
            "POST",
            "/v1/prompts/create",
            json=form_data.model_dump(),
            model=Optional[PromptModel],
        )

    async def get_prompt_by_command(
        self, command: str
    ) -> Optional[PromptAccessResponse]:
        """Get a prompt by its command trigger.

        Args:
            command: The command trigger (e.g., '/help' or 'help'). Leading slash is optional.

        Returns:
            Optional[PromptAccessResponse]: The prompt with access info.
        """
        # Backend stores command with leading slash and does exact match. Path param cannot
        # contain a raw slash, so we try URL-encoded slash first; if that returns non-JSON
        # (e.g. some servers mishandle %2F), fall back to resolving via list.
        normalized = command if command.startswith("/") else f"/{command}"
        try:
            out = await self._request(
                "GET",
                f"/v1/prompts/command/{quote(normalized, safe='')}",
                model=Optional[PromptAccessResponse],
            )
            if isinstance(out, PromptAccessResponse):
                return out
        except Exception:
            pass
        # Fallback: resolve by listing and matching command, then fetch by id for full access response.
        prompts = await self.get_prompts()
        for p in prompts or []:
            if p.command == normalized or p.command == command:
                return await self.get_prompt_by_id(p.id)
        return None

    async def get_prompt_by_id(self, prompt_id: str) -> Optional[PromptAccessResponse]:
        """Get a prompt by its ID.

        Args:
            prompt_id: The unique identifier of the prompt.

        Returns:
            Optional[PromptAccessResponse]: The prompt with access info.
        """
        return await self._request(
            "GET",
            f"/v1/prompts/id/{prompt_id}",
            model=Optional[PromptAccessResponse],
        )

    async def update_prompt_by_command(
        self, command: str, form_data: PromptForm
    ) -> Optional[PromptModel]:
        """Update a prompt by its command trigger.

        Resolves the prompt by command then updates by ID. Creates a new history entry.

        Args:
            command: The command trigger (e.g., '/help' or 'help').
            form_data: The updated prompt data.

        Returns:
            Optional[PromptModel]: The updated prompt.
        """
        prompt = await self.get_prompt_by_command(command)
        if prompt is None:
            return None
        return await self.update_prompt_by_id(prompt.id, form_data)

    async def update_prompt_by_id(
        self, prompt_id: str, form_data: PromptForm
    ) -> Optional[PromptModel]:
        """Update a prompt by ID.

        Creates a new history entry for the update. Requires write access.

        Args:
            prompt_id: The unique identifier of the prompt.
            form_data: The updated prompt data.

        Returns:
            Optional[PromptModel]: The updated prompt.
        """
        return await self._request(
            "POST",
            f"/v1/prompts/id/{prompt_id}/update",
            json=form_data.model_dump(),
            model=Optional[PromptModel],
        )

    async def update_prompt_metadata(
        self, prompt_id: str, form_data: PromptMetadataForm
    ) -> Optional[PromptModel]:
        """Update prompt metadata (name, command, tags) without creating history.

        Lightweight update for metadata changes that don't affect content.

        Args:
            prompt_id: The unique identifier of the prompt.
            form_data: The metadata to update.

        Returns:
            Optional[PromptModel]: The updated prompt.
        """
        return await self._request(
            "POST",
            f"/v1/prompts/id/{prompt_id}/update/meta",
            json=form_data.model_dump(),
            model=Optional[PromptModel],
        )

    async def set_prompt_version(
        self, prompt_id: str, form_data: PromptVersionUpdateForm
    ) -> Optional[PromptModel]:
        """Set the active version of a prompt.

        Rolls back to a previous version by specifying its history entry ID.

        Args:
            prompt_id: The unique identifier of the prompt.
            form_data: Contains the version_id to set as active.

        Returns:
            Optional[PromptModel]: The updated prompt.
        """
        return await self._request(
            "POST",
            f"/v1/prompts/id/{prompt_id}/update/version",
            json=form_data.model_dump(),
            model=Optional[PromptModel],
        )

    async def update_prompt_access(
        self, prompt_id: str, form_data: PromptAccessGrantsForm
    ) -> Optional[PromptModel]:
        """Update access grants for a prompt.

        Controls who can read or write the prompt.

        Args:
            prompt_id: The unique identifier of the prompt.
            form_data: The access grants to set.

        Returns:
            Optional[PromptModel]: The updated prompt.
        """
        return await self._request(
            "POST",
            f"/v1/prompts/id/{prompt_id}/access/update",
            json=form_data.model_dump(),
            model=Optional[PromptModel],
        )

    async def delete_prompt_by_command(self, command: str) -> bool:
        """Delete a prompt by its command trigger.

        Resolves the prompt by command then deletes by ID.

        Args:
            command: The command trigger (e.g., '/help' or 'help').

        Returns:
            bool: True if the prompt was found and deleted.
        """
        prompt = await self.get_prompt_by_command(command)
        if prompt is None:
            return False
        return await self.delete_prompt_by_id(prompt.id)

    async def delete_prompt_by_id(self, prompt_id: str) -> bool:
        """Delete a prompt by ID.

        Requires write access to the prompt.

        Args:
            prompt_id: The unique identifier of the prompt.

        Returns:
            bool: True if successful.
        """
        return await self._request(
            "DELETE",
            f"/v1/prompts/id/{prompt_id}/delete",
            model=bool,
        )

    async def toggle_prompt_active(self, prompt_id: str) -> Optional[PromptModel]:
        """Toggle a prompt's active state.

        Args:
            prompt_id: The ID of the prompt to toggle.

        Returns:
            Optional[PromptModel]: The updated `PromptModel` with toggled active state.
        """
        return await self._request(
            "POST",
            f"/v1/prompts/id/{prompt_id}/toggle",
            model=Optional[PromptModel],
        )

    # History endpoints

    async def get_prompt_history(
        self, prompt_id: str, page: int = 0
    ) -> List[PromptHistoryResponse]:
        """Get version history for a prompt.

        Returns paginated history entries ordered by creation time (newest first).

        Args:
            prompt_id: The unique identifier of the prompt.
            page: Page number (0-indexed, default 0).

        Returns:
            List[PromptHistoryResponse]: List of history entries with user info.
        """
        return await self._request(
            "GET",
            f"/v1/prompts/id/{prompt_id}/history",
            params={"page": page},
            model=List[PromptHistoryResponse],
        )

    async def get_prompt_history_entry(
        self, prompt_id: str, history_id: str
    ) -> PromptHistoryModel:
        """Get a specific version from history.

        Args:
            prompt_id: The unique identifier of the prompt.
            history_id: The unique identifier of the history entry.

        Returns:
            `PromptHistoryModel`: The history entry details.
        """
        return await self._request(
            "GET",
            f"/v1/prompts/id/{prompt_id}/history/{history_id}",
            model=PromptHistoryModel,
        )

    async def delete_prompt_history_entry(
        self, prompt_id: str, history_id: str
    ) -> bool:
        """Delete a history entry.

        Cannot delete the active production version. Children are reparented to grandparent.

        Args:
            prompt_id: The unique identifier of the prompt.
            history_id: The unique identifier of the history entry.

        Returns:
            bool: True if successful.
        """
        return await self._request(
            "DELETE",
            f"/v1/prompts/id/{prompt_id}/history/{history_id}",
            model=bool,
        )

    async def get_prompt_diff(
        self, prompt_id: str, from_id: str, to_id: str
    ) -> PromptDiffResponse:
        """Get diff between two prompt versions.

        Computes a unified diff of the content between two history entries.

        Args:
            prompt_id: The unique identifier of the prompt.
            from_id: ID of the source (from) history entry.
            to_id: ID of the target (to) history entry.

        Returns:
            `PromptDiffResponse`: Diff information between the two versions.
        """
        return await self._request(
            "GET",
            f"/v1/prompts/id/{prompt_id}/history/diff",
            params={"from_id": from_id, "to_id": to_id},
            model=PromptDiffResponse,
        )
