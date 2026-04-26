"""Calendar models for the Open WebUI API.

This module provides Pydantic models for calendars, calendar events, attendees,
and related forms and responses.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from owui_client.models.users import UserResponse
from owui_client.models.access_grants import AccessGrantModel


class CalendarModel(BaseModel):
    """A calendar owned by or shared with a user.

    Calendars group events and control their visibility through access grants.
    The backend automatically creates a 'Personal' default calendar if none exist.
    A virtual 'Scheduled Tasks' calendar may also appear when automations are enabled.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    """Unique identifier for the calendar."""

    user_id: str
    """ID of the user who owns the calendar."""

    name: str
    """Display name of the calendar."""

    color: Optional[str] = None
    """Hex color code for the calendar (e.g., '#3b82f6')."""

    is_default: bool = False
    """Whether this is the user's default calendar."""

    is_system: bool = False
    """Whether this is a system calendar (e.g., Scheduled Tasks). System calendars cannot be deleted."""

    data: Optional[dict] = None
    """Custom data associated with the calendar.

    Dict Fields:
        This dictionary accepts arbitrary key-value pairs for extensibility.
        No specific keys are enforced by the backend.
    """

    meta: Optional[dict] = None
    """Metadata associated with the calendar.

    Dict Fields:
        This dictionary accepts arbitrary key-value pairs for extensibility.
        No specific keys are enforced by the backend.
    """

    access_grants: list[AccessGrantModel] = Field(default_factory=list)
    """List of access grants controlling who can read or write this calendar."""

    created_at: int
    """Timestamp when the calendar was created (epoch nanoseconds)."""

    updated_at: int
    """Timestamp when the calendar was last updated (epoch nanoseconds)."""


