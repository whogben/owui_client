from typing import Optional, List
from owui_client.client_base import ResourceBase
from owui_client.models.calendar import (
    CalendarModel,
    CalendarEventModel,
    CalendarForm,
    CalendarUpdateForm,
    CalendarEventForm,
    CalendarEventUpdateForm,
    CalendarEventUserResponse,
    CalendarEventListResponse,
    RSVPForm,
)


class CalendarClient(ResourceBase):
    """
    Client for the Calendar endpoints.

    This client handles calendar and event CRUD operations, including
    creating calendars, managing events, setting RSVP status, and searching events.
    """

    async def get_calendars(self) -> List[CalendarModel]:
        """List calendars visible to the current user.

        Returns owned calendars, shared calendars, and a virtual 'Scheduled Tasks'
        calendar when automations are available.

        Returns:
            A list of `CalendarModel` objects.
        """
        return await self._request(
            "GET",
            "/v1/calendars/",
            model=CalendarModel,
        )

    async def create_calendar(self, form_data: CalendarForm) -> CalendarModel:
        """Create a new user calendar.

        Args:
            form_data: The data for the new calendar.

        Returns:
            The created `CalendarModel`.
        """
        return await self._request(
            "POST",
            "/v1/calendars/create",
            model=CalendarModel,
            json=form_data.model_dump(),
        )

    async def get_events(
        self,
        start: str,
        end: str,
        calendar_ids: Optional[List[str]] = None,
    ) -> List[CalendarEventUserResponse]:
        """Get events in a date range.

        Includes stored events from the database and expands recurring events.
        May also include virtual automation events when the 'Scheduled Tasks'
        calendar is selected and automations are enabled.

        Args:
            start: ISO 8601 datetime string (e.g., '2026-04-01T00:00:00').
            end: ISO 8601 datetime string (e.g., '2026-05-01T00:00:00').
            calendar_ids: Optional list of calendar IDs to filter by.

        Returns:
            A list of `CalendarEventUserResponse` objects.
        """
        params = {
            "start": start,
            "end": end,
        }
        if calendar_ids:
            params["calendar_ids"] = ",".join(calendar_ids)

        return await self._request(
            "GET",
            "/v1/calendars/events",
            model=list[CalendarEventUserResponse],
            params=params,
        )

    async def create_event(self, form_data: CalendarEventForm) -> CalendarEventModel:
        """Create a new calendar event.

        Args:
            form_data: The data for the new event.

        Returns:
            The created `CalendarEventModel`.
        """
        return await self._request(
            "POST",
            "/v1/calendars/events/create",
            model=CalendarEventModel,
            json=form_data.model_dump(),
        )

    async def search_events(
        self,
        query: Optional[str] = None,
        skip: int = 0,
        limit: int = 30,
    ) -> CalendarEventListResponse:
        """Search for calendar events.

        Args:
            query: Search query string to filter by title, description, or location.
            skip: Number of results to skip for pagination.
            limit: Maximum number of results to return.

        Returns:
            `CalendarEventListResponse` containing matching events and total count.
        """
        params = {
            "skip": skip,
            "limit": limit,
        }
        if query is not None:
            params["query"] = query

        return await self._request(
            "GET",
            "/v1/calendars/events/search",
            model=CalendarEventListResponse,
            params=params,
        )

    async def get_event(self, event_id: str) -> CalendarEventModel:
        """Get a specific event by its ID.

        Args:
            event_id: The unique identifier of the event.

        Returns:
            The requested `CalendarEventModel`.
        """
        return await self._request(
            "GET",
            f"/v1/calendars/events/{event_id}",
            model=CalendarEventModel,
        )

    async def update_event(
        self,
        event_id: str,
        form_data: CalendarEventUpdateForm,
    ) -> CalendarEventModel:
        """Update an existing calendar event.

        Args:
            event_id: The unique identifier of the event to update.
            form_data: The updated event data.

        Returns:
            The updated `CalendarEventModel`.
        """
        return await self._request(
            "POST",
            f"/v1/calendars/events/{event_id}/update",
            model=CalendarEventModel,
            json=form_data.model_dump(exclude_unset=True),
        )

    async def delete_event(self, event_id: str) -> bool:
        """Delete a calendar event.

        Args:
            event_id: The unique identifier of the event to delete.

        Returns:
            True if deletion was successful.
        """
        return await self._request(
            "DELETE",
            f"/v1/calendars/events/{event_id}/delete",
            model=bool,
        )

    async def rsvp_event(self, event_id: str, form_data: RSVPForm) -> dict:
        """Update the current user's RSVP status for an event.

        Args:
            event_id: The unique identifier of the event.
            form_data: The RSVP form containing the desired status.

        Returns:
            A dictionary with 'status' (bool) and 'rsvp' (str) keys.
        """
        return await self._request(
            "POST",
            f"/v1/calendars/events/{event_id}/rsvp",
            model=dict,
            json=form_data.model_dump(),
        )

    async def get_calendar_by_id(self, calendar_id: str) -> CalendarModel:
        """Get a specific calendar by its ID.

        Args:
            calendar_id: The unique identifier of the calendar.

        Returns:
            The requested `CalendarModel`.
        """
        return await self._request(
            "GET",
            f"/v1/calendars/{calendar_id}",
            model=CalendarModel,
        )

    async def update_calendar(
        self,
        calendar_id: str,
        form_data: CalendarUpdateForm,
    ) -> CalendarModel:
        """Update an existing calendar.

        Args:
            calendar_id: The unique identifier of the calendar to update.
            form_data: The updated calendar data.

        Returns:
            The updated `CalendarModel`.
        """
        return await self._request(
            "POST",
            f"/v1/calendars/{calendar_id}/update",
            model=CalendarModel,
            json=form_data.model_dump(exclude_unset=True),
        )

    async def delete_calendar(self, calendar_id: str) -> bool:
        """Delete a calendar.

        System calendars and the default calendar cannot be deleted.

        Args:
            calendar_id: The unique identifier of the calendar to delete.

        Returns:
            True if deletion was successful.
        """
        return await self._request(
            "DELETE",
            f"/v1/calendars/{calendar_id}/delete",
            model=bool,
        )

    async def set_default_calendar(self, calendar_id: str) -> CalendarModel:
        """Set a calendar as the user's default.

        This clears the default flag from all other calendars owned by the user.

        Args:
            calendar_id: The unique identifier of the calendar to set as default.

        Returns:
            The updated `CalendarModel`.
        """
        return await self._request(
            "POST",
            f"/v1/calendars/{calendar_id}/default",
            model=CalendarModel,
        )
