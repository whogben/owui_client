import pytest

from owui_client.models.events import (
    EventWebhook,
    EventWebhookForm,
    EventWebhookUpdateForm,
)


@pytest.mark.asyncio
async def test_get_event_webhooks_empty(client):
    """GET list returns a list (possibly empty) of EventWebhook."""
    webhooks = await client.events.get_event_webhooks()
    assert isinstance(webhooks, list)
    for wh in webhooks:
        assert isinstance(wh, EventWebhook)


@pytest.mark.asyncio
async def test_event_webhook_crud(client):
    """Create, read, update, delete round-trip for an event webhook."""
    # Clean slate: remove any webhook using our test URL to avoid collisions.
    test_url = "https://example.com/webhook/test_client"
    for existing in await client.events.get_event_webhooks():
        if existing.url == test_url:
            await client.events.delete_event_webhook(existing.id)

    # Create with a wildcard event filter.
    created = await client.events.create_event_webhook(
        EventWebhookForm(
            name="owui_client test webhook",
            url=test_url,
            enabled=True,
            events=["*"],
            targets=None,
        )
    )
    assert isinstance(created, EventWebhook)
    assert created.id
    assert created.url == test_url
    assert created.enabled is True
    assert created.events == ["*"]
    assert created.targets is None
    webhook_id = created.id

    try:
        # It appears in the list.
        listed = await client.events.get_event_webhooks()
        assert any(wh.id == webhook_id for wh in listed)

        # Update: narrow the event filter and disable delivery.
        updated = await client.events.update_event_webhook(
            webhook_id,
            EventWebhookUpdateForm(
                events=["user.created"],
                enabled=False,
            ),
        )
        assert isinstance(updated, EventWebhook)
        assert updated.id == webhook_id
        assert updated.events == ["user.created"]
        assert updated.enabled is False
        # Unmodified fields are preserved.
        assert updated.url == test_url

        # Update: set delivery targets to restrict to system events only.
        targeted = await client.events.update_event_webhook(
            webhook_id,
            EventWebhookUpdateForm(targets=[]),
        )
        assert targeted.targets == []
    finally:
        # Delete and confirm.
        deleted = await client.events.delete_event_webhook(webhook_id)
        assert deleted is True
        listed_after = await client.events.get_event_webhooks()
        assert not any(wh.id == webhook_id for wh in listed_after)


@pytest.mark.asyncio
async def test_delete_event_webhook_not_found(client):
    """DELETE on a non-existent id raises 404."""
    with pytest.raises(Exception) as exc_info:
        await client.events.delete_event_webhook("nonexistent-webhook-id")
    assert "404" in str(exc_info.value)


@pytest.mark.asyncio
async def test_update_event_webhook_not_found(client):
    """PUT on a non-existent id raises 404."""
    with pytest.raises(Exception) as exc_info:
        await client.events.update_event_webhook(
            "nonexistent-webhook-id",
            EventWebhookUpdateForm(enabled=False),
        )
    assert "404" in str(exc_info.value)


@pytest.mark.asyncio
async def test_create_event_webhook_invalid_event(client):
    """Create with an unknown event name raises 400."""
    with pytest.raises(Exception) as exc_info:
        await client.events.create_event_webhook(
            EventWebhookForm(
                url="https://example.com/webhook/invalid",
                events=["totally.bogus.event"],
            )
        )
    assert "400" in str(exc_info.value)
