import time
import pytest
from owui_client.models.calendar import (
    CalendarForm,
    CalendarUpdateForm,
    CalendarEventForm,
    CalendarEventUpdateForm,
)

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio


def _ns_now() -> int:
    """Current time in nanoseconds (ms precision)."""
    return int(time.time() * 1000) * 1_000_000


def _ns_future(hours: int) -> int:
    """Nanoseconds `hours` from now."""
    return _ns_now() + hours * 3_600_000_000_000


async def test_calendar_client_initialization(client):
    assert client.calendar is not None


async def test_calendar_lifecycle(client):
    """Test create, get, list, update, set-default, delete calendar."""
    # 1. List calendars (auto-creates default "Personal" calendar)
    calendars = await client.calendar.get_calendars()
    assert isinstance(calendars, list)
    assert len(calendars) >= 1
    default_cal = next((c for c in calendars if c.is_default), None)
    assert default_cal is not None

    # 2. Create a second calendar
    form = CalendarForm(name="Test Calendar", color="#ef4444")
    created = await client.calendar.create_calendar(form)
    assert created is not None
    assert created.name == "Test Calendar"
    assert created.color == "#ef4444"
    cal_id = created.id

    # 3. Get calendar by ID
    fetched = await client.calendar.get_calendar_by_id(cal_id)
    assert fetched is not None
    assert fetched.id == cal_id
    assert fetched.name == "Test Calendar"

    # 4. Update calendar
    update_form = CalendarUpdateForm(name="Updated Calendar", color="#22c55e")
    updated = await client.calendar.update_calendar(cal_id, update_form)
    assert updated is not None
    assert updated.name == "Updated Calendar"
    assert updated.color == "#22c55e"

    # 5. Delete the non-default calendar
    deleted = await client.calendar.delete_calendar(cal_id)
    assert deleted is True

    # 6. Verify deletion
    try:
        await client.calendar.get_calendar_by_id(cal_id)
        assert False, "Should have raised exception"
    except Exception:
        pass

    # 7. Set default calendar (use the original default)
    default_result = await client.calendar.set_default_calendar(default_cal.id)
    assert default_result is not None
    assert default_result.is_default is True


async def test_event_lifecycle(client):
    """Test create, get, search, update, delete event."""
    # Get or create a calendar
    calendars = await client.calendar.get_calendars()
    cal = next((c for c in calendars if not c.is_system), None)
    assert cal is not None
    cal_id = cal.id

    # 1. Create event
    start = _ns_future(1)
    end = _ns_future(2)
    event_form = CalendarEventForm(
        calendar_id=cal_id,
        title="Test Event",
        description="A test event",
        start_at=start,
        end_at=end,
        location="Test Location",
        meta={"alert_minutes": 15},
    )
    created = await client.calendar.create_event(event_form)
    assert created is not None
    assert created.title == "Test Event"
    assert created.calendar_id == cal_id
    event_id = created.id

    # 2. Get event by ID
    fetched = await client.calendar.get_event_by_id(event_id)
    assert fetched is not None
    assert fetched.id == event_id
    assert fetched.title == "Test Event"

    # 3. Search events
    results = await client.calendar.search_events(query="Test Event")
    assert results.total >= 1
    found = next((e for e in results.items if e.id == event_id), None)
    assert found is not None

    # 4. Update event
    update_form = CalendarEventUpdateForm(
        title="Updated Event",
        location="New Location",
    )
    updated = await client.calendar.update_event(event_id, update_form)
    assert updated is not None
    assert updated.title == "Updated Event"
    assert updated.location == "New Location"

    # 5. Delete event
    deleted = await client.calendar.delete_event(event_id)
    assert deleted is True

    # 6. Verify deletion
    try:
        await client.calendar.get_event_by_id(event_id)
        assert False, "Should have raised exception"
    except Exception:
        pass


async def test_get_events_range(client):
    """Test fetching events by date range."""
    calendars = await client.calendar.get_calendars()
    cal = next((c for c in calendars if not c.is_system), None)
    assert cal is not None

    # Create an event in the near future
    start = _ns_future(1)
    end = _ns_future(2)
    form = CalendarEventForm(
        calendar_id=cal.id,
        title="Range Test Event",
        start_at=start,
        end_at=end,
    )
    created = await client.calendar.create_event(form)
    assert created is not None

    # Query with a wide range using ISO 8601 strings
    from datetime import datetime, timezone, timedelta

    range_start = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(
        timespec="seconds"
    )
    range_end = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat(
        timespec="seconds"
    )
    events = await client.calendar.get_events(
        start=range_start,
        end=range_end,
    )
    assert isinstance(events, list)
    found = next((e for e in events if e.id == created.id), None)
    assert found is not None

    # Clean up
    await client.calendar.delete_event(created.id)


async def test_rsvp_event(client):
    """Test RSVP on an event with attendees."""
    calendars = await client.calendar.get_calendars()
    cal = next((c for c in calendars if not c.is_system), None)
    assert cal is not None

    # Create event with the current user as attendee
    start = _ns_future(3)
    end = _ns_future(4)
    form = CalendarEventForm(
        calendar_id=cal.id,
        title="RSVP Test Event",
        start_at=start,
        end_at=end,
        attendees=[{"user_id": cal.user_id, "status": "pending"}],
    )
    created = await client.calendar.create_event(form)
    assert created is not None
    assert len(created.attendees) >= 1

    # RSVP
    result = await client.calendar.rsvp_event(created.id, "accepted")
    assert result.get("status") is True
    assert result.get("rsvp") == "accepted"

    # Clean up
    await client.calendar.delete_event(created.id)


async def test_search_events_pagination(client):
    """Test search with skip/limit pagination."""
    results = await client.calendar.search_events(skip=0, limit=5)
    assert isinstance(results.total, int)
    assert len(results.items) <= 5


async def test_cannot_delete_default_calendar(client):
    """Verify the default calendar cannot be deleted."""
    calendars = await client.calendar.get_calendars()
    default = next((c for c in calendars if c.is_default and not c.is_system), None)
    if default is None:
        pytest.skip("No default calendar found")

    try:
        await client.calendar.delete_calendar(default.id)
        assert False, "Should have raised exception"
    except Exception:
        pass
