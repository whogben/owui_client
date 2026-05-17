"""Calendar models for the Open WebUI scheduling system.

Calendars contain events with optional recurrence (RRULE), attendees with RSVP
status, and access-control grants for sharing. A virtual "Scheduled Tasks"
calendar (`__scheduled_tasks__`) surfaces automation runs as read-only events.
"""

from typing import Optional, Any
from pydantic import BaseModel, ConfigDict, Field


class CalendarModel(BaseModel):
    """A user-owned or shared calendar.

    The virtual Scheduled Tasks calendar has `is_system=True` and a fixed
    id of `__scheduled_tasks__`. All other calendars are user-created.
    """

    id: str
    """Unique identifier (UUID), or `__scheduled_tasks__` for the system calendar."""

    user_id: str
    """ID of the owning user."""

    name: str
    """Display name of the calendar."""

    color: Optional[str] = None
    """CSS color string for the calendar, e.g. `#3b82f6`."""

    is_default: bool = False
    """Whether this is the user's default calendar. Only one default per user."""

    is_system: bool = False
    """True for the virtual Scheduled Tasks calendar, False for user-created."""

    data: Optional[dict[str, Any]] = None
    """Arbitrary calendar data.

    Dict Fields:
        Reserved for future use. No keys are currently read by the backend.
    """

    meta: Optional[dict[str, Any]] = None
    """Arbitrary calendar metadata.

    Dict Fields:
        Reserved for future use. No keys are currently read by the backend.
    """

    access_grants: list[Any] = Field(default_factory=list)
    """List of access grants controlling sharing. Each grant is a dict.

    Dict Fields:
        - `target_type` (str, required): Grant target type, e.g. 'user' or 'group'
        - `target_id` (str, required): ID of the user or group
        - `permission` (str, required): 'read' or 'write'
    """

    created_at: int
    """Timestamp (nanoseconds since epoch) of creation."""

    updated_at: int
    """Timestamp (nanoseconds since epoch) of last update."""

    model_config = ConfigDict(from_attributes=True)


class CalendarEventAttendeeModel(BaseModel):
    """An attendee on a calendar event with RSVP status."""

    id: str
    """Unique identifier (UUID)."""

    event_id: str
    """ID of the parent event."""

    user_id: str
    """ID of the attendee user."""

    status: str = "pending"
    """RSVP status: 'accepted', 'declined', 'tentative', or 'pending'."""

    meta: Optional[dict[str, Any]] = None
    """Arbitrary attendee metadata.

    Dict Fields:
        Reserved for future use. No keys are currently read by the backend.
    """

    created_at: int
    """Timestamp (nanoseconds since epoch) of creation."""

    updated_at: int
    """Timestamp (nanoseconds since epoch) of last update."""

    model_config = ConfigDict(from_attributes=True)


class CalendarEventModel(BaseModel):
    """A calendar event with optional recurrence and attendees.

    Timestamps are nanoseconds since epoch. Recurring events use an RRULE
    string (RFC 5545); the backend expands instances server-side.
    """

    id: str
    """Unique identifier (UUID), or `auto_{id}`/`run_{id}` for virtual events."""

    calendar_id: str
    """ID of the parent calendar, or `__scheduled_tasks__` for virtual events."""

    user_id: str
    """ID of the event creator."""

    title: str
    """Event title."""

    description: Optional[str] = None
    """Event description or notes."""

    start_at: int
    """Start time as nanoseconds since epoch."""

    end_at: Optional[int] = None
    """End time as nanoseconds since epoch. Null for point events."""

    all_day: bool = False
    """Whether this is an all-day event."""

    rrule: Optional[str] = None
    """RRULE recurrence rule (RFC 5545), e.g. `FREQ=DAILY;DTSTART=20260101T090000Z`."""

    color: Optional[str] = None
    """CSS color override for this event, e.g. `#ef4444`."""

    location: Optional[str] = None
    """Event location string."""

    data: Optional[dict[str, Any]] = None
    """Arbitrary event data.

    Dict Fields:
        Reserved for future use. No keys are currently read by the backend.
    """

    meta: Optional[dict[str, Any]] = None
    """Event metadata.

    Dict Fields:
        - `alert_minutes` (int, optional): Minutes before event to send a reminder.
          0 = at time of event, -1 = no reminder. Defaults to 10 if absent.
        - `automation_id` (str, optional): Set on virtual Scheduled Tasks events
          to link back to the source automation.
        - `run_id` (str, optional): Set on virtual past-run events to link to the
          automation run record.
        - `chat_id` (str, optional): Set on virtual past-run events for the
          associated chat.
        - `status` (str, optional): Set on virtual past-run events, 'success' or
          'error'.
    """

    is_cancelled: bool = False
    """Whether the event has been cancelled."""

    attendees: list[CalendarEventAttendeeModel] = Field(default_factory=list)
    """List of event attendees with RSVP status."""

    created_at: int
    """Timestamp (nanoseconds since epoch) of creation."""

    updated_at: int
    """Timestamp (nanoseconds since epoch) of last update."""

    model_config = ConfigDict(from_attributes=True, extra="allow")


