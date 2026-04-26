import pytest
from owui_client.models.automations import (
    AutomationForm,
    AutomationData,
    AutomationResponse,
    AutomationListResponse,
    AutomationRunModel,
)

pytestmark = pytest.mark.asyncio


async def _ensure_automations_enabled(client):
    config = await client.auths.get_admin_config()
    if not config.ENABLE_AUTOMATIONS:
        config.ENABLE_AUTOMATIONS = True
        await client.auths.update_admin_config(config)


async def test_automation_lifecycle(client):
    await _ensure_automations_enabled(client)

    automation_form = AutomationForm(
        name="Test Automation",
        data=AutomationData(
            prompt="Say hello",
            model_id="gpt-3.5-turbo",
            rrule="FREQ=DAILY;INTERVAL=1",
        ),
        is_active=True,
    )

    created = await client.automations.create_automation(automation_form)
    assert isinstance(created, AutomationResponse)
    assert created.name == "Test Automation"
    assert created.data["prompt"] == "Say hello"
    assert created.is_active is True
    assert created.id is not None

    automation_id = created.id

    listed = await client.automations.list_automations()
    assert isinstance(listed, AutomationListResponse)
    assert listed.total >= 1
    assert any(item.id == automation_id for item in listed.items)

    fetched = await client.automations.get_automation(automation_id)
    assert isinstance(fetched, AutomationResponse)
    assert fetched.id == automation_id
    assert fetched.name == "Test Automation"

    update_form = AutomationForm(
        name="Updated Automation",
        data=AutomationData(
            prompt="Say goodbye",
            model_id="gpt-3.5-turbo",
            rrule="FREQ=DAILY;INTERVAL=1",
        ),
        is_active=True,
    )

    updated = await client.automations.update_automation(automation_id, update_form)
    assert isinstance(updated, AutomationResponse)
    assert updated.name == "Updated Automation"
    assert updated.data["prompt"] == "Say goodbye"

    toggled = await client.automations.toggle_automation(automation_id)
    assert isinstance(toggled, AutomationResponse)
    assert toggled.is_active is False

    toggled_back = await client.automations.toggle_automation(automation_id)
    assert toggled_back.is_active is True

    ran = await client.automations.run_automation(automation_id)
    assert isinstance(ran, AutomationResponse)
    assert ran.id == automation_id

    runs = await client.automations.get_automation_runs(automation_id)
    assert isinstance(runs, list)
    for run in runs:
        assert isinstance(run, AutomationRunModel)
        assert run.automation_id == automation_id

    deleted = await client.automations.delete_automation(automation_id)
    assert deleted is True

    listed_after = await client.automations.list_automations()
    assert not any(item.id == automation_id for item in listed_after.items)
