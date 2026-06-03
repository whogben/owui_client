from typing import List, Optional

from owui_client.client_base import ResourceBase
from owui_client.models.automations import (
    AutomationResponse,
    AutomationRunModel,
    AutomationForm,
    AutomationListResponse,
)


class AutomationsClient(ResourceBase):
    """
    Client for the Automations endpoints.
    """

    async def get_automation_items(
        self,
        query: Optional[str] = None,
        status: Optional[str] = None,
        page: Optional[int] = 1,
    ) -> AutomationListResponse:
        """Get a paginated, searchable list of automations.

        Returns automations owned by the authenticated user. Each item includes
        the latest run record. Supports filtering by name/prompt text and
        active/paused status.

        Args:
            query: Optional search string to filter by name or prompt content.
            status: Optional status filter: 'active' or 'paused'.
            page: Page number (1-indexed). Defaults to 1.

        Returns:
            `AutomationListResponse`: Paginated automations with run history.
        """
        params = {}
        if query is not None:
            params["query"] = query
        if status is not None:
            params["status"] = status
        if page is not None:
            params["page"] = page

        return await self._request(
            "GET",
            "/v1/automations/list",
            params=params,
            model=AutomationListResponse,
        )

    async def create_new_automation(
        self, form_data: AutomationForm
    ) -> Optional[AutomationResponse]:
        """Create a new automation.

        Validates the RRULE schedule and enforces user automation limits.
        The automation is scheduled for its next run immediately upon creation.

        Args:
            form_data: The automation definition including name, data (prompt,
                model_id, rrule), optional meta, and is_active flag.

        Returns:
            Optional[AutomationResponse]: The created automation with enriched run data.
        """
        return await self._request(
            "POST",
            "/v1/automations/create",
            json=form_data.model_dump(mode="json", exclude_none=True),
            model=Optional[AutomationResponse],
        )

    async def get_automation_by_id(self, id: str) -> Optional[AutomationResponse]:
        """Get a single automation by ID with enriched run data.

        Returns the automation details including the latest run record and
        computed next run timestamps.

        Args:
            id: The automation ID.

        Returns:
            Optional[AutomationResponse]: The automation with run history.
        """
        return await self._request(
            "GET",
            f"/v1/automations/{id}",
            model=Optional[AutomationResponse],
        )

    async def update_automation_by_id(
        self, id: str, form_data: AutomationForm
    ) -> Optional[AutomationResponse]:
        """Update an automation by ID.

        Re-validates the RRULE and re-enforces rate limits. The schedule is
        recalculated based on the new RRULE.

        Args:
            id: The automation ID.
            form_data: The updated automation definition.

        Returns:
            Optional[AutomationResponse]: The updated automation with enriched run data.
        """
        return await self._request(
            "POST",
            f"/v1/automations/{id}/update",
            json=form_data.model_dump(mode="json", exclude_none=True),
            model=Optional[AutomationResponse],
        )

    async def toggle_automation_by_id(
        self, id: str
    ) -> Optional[AutomationResponse]:
        """Toggle an automation's active state.

        Flips the `is_active` flag. Paused automations are excluded from
        scheduling. When reactivated, the next run is recalculated from the
        RRULE.

        Args:
            id: The automation ID.

        Returns:
            Optional[AutomationResponse]: The toggled automation with enriched run data.
        """
        return await self._request(
            "POST",
            f"/v1/automations/{id}/toggle",
            model=Optional[AutomationResponse],
        )

    async def run_automation_by_id(
        self, id: str
    ) -> Optional[AutomationResponse]:
        """Trigger an immediate execution of an automation.

        The automation runs asynchronously in the background. This endpoint
        returns the current automation state immediately, not the run result.

        Args:
            id: The automation ID.

        Returns:
            Optional[AutomationResponse]: The automation state at trigger time.
        """
        return await self._request(
            "POST",
            f"/v1/automations/{id}/run",
            model=Optional[AutomationResponse],
        )

    async def delete_automation_by_id(self, id: str) -> bool:
        """Delete an automation and all its run history by ID.

        Permanently removes the automation and all associated run records.

        Args:
            id: The automation ID.

        Returns:
            bool: True if deletion succeeded.
        """
        return await self._request(
            "DELETE",
            f"/v1/automations/{id}/delete",
            model=bool,
        )

    async def get_automation_runs(
        self,
        id: str,
        skip: int = 0,
        limit: int = 50,
    ) -> List[AutomationRunModel]:
        """Get run history for an automation.

        Returns execution records ordered by creation time descending (most
        recent first).

        Args:
            id: The automation ID.
            skip: Number of records to skip. Defaults to 0.
            limit: Maximum number of records to return. Defaults to 50.

        Returns:
            List[AutomationRunModel]: List of run records.
        """
        return await self._request(
            "GET",
            f"/v1/automations/{id}/runs",
            params={"skip": skip, "limit": limit},
            model=List[AutomationRunModel],
        )
