import pytest
from owui_client.models.calendar import (
    CalendarForm,
    CalendarUpdateForm,
    CalendarEventForm,
    CalendarEventUpdateForm,
    RSVPForm,
    CalendarModel,
)

pytestmark = pytest.mark.asyncio


async def test_calendar_lifecycle(client):
    """Test calendar CRUD: create, list, get, update."""
    admin_config = await client.auths.get_admin_config()
    if not admin_config.ENABLE_CALENDAR:
        admin_config.ENABLE_CALENDAR = True
        await client.auths.update_admin_config(admin_config)

    form = CalendarForm(name="Test Calendar", color="#ff0000")
    created = await client.calendar.create_calendar(form)
    assert created is not None
    assert created.name == "Test Calendar"
    assert created.color == "#ff0000"
    calendar_id = created.id

    calendars = await client.calendar.get_calendars()
    assert isinstance(calendars, list)
    found = next((c for c in calendars if c.id == calendar_id), None)
    assert found is not None
    assert isinstance(found, CalendarModel)

    fetched = await client.calendar.get_calendar_by_id(calendar_id)
    assert fetched is not None
    assert fetched.id == calendar_id
    assert fetched.name == "Test Calendar"

    update_form = CalendarUpdateForm(name="Updated Calendar")
    updated = await client.calendar.update_calendar(calendar_id, update_form)
    assert updated is not None
    assert updated.name == "Updated Calendar"

    fetched_updated = await client.calendar.get_calendar_by_id(calendar_id)
    assert fetched_updated.name == "Updated Calendar"


async def test_set_default_calendar(client):
    """Test setting a calendar as default."""
    admin_config = await client.auths.get_admin_config()
    if not admin_config.ENABLE_CALENDAR:
        admin_config.ENABLE_CALENDAR = True
        await client.auths.update_admin_config(admin_config)

    cal = await client.calendar.create_calendar(
        CalendarForm(name="Default Test Calendar")
    )
    calendar_id = cal.id

    default_cal = await client.calendar.set_default_calendar(calendar_id)
    assert default_cal is not None
    assert default_cal.is_default is True

    fetched = await client.calendar.get_calendar_by_id(calendar_id)
    assert fetched.is_default is True


async def test_event_lifecycle(client):
    """Test event CRUD: create, get, update, search, rsvp, delete."""
    admin_config = await client.auths.get_admin_config()
    if not admin_config.ENABLE_CALENDAR:
        admin_config.ENABLE_CALENDAR = True
        await client.auths.update_admin_config(admin_config)

    cal = await client.calendar.create_calendar(
        CalendarForm(name="Event Test Calendar")
    )
    calendar_id = cal.id

    user = await client.auths.get_session_user()
    now_ns = 1714521600000000000
    event_form = CalendarEventForm(
        calendar_id=calendar_id,
        title="Test Event",
        description="A test event",
        start_at=now_ns,
        end_at=now_ns + 3600000000000,
        location="Test Location",
        attendees=[{"user_id": user.id, "status": "pending"}],
    )
    created_event = await client.calendar.create_event(event_form)
    assert created_event is not None
    assert created_event.title == "Test Event"
    assert created_event.calendar_id == calendar_id
    assert created_event.location == "Test Location"
    event_id = created_event.id

    try:
        fetched_event = await client.calendar.get_event(event_id)
        assert fetched_event is not None
        assert fetched_event.id == event_id
        assert fetched_event.title == "Test Event"

        update_form = CalendarEventUpdateForm(
            title="Updated Event",
            description="Updated description",
        )
        updated_event = await client.calendar.update_event(event_id, update_form)
        assert updated_event is not None
        assert updated_event.title == "Updated Event"
        assert updated_event.description == "Updated description"

        search_results = await client.calendar.search_events(query="Updated")
        assert search_results is not None
        assert hasattr(search_results, "items")
        assert hasattr(search_results, "total")
        assert any(e.id == event_id for e in search_results.items)

        rsvp_form = RSVPForm(status="accepted")
        rsvp_result = await client.calendar.rsvp_event(event_id, rsvp_form)
        assert rsvp_result is not None
        assert rsvp_result.get("status") is True
        assert rsvp_result.get("rsvp") == "accepted"

        events = await client.calendar.get_events(
            start="2024-04-01T00:00:00",
            end="2024-06-01T00:00:00",
            calendar_ids=[calendar_id],
        )
        assert isinstance(events, list)
        assert any(e.id == event_id for e in events)
    finally:
        await client.calendar.delete_event(event_id)
