from typing import List, Optional

from owui_client.client_base import ResourceBase
from owui_client.models.calendar import (
    CalendarModel,
    CalendarEventModel,
    CalendarEventUserResponse,
    CalendarEventListResponse,
    CalendarForm,
    CalendarUpdateForm,
    CalendarEventForm,
    CalendarEventUpdateForm,
    RSVPForm,
)


class CalendarClient(ResourceBase):
    """
    Client for the Calendar endpoints.
    """

    def _get_url(self, path: str) -> str:
        # File stem is 'calendar' but API uses plural 'calendars'
        return path.replace("/calendar", "/v1/calendars")

    async def get_calendars(self) -> List[CalendarModel]:
        """List the authenticated user's calendars (owned + shared).

        Includes a virtual "Scheduled Tasks" calendar when the automations
        feature is available to the user.

        Returns:
            List[CalendarModel]: All accessible calendars.
        """
        # Using _get_url("/calendar/") to match drift script heuristic
        return await self._request(
            "GET",
            self._get_url("/calendar/"),
            model=List[CalendarModel],
        )

    async def create_calendar(self, form_data: CalendarForm) -> Optional[CalendarModel]:
        """Create a new user calendar.

        Public access grants are filtered by the server based on the user's
        sharing permissions.

        Args:
            form_data: Calendar definition with name, optional color, and
                optional access grants.

        Returns:
            Optional[CalendarModel]: The created calendar.
        """
        return await self._request(
            "POST",
            "/v1/calendars/create",
            json=form_data.model_dump(mode="json", exclude_none=True),
            model=Optional[CalendarModel],
        )

    async def get_calendar_by_id(self, calendar_id: str) -> Optional[CalendarModel]:
        """Get a single calendar by ID.

        Requires read access to the calendar.

        Args:
            calendar_id: The calendar ID.

        Returns:
            Optional[CalendarModel]: The calendar if found and accessible.
        """
        return await self._request(
            "GET",
            f"/v1/calendars/{calendar_id}",
            model=Optional[CalendarModel],
        )

    async def update_calendar(
        self, calendar_id: str, form_data: CalendarUpdateForm
    ) -> Optional[CalendarModel]:
        """Update a calendar by ID.

        Only the owner or admin can modify access grants. The `data` and
        `meta` dicts are merged (new keys overwrite existing ones).

        Args:
            calendar_id: The calendar ID.
            form_data: Fields to update. Only set fields are applied.

        Returns:
            Optional[CalendarModel]: The updated calendar.
        """
        return await self._request(
            "POST",
            f"/v1/calendars/{calendar_id}/update",
            json=form_data.model_dump(mode="json", exclude_none=True),
            model=Optional[CalendarModel],
        )

    async def delete_calendar(self, calendar_id: str) -> bool:
        """Delete a non-default, non-system calendar.

        Cascades to events, attendees, and access grants. Only the owner
        or admin can delete. Default and system calendars cannot be deleted.

        Args:
            calendar_id: The calendar ID.

        Returns:
            bool: True if deletion succeeded.
        """
        return await self._request(
            "DELETE",
            f"/v1/calendars/{calendar_id}/delete",
            model=bool,
        )

    async def set_default_calendar(self, calendar_id: str) -> Optional[CalendarModel]:
        """Set a calendar as the user's default.

        Clears the default flag from all other user calendars and sets it
        on the specified one.

        Args:
            calendar_id: The calendar ID to make default.

        Returns:
            Optional[CalendarModel]: The updated calendar.
        """
        return await self._request(
            "POST",
            f"/v1/calendars/{calendar_id}/default",
            model=Optional[CalendarModel],
        )

    async def get_events(
        self,
        start: str,
        end: str,
        calendar_ids: Optional[List[str]] = None,
    ) -> List[CalendarEventUserResponse]:
        """Get events in a date range, with recurring-event expansion.

        Returns stored events from accessible calendars plus virtual
        "Scheduled Tasks" events from active automations. Recurring events
        are expanded into individual instances.

        Args:
            start: ISO 8601 datetime string for range start, e.g.
                `2026-04-01T00:00:00`.
            end: ISO 8601 datetime string for range end, e.g.
                `2026-05-01T00:00:00`.
            calendar_ids: Optional list of calendar IDs to filter by.

        Returns:
            List[CalendarEventUserResponse]: Expanded events in the range.
        """
        params = {"start": start, "end": end}
        if calendar_ids is not None:
            params["calendar_ids"] = ",".join(calendar_ids)

        return await self._request(
            "GET",
            "/v1/calendars/events",
            params=params,
            model=List[CalendarEventUserResponse],
        )

    async def create_event(
        self, form_data: CalendarEventForm
    ) -> Optional[CalendarEventModel]:
        """Create a new calendar event.

        Requires write access to the target calendar.

        Args:
            form_data: Event definition with calendar_id, title, start_at,
                and optional fields.

        Returns:
            Optional[CalendarEventModel]: The created event with attendees.
        """
        return await self._request(
            "POST",
            "/v1/calendars/events/create",
            json=form_data.model_dump(mode="json", exclude_none=True),
            model=Optional[CalendarEventModel],
        )

    async def search_events(
        self,
        query: Optional[str] = None,
        skip: int = 0,
        limit: int = 30,
    ) -> CalendarEventListResponse:
        """Search calendar events by text.

        Searches title, description, and location fields across all
        accessible calendars.

        Args:
            query: Optional search string.
            skip: Number of results to skip. Defaults to 0.
            limit: Maximum results to return. Defaults to 30.

        Returns:
            `CalendarEventListResponse`: Paginated matching events.
        """
        params = {"skip": skip, "limit": limit}
        if query is not None:
            params["query"] = query

        return await self._request(
            "GET",
            "/v1/calendars/events/search",
            params=params,
            model=CalendarEventListResponse,
        )

    async def get_event_by_id(self, event_id: str) -> Optional[CalendarEventModel]:
        """Get a single event by ID.

        Requires read access to the event's calendar.

        Args:
            event_id: The event ID.

        Returns:
            Optional[CalendarEventModel]: The event if found and accessible.
        """
        return await self._request(
            "GET",
            f"/v1/calendars/events/{event_id}",
            model=Optional[CalendarEventModel],
        )

    async def update_event(
        self, event_id: str, form_data: CalendarEventUpdateForm
    ) -> Optional[CalendarEventModel]:
        """Update an event by ID.

        Requires write access to the event's calendar. The `data` and
        `meta` dicts are merged (new keys overwrite existing ones).

        Args:
            event_id: The event ID.
            form_data: Fields to update. Only set fields are applied.

        Returns:
            Optional[CalendarEventModel]: The updated event.
        """
        return await self._request(
            "POST",
            f"/v1/calendars/events/{event_id}/update",
            json=form_data.model_dump(mode="json", exclude_none=True),
            model=Optional[CalendarEventModel],
        )

    async def delete_event(self, event_id: str) -> bool:
        """Delete an event and its attendees.

        Requires write access to the event's calendar.

        Args:
            event_id: The event ID.

        Returns:
            bool: True if deletion succeeded.
        """
        return await self._request(
            "DELETE",
            f"/v1/calendars/events/{event_id}/delete",
            model=bool,
        )

    async def rsvp_event(self, event_id: str, status: str) -> dict:
        """Update the authenticated user's RSVP status for an event.

        The user must be an attendee of the event.

        Args:
            event_id: The event ID.
            status: RSVP status: 'accepted', 'declined', 'tentative',
                or 'pending'.

        Returns:
            dict: `{'status': True, 'rsvp': '<status>'}` on success.
        """
        form = RSVPForm(status=status)
        return await self._request(
            "POST",
            f"/v1/calendars/events/{event_id}/rsvp",
            json=form.model_dump(mode="json", exclude_none=True),
            model=dict,
        )
