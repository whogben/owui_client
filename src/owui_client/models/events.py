"""Models for the Open WebUI event webhooks system.

Open WebUI emits structured events for a wide range of system activity
(sign-ins, config changes, chat/file/knowledge actions, etc.). Administrators
configure outbound **event webhooks** that receive matching events as HTTP POST
deliveries. Each webhook filters by event name pattern and optionally restricts
delivery to events whose actor/subject matches a set of users or groups.

The backing store is the `events.webhooks` config key (a list of webhook
dicts); there is no dedicated database table. The backend normalizes each
webhook dict via `normalize_event_webhook` in
`refs/owui_source_main/backend/open_webui/events.py`. Note that, unlike most
Open WebUI models, the `created_at`/`updated_at` timestamps here are
**seconds** since the epoch (not nanoseconds).
"""

from typing import Optional
from pydantic import BaseModel


class EventWebhookTarget(BaseModel):
    """A single delivery target that scopes which events a webhook receives.

    A webhook with `targets == None` receives events for all users and
    system activity; `targets == []` (empty) receives only system events with
    no associated user; a non-empty list restricts delivery to events whose
    actor or subject user matches one of the listed users, or belongs to one of
    the listed groups.
    """

    type: str
    """Target kind. Must be `'user'` or `'group'` (validated by the backend)."""

    id: str
    """ID of the user or group being targeted."""


class EventWebhook(BaseModel):
    """A normalized event webhook as stored in the `events.webhooks` config.

    The `id` is server-assigned (UUID) on create. `events` and `targets`
    together determine which emitted events get delivered to `url`. The
    `enabled` flag toggles delivery without deleting the webhook.
    """

    id: str
    """Unique identifier (UUID). The special id `'default'` is reserved for the
    webhook migrated from the legacy single-webhook config."""

    name: str
    """Display name. Defaults to `'Default webhook'` for the default id, else
    `'Webhook'`, when not provided."""

    url: str
    """Destination URL that receives event deliveries via HTTP POST. Validated
    with the server-side URL allow-list (`validate_url`)."""

    enabled: bool
    """Whether this webhook is actively delivering events. When `False`, no
    events match this webhook."""

    events: list[str]
    """Event name filters that select which events are delivered.

    Each entry must be one of:
    - `'*'` — matches every event.
    - `'prefix.*'` — matches every event whose name starts with `'prefix.'`
      (e.g. `'chat.*'`, `'knowledge.file.*'`). The prefix must correspond to at
      least one real event in the catalog.
    - An exact event name from the event catalog (e.g. `'user.created'`,
      `'auth.login'`, `'config.updated'`). The full catalog is defined by
      `EventDefinitions` in
      `refs/owui_source_main/backend/open_webui/events.py` and is also available
      via the `GET /api/events` catalog endpoint.

    An empty/missing list defaults to `['*']`.
    """

    targets: Optional[list[EventWebhookTarget]] = None
    """Optional list of delivery targets restricting which users' events are
    sent. `None` means all users plus system events; an empty list means system
    events only. See `EventWebhookTarget` for the entry shape (`type`/`id`)."""

    created_at: int
    """Creation time as Unix epoch **seconds** (not nanoseconds)."""

    updated_at: int
    """Last update time as Unix epoch **seconds** (not nanoseconds)."""


class EventWebhookForm(BaseModel):
    """Create/upsert body for `POST /api/events/webhooks`.

    Mirrors `EventWebhookForm` in
    `refs/owui_source_main/backend/open_webui/main.py`. On submit the backend
    upserts by `id`: an existing webhook with the same id is replaced, otherwise
    a new webhook is appended (with a server-generated id). `url` is required
    and validated.
    """

    name: Optional[str] = None
    """Optional display name. Defaults server-side if omitted."""

    url: str
    """Destination URL for event deliveries (validated against the URL allow-list)."""

    enabled: bool = True
    """Whether delivery is active. Defaults to `True`."""

    events: Optional[list[str]] = None
    """Optional event filters; see `EventWebhook.events`. Defaults to `['*']`."""

    targets: Optional[list[EventWebhookTarget]] = None
    """Optional delivery targets; see `EventWebhook.targets`. Defaults to all."""

    def to_payload(self) -> dict:
        """Serialize for the JSON request body, omitting unset (`None`) fields."""
        return self.model_dump(mode="json", exclude_none=True)


class EventWebhookUpdateForm(BaseModel):
    """Partial update body for `PUT /api/events/webhooks/{webhook_id}`.

    Mirrors `EventWebhookUpdateForm` in
    `refs/owui_source_main/backend/open_webui/main.py`. All fields optional; the
    backend merges only the provided (non-`None`) fields onto the existing
    webhook.
    """

    name: Optional[str] = None
    """Optional new display name."""

    url: Optional[str] = None
    """Optional new destination URL (validated against the URL allow-list)."""

    enabled: Optional[bool] = None
    """Optional new enabled flag."""

    events: Optional[list[str]] = None
    """Optional new event filters; see `EventWebhook.events`."""

    targets: Optional[list[EventWebhookTarget]] = None
    """Optional new delivery targets; see `EventWebhook.targets`. Pass an empty
    list to restrict to system events only, or `None` to leave unchanged."""

    def to_payload(self) -> dict:
        """Serialize for the JSON request body, omitting unset (`None`) fields."""
        return self.model_dump(mode="json", exclude_none=True)