class CalendarForm(BaseModel):
    """Form for creating a new calendar."""

    name: str
    """Display name of the calendar."""

    color: Optional[str] = None
    """CSS color string, e.g. `#3b82f6`."""

    data: Optional[dict[str, Any]] = None
    """Arbitrary calendar data.

    Dict Fields:
        Reserved for future use. No keys are currently read by the backend.
    """

    meta: Optional[dict[str, Any]] = None
    """Arbitrary calendar metadata.

    Dict Fields:
        Reserved for future use. No keys are currently read by the backend.
    """

    access_grants: Optional[list[dict[str, Any]]] = None
    """Access grants for sharing the calendar. Each dict defines a grant.

    Dict Fields:
        - `target_type` (str, required): Grant target type, e.g. 'user' or 'group'
        - `target_id` (str, required): ID of the user or group
        - `permission` (str, required): 'read' or 'write'
    """


class CalendarUpdateForm(BaseModel):
    """Form for updating an existing calendar. Only set fields are applied."""

    name: Optional[str] = None
    """New display name."""

    color: Optional[str] = None
    """New CSS color string."""

    data: Optional[dict[str, Any]] = None
    """Merged into existing data. New keys overwrite old ones.

    Dict Fields:
        Reserved for future use. No keys are currently read by the backend.
    """

    meta: Optional[dict[str, Any]] = None
    """Merged into existing metadata. New keys overwrite old ones.

    Dict Fields:
        Reserved for future use. No keys are currently read by the backend.
    """

    access_grants: Optional[list[dict[str, Any]]] = None
    """Replaces all existing access grants. Each dict defines a grant.

    Dict Fields:
        - `target_type` (str, required): Grant target type, e.g. 'user' or 'group'
        - `target_id` (str, required): ID of the user or group
        - `permission` (str, required): 'read' or 'write'
    """


class CalendarEventForm(BaseModel):
    """Form for creating a new calendar event."""

    calendar_id: str
    """ID of the calendar to create the event in."""

    title: str
    """Event title."""

    description: Optional[str] = None
    """Event description or notes."""

    start_at: int
    """Start time as nanoseconds since epoch."""

    end_at: Optional[int] = None
    """End time as nanoseconds since epoch. Null for point events."""

    all_day: bool = False
    """Whether this is an all-day event."""

    rrule: Optional[str] = None
    """RRULE recurrence rule (RFC 5545), e.g. `FREQ=WEEKLY;DTSTART=20260101T090000Z`."""

    color: Optional[str] = None
    """CSS color override for this event."""

    location: Optional[str] = None
    """Event location string."""

    data: Optional[dict[str, Any]] = None
    """Arbitrary event data.

    Dict Fields:
        Reserved for future use. No keys are currently read by the backend.
    """

    meta: Optional[dict[str, Any]] = None
    """Event metadata.

    Dict Fields:
        - `alert_minutes` (int, optional): Minutes before event to send a reminder.
          0 = at time of event, -1 = no reminder. Defaults to 10 if absent.
    """

    attendees: Optional[list[dict[str, Any]]] = None
    """Attendees to add to the event. Each dict defines an attendee.

    Dict Fields:
        - `user_id` (str, required): ID of the attendee user
        - `status` (str, optional): RSVP status, defaults to 'pending'
        - `meta` (dict, optional): Arbitrary attendee metadata
    """


class CalendarEventUpdateForm(BaseModel):
    """Form for updating an existing calendar event. Only set fields are applied."""

    calendar_id: Optional[str] = None
    """Move event to a different calendar."""

    title: Optional[str] = None
    """New event title."""

    description: Optional[str] = None
    """New event description."""

    start_at: Optional[int] = None
    """New start time as nanoseconds since epoch."""

    end_at: Optional[int] = None
    """New end time as nanoseconds since epoch."""

    all_day: Optional[bool] = None
    """Whether this is an all-day event."""

    rrule: Optional[str] = None
    """New RRULE recurrence rule, or null to remove recurrence."""

    color: Optional[str] = None
    """New CSS color override."""

    location: Optional[str] = None
    """New event location."""

    data: Optional[dict[str, Any]] = None
    """Merged into existing data. New keys overwrite old ones.

    Dict Fields:
        Reserved for future use. No keys are currently read by the backend.
    """

    meta: Optional[dict[str, Any]] = None
    """Merged into existing metadata. New keys overwrite old ones.

    Dict Fields:
        - `alert_minutes` (int, optional): Minutes before event to send a reminder.
          0 = at time of event, -1 = no reminder. Defaults to 10 if absent.
    """

    is_cancelled: Optional[bool] = None
    """Set to True to cancel the event."""

    attendees: Optional[list[dict[str, Any]]] = None
    """Replaces all existing attendees. Each dict defines an attendee.

    Dict Fields:
        - `user_id` (str, required): ID of the attendee user
        - `status` (str, optional): RSVP status, defaults to 'pending'
        - `meta` (dict, optional): Arbitrary attendee metadata
    """


class RSVPForm(BaseModel):
    """Form for updating RSVP status on an event."""

    status: str
    """RSVP status: 'accepted', 'declined', 'tentative', or 'pending'."""


class CalendarEventUserResponse(CalendarEventModel):
    """Calendar event enriched with the creator's user profile."""

    user: Optional[Any] = None
    """User profile of the event creator. Structure matches UserResponse."""


class CalendarEventListResponse(BaseModel):
    """Paginated list of calendar events with enriched user data."""

    items: list[CalendarEventUserResponse] = []
    """List of events in the current page."""

    total: int = 0
    """Total number of events matching the query before pagination."""
