from typing import Optional
from owui_client.client_base import ResourceBase
from owui_client.models.automations import (
    AutomationForm,
    AutomationModel,
    AutomationResponse,
    AutomationRunModel,
    AutomationListResponse,
)


class AutomationsClient(ResourceBase):
    """
    Client for the Automations endpoints.

    This client manages scheduled automations that perform recurring
    chat completions based on an RRULE schedule.
    """

    async def list_automations(
        self,
        query: Optional[str] = None,
        status: Optional[str] = None,
        page: Optional[int] = 1,
    ) -> AutomationListResponse:
        """List automations with optional filtering and pagination.

        Retrieves a paginated list of the user's automations, optionally
        filtered by query string and status.

        Args:
            query: Optional search string to filter by automation name or prompt.
            status: Optional status filter. Use 'active' or 'paused'.
            page: Page number for pagination. Defaults to 1.

        Returns:
            `AutomationListResponse`: Paginated list of automations.
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
            model=AutomationListResponse,
            params=params,
        )

    async def create_automation(self, form_data: AutomationForm) -> AutomationResponse:
        """Create a new automation.

        Creates a scheduled automation that will execute chat completions
        according to the provided RRULE schedule.

        Args:
            form_data: The automation configuration including name, data, and schedule.

        Returns:
            `AutomationResponse`: The created automation with computed fields.
        """
        return await self._request(
            "POST",
            "/v1/automations/create",
            model=AutomationResponse,
            json=form_data.model_dump(),
        )

    async def get_automation(self, id: str) -> AutomationResponse:
        """Get an automation by ID.

        Retrieves a single automation including its latest run and upcoming
        schedule information.

        Args:
            id: The automation identifier.

        Returns:
            `AutomationResponse`: The automation details.
        """
        return await self._request(
            "GET",
            f"/v1/automations/{id}",
            model=AutomationResponse,
        )

    async def update_automation(
        self, id: str, form_data: AutomationForm
    ) -> AutomationResponse:
        """Update an existing automation.

        Replaces the automation's configuration with the provided form data.

        Args:
            id: The automation identifier.
            form_data: The updated automation configuration.

        Returns:
            `AutomationResponse`: The updated automation.
        """
        return await self._request(
            "POST",
            f"/v1/automations/{id}/update",
            model=AutomationResponse,
            json=form_data.model_dump(),
        )

    async def toggle_automation(self, id: str) -> AutomationResponse:
        """Toggle an automation's active state.

        Activates a paused automation or pauses an active one.

        Args:
            id: The automation identifier.

        Returns:
            `AutomationResponse`: The automation with its new active state.
        """
        return await self._request(
            "POST",
            f"/v1/automations/{id}/toggle",
            model=AutomationResponse,
        )

    async def run_automation(self, id: str) -> AutomationResponse:
        """Trigger an automation to run immediately.

        Creates a background task to execute the automation and returns
        the automation details. The execution happens asynchronously.

        Args:
            id: The automation identifier.

        Returns:
            `AutomationResponse`: The automation details.
        """
        return await self._request(
            "POST",
            f"/v1/automations/{id}/run",
            model=AutomationResponse,
        )

    async def delete_automation(self, id: str) -> bool:
        """Delete an automation.

        Removes the automation and all associated run history.

        Args:
            id: The automation identifier.

        Returns:
            bool: True if the automation was deleted successfully.
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
    ) -> list[AutomationRunModel]:
        """Get the execution history for an automation.

        Retrieves a paginated list of run records for the given automation.

        Args:
            id: The automation identifier.
            skip: Number of records to skip for pagination. Defaults to 0.
            limit: Maximum number of records to return. Defaults to 50.

        Returns:
            list[`AutomationRunModel`]: The automation run history.
        """
        return await self._request(
            "GET",
            f"/v1/automations/{id}/runs",
            model=list[AutomationRunModel],
            params={"skip": skip, "limit": limit},
        )
