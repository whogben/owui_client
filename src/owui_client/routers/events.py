"""Client for the Event Webhooks endpoints.

These are top-level `@app` routes under `/api/events/webhooks` (defined in
`refs/owui_source_main/backend/open_webui/main.py`, not in a router module). All
four endpoints require administrator access. The event webhooks system replaced
the old per-instance `/api/webhook` URL endpoints in Open WebUI 0.10.0.
"""

from typing import List

from owui_client.client_base import ResourceBase
from owui_client.models.events import (
    EventWebhook,
    EventWebhookForm,
    EventWebhookUpdateForm,
)


class EventsClient(ResourceBase):
    """
    Client for the Event Webhooks admin endpoints.
    """

    async def get_event_webhooks(self) -> List[EventWebhook]:
        """List all configured event webhooks.

        Returns the normalized webhook list stored under the `events.webhooks`
        config key. Invalid entries in the stored config are skipped by the
        backend rather than causing an error.

        Returns:
            List[EventWebhook]: All event webhooks (may be empty).
        """
        return await self._request(
            "GET",
            "/events/webhooks",
            model=List[EventWebhook],
        )

    async def create_event_webhook(
        self, form_data: EventWebhookForm
    ) -> EventWebhook:
        """Create an event webhook (always appends).

        Submits the form to `POST /api/events/webhooks`. Because `EventWebhookForm`
        does not expose `id`, this always appends a new webhook with a
        server-generated id; the backend's underlying upsert-by-id path is not
        reachable from this client. The URL is validated against the server URL
        allow-list and event filters are validated against the event catalog.

        Args:
            form_data: Creation body; `url` is required.

        Returns:
            `EventWebhook`: The created/updated webhook.

        Raises:
            httpx.HTTPStatusError: `400` if the URL or event filters are
                invalid.
        """
        return await self._request(
            "POST",
            "/events/webhooks",
            json=form_data.to_payload(),
            model=EventWebhook,
        )

    async def update_event_webhook(
        self,
        webhook_id: str,
        form_data: EventWebhookUpdateForm,
    ) -> EventWebhook:
        """Update an existing event webhook by id.

        Only the non-`None` fields on `form_data` are merged onto the stored
        webhook. The URL (if provided) and event filters are re-validated.

        Args:
            webhook_id: The id of the webhook to update.
            form_data: Partial update body.

        Returns:
            `EventWebhook`: The updated webhook.

        Raises:
            httpx.HTTPStatusError: `404` if no webhook exists with `webhook_id`,
                or `400` if the URL or event filters are invalid.
        """
        return await self._request(
            "PUT",
            f"/events/webhooks/{webhook_id}",
            json=form_data.to_payload(),
            model=EventWebhook,
        )

    async def delete_event_webhook(self, webhook_id: str) -> bool:
        """Delete an event webhook by id.

        Args:
            webhook_id: The id of the webhook to delete. Deleting the special
                `'default'` webhook also clears the legacy `webhook_url` config.

        Returns:
            `True` on success. (The backend response body is `{"status": true}`.)

        Raises:
            httpx.HTTPStatusError: `404` if no webhook exists with `webhook_id`.
        """
        result = await self._request(
            "DELETE",
            f"/events/webhooks/{webhook_id}",
            model=dict,
        )
        return bool(result.get("status"))
