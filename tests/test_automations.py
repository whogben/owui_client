import pytest
from owui_client.models.automations import (
    AutomationForm,
    AutomationData,
)

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio


async def test_automations_client_initialization(client):
    assert client.automations is not None


async def test_automations_lifecycle(client):
    """Test create, get, list, update, toggle, run, delete automation."""
    # Use a daily RRULE starting now so validation passes
    rrule = "FREQ=DAILY"
    form = AutomationForm(
        name="Test Automation",
        data=AutomationData(
            prompt="Summarize the latest news",
            model_id="test-model",
            rrule=rrule,
        ),
    )

    # 1. Create automation
    created = await client.automations.create_new_automation(form)
    assert created is not None
    assert created.name == "Test Automation"
    assert created.is_active is True
    automation_id = created.id

    # 2. Get automation by ID
    fetched = await client.automations.get_automation_by_id(automation_id)
    assert fetched is not None
    assert fetched.id == automation_id
    assert fetched.name == "Test Automation"

    # 3. List automations
    items = await client.automations.get_automation_items()
    assert items.total >= 1
    found = next((a for a in items.items if a.id == automation_id), None)
    assert found is not None
    assert found.id == automation_id

    # 4. Update automation
    update_form = AutomationForm(
        name="Updated Automation",
        data=AutomationData(
            prompt="Translate the latest news",
            model_id="test-model-v2",
            rrule=rrule,
        ),
    )
    updated = await client.automations.update_automation_by_id(
        automation_id, update_form
    )
    assert updated is not None
    assert updated.name == "Updated Automation"

    # 5. Toggle automation (pause)
    toggled = await client.automations.toggle_automation_by_id(automation_id)
    assert toggled is not None
    assert toggled.is_active is False

    # Toggle back to active
    toggled_back = await client.automations.toggle_automation_by_id(automation_id)
    assert toggled_back is not None
    assert toggled_back.is_active is True

    # 6. Run automation (triggers async execution)
    run_result = await client.automations.run_automation_by_id(automation_id)
    assert run_result is not None
    assert run_result.id == automation_id

    # 7. Get automation runs
    runs = await client.automations.get_automation_runs(automation_id)
    assert isinstance(runs, list)

    # 8. Delete automation
    delete_result = await client.automations.delete_automation_by_id(automation_id)
    assert delete_result is True

    # 9. Verify deletion
    try:
        await client.automations.get_automation_by_id(automation_id)
        assert False, "Should have raised exception"
    except Exception:
        pass


async def test_automations_list_with_filters(client):
    """Test listing automations with query and status filters."""
    rrule = "FREQ=WEEKLY"
    form = AutomationForm(
        name="Filter Test Automation",
        data=AutomationData(
            prompt="Test query filter",
            model_id="test-model",
            rrule=rrule,
        ),
    )

    created = await client.automations.create_new_automation(form)
    assert created is not None
    automation_id = created.id

    # Filter by query
    queried = await client.automations.get_automation_items(query="Filter Test")
    assert queried.total >= 1

    # Filter by active status
    active = await client.automations.get_automation_items(status="active")
    assert active.total >= 1

    # Clean up
    await client.automations.delete_automation_by_id(automation_id)