class CalendarEventAttendeeModel(BaseModel):
    """An attendee of a calendar event."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    """Unique identifier for the attendee record."""

    event_id: str
    """ID of the event this attendee belongs to."""

    user_id: str
    """ID of the attending user."""

    status: str = "pending"
    """RSVP status. Valid values: 'accepted', 'declined', 'tentative', 'pending'."""

    meta: Optional[dict] = None
    """Metadata associated with the attendee.

    Dict Fields:
        This dictionary accepts arbitrary key-value pairs for extensibility.
        No specific keys are enforced by the backend.
    """

    created_at: int
    """Timestamp when the attendee record was created (epoch nanoseconds)."""

    updated_at: int
    """Timestamp when the attendee record was last updated (epoch nanoseconds)."""


class CalendarEventModel(BaseModel):
    """A calendar event.

    Events support recurring instances via RRULE strings. When querying events,
    the backend expands recurring events into individual instances within the
    requested date range.
    """

    model_config = ConfigDict(from_attributes=True, extra="allow")

    id: str
    """Unique identifier for the event."""

    calendar_id: str
    """ID of the calendar this event belongs to."""

    user_id: str
    """ID of the user who created the event."""

    title: str
    """Title of the event."""

    description: Optional[str] = None
    """Description or notes for the event."""

    start_at: int
    """Start time in epoch nanoseconds."""

    end_at: Optional[int] = None
    """End time in epoch nanoseconds. None for open-ended events."""

    all_day: bool = False
    """Whether this is an all-day event."""

    rrule: Optional[str] = None
    """Recurrence rule in iCalendar RRULE format (e.g., 'FREQ=DAILY;COUNT=5').

    When present, the backend expands this event into recurring instances.
    """

    color: Optional[str] = None
    """Hex color code for this event (overrides calendar color)."""

    location: Optional[str] = None
    """Location of the event."""

    data: Optional[dict] = None
    """Custom data associated with the event.

    Dict Fields:
        This dictionary accepts arbitrary key-value pairs for extensibility.
        No specific keys are enforced by the backend.
    """

    meta: Optional[dict] = None
    """Metadata associated with the event.

    Dict Fields:
        - `alert_minutes` (int, optional): Minutes before the event to trigger an alert.
            Negative values mean "no alert". If absent, a default lookahead is used.
        - Additional keys may exist for extensibility.
    """

    is_cancelled: bool = False
    """Whether the event has been cancelled."""

    attendees: list[CalendarEventAttendeeModel] = Field(default_factory=list)
    """List of attendees for this event."""

    created_at: int
    """Timestamp when the event was created (epoch nanoseconds)."""

    updated_at: int
    """Timestamp when the event was last updated (epoch nanoseconds)."""


class CalendarForm(BaseModel):
    """Form data for creating a new calendar."""

    name: str
    """Display name for the new calendar."""

    color: Optional[str] = None
    """Hex color code (e.g., '#3b82f6')."""

    data: Optional[dict] = None
    """Custom data for the calendar.

    Dict Fields:
        This dictionary accepts arbitrary key-value pairs for extensibility.
        No specific keys are enforced by the backend.
    """

    meta: Optional[dict] = None
    """Metadata for the calendar.

    Dict Fields:
        This dictionary accepts arbitrary key-value pairs for extensibility.
        No specific keys are enforced by the backend.
    """

    access_grants: Optional[list[dict]] = None
    """Initial access grants for the calendar.

    Dict Fields:
        - `id` (str, optional): Unique identifier for the grant.
        - `principal_type` (str, required): 'user' or 'group'.
        - `principal_id` (str, required): User/group ID, or '*' for public access.
        - `permission` (str, required): 'read' or 'write'.
    """


class CalendarUpdateForm(BaseModel):
    """Form data for updating an existing calendar."""

    name: Optional[str] = None
    """New display name for the calendar."""

    color: Optional[str] = None
    """New hex color code."""

    data: Optional[dict] = None
    """Custom data to merge into existing data.

    Dict Fields:
        This dictionary accepts arbitrary key-value pairs for extensibility.
        When updating, the backend performs a shallow merge with existing data.
    """

    meta: Optional[dict] = None
    """Metadata to merge into existing meta.

    Dict Fields:
        This dictionary accepts arbitrary key-value pairs for extensibility.
        When updating, the backend performs a shallow merge with existing meta.
    """

    access_grants: Optional[list[dict]] = None
    """Replacement access grants for the calendar.

    Dict Fields:
        - `id` (str, optional): Unique identifier for the grant.
        - `principal_type` (str, required): 'user' or 'group'.
        - `principal_id` (str, required): User/group ID, or '*' for public access.
        - `permission` (str, required): 'read' or 'write'.
    """


class CalendarEventForm(BaseModel):
    """Form data for creating a new calendar event."""

    calendar_id: str
    """ID of the calendar to create the event in."""

    title: str
    """Title of the event."""

    description: Optional[str] = None
    """Description or notes for the event."""

    start_at: int
    """Start time in epoch nanoseconds."""

    end_at: Optional[int] = None
    """End time in epoch nanoseconds."""

    all_day: bool = False
    """Whether this is an all-day event."""

    rrule: Optional[str] = None
    """Recurrence rule in iCalendar RRULE format."""

    color: Optional[str] = None
    """Hex color code for this event."""

    location: Optional[str] = None
    """Location of the event."""

    data: Optional[dict] = None
    """Custom data for the event.

    Dict Fields:
        This dictionary accepts arbitrary key-value pairs for extensibility.
        No specific keys are enforced by the backend.
    """

    meta: Optional[dict] = None
    """Metadata for the event.

    Dict Fields:
        - `alert_minutes` (int, optional): Minutes before the event to trigger an alert.
        - Additional keys may exist for extensibility.
    """

    attendees: Optional[list[dict]] = None
    """Initial attendees for the event.

    Dict Fields:
        - `user_id` (str, required): ID of the user to invite.
        - `status` (str, optional): Initial RSVP status ('pending', 'accepted', 'declined', 'tentative').
        - `meta` (dict, optional): Attendee-specific metadata.
    """


class CalendarEventUpdateForm(BaseModel):
    """Form data for updating an existing calendar event."""

    calendar_id: Optional[str] = None
    """New calendar ID to move the event to."""

    title: Optional[str] = None
    """New title for the event."""

    description: Optional[str] = None
    """New description for the event."""

    start_at: Optional[int] = None
    """New start time in epoch nanoseconds."""

    end_at: Optional[int] = None
    """New end time in epoch nanoseconds."""

    all_day: Optional[bool] = None
    """Whether this is an all-day event."""

    rrule: Optional[str] = None
    """New recurrence rule. Set to null to remove recurrence."""

    color: Optional[str] = None
    """New hex color code."""

    location: Optional[str] = None
    """New location for the event."""

    data: Optional[dict] = None
    """Custom data to merge into existing data.

    Dict Fields:
        This dictionary accepts arbitrary key-value pairs for extensibility.
        When updating, the backend performs a shallow merge with existing data.
    """

    meta: Optional[dict] = None
    """Metadata to merge into existing meta.

    Dict Fields:
        - `alert_minutes` (int, optional): Minutes before the event to trigger an alert.
        - Additional keys may exist for extensibility.
    """

    is_cancelled: Optional[bool] = None
    """Set to True to cancel the event."""

    attendees: Optional[list[dict]] = None
    """Replacement list of attendees for the event.

    Dict Fields:
        - `user_id` (str, required): ID of the user to invite.
        - `status` (str, optional): RSVP status ('pending', 'accepted', 'declined', 'tentative').
        - `meta` (dict, optional): Attendee-specific metadata.
    """


class RSVPForm(BaseModel):
    """Form data for updating RSVP status for an event."""

    status: str
    """RSVP status. Must be one of: 'accepted', 'declined', 'tentative', 'pending'."""


class CalendarEventUserResponse(CalendarEventModel):
    """Calendar event with embedded user information.

    Returned by event listing endpoints. Includes the creator's user details.
    For recurring events, extra fields such as `instance_id` may be present
    when the backend expands an RRULE into individual instances.
    """

    user: Optional[UserResponse] = None
    """The user who created the event."""


class CalendarEventListResponse(BaseModel):
    """Paginated response for event search results."""

    items: list[CalendarEventUserResponse]
    """List of events matching the search criteria."""

    total: int
    """Total number of matching events."""
