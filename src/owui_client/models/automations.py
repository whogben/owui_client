"""Automation models for the Open WebUI scheduling system.

Automations are scheduled tasks that execute prompts on a recurring basis using
RRULE scheduling. Each automation creates a chat and runs through the full chat
completion pipeline when triggered.
"""

from typing import Optional, Any
from pydantic import BaseModel, ConfigDict


class AutomationTerminalConfig(BaseModel):
    """Configuration for a terminal server attached to an automation.

    When present, the automation's execution will connect to the specified
    terminal server before running the prompt.
    """

    server_id: str
    """ID of the terminal server to connect to."""

    cwd: Optional[str] = None
    """Working directory to set on the terminal server before execution."""


class AutomationData(BaseModel):
    """Core data payload defining what an automation does and when it runs.

    This is the structured form used in create/update requests. When stored
    in the database and returned by the API, it is serialized as a plain dict
    on `AutomationModel.data`.
    """

    prompt: str
    """Prompt template to execute. Supports template variables like `{{user_name}}`."""

    model_id: str
    """ID of the model to use for chat completion."""

    rrule: str
    """RRULE recurrence rule defining the schedule (RFC 5545). For example,
    `FREQ=DAILY;DTSTART=20250101T090000Z` for daily at 9 AM UTC."""

    terminal: Optional[AutomationTerminalConfig] = None
    """Optional terminal server configuration."""


class AutomationModel(BaseModel):
    """Full automation model as stored in the database.

    Represents an automation with all persisted fields including scheduling state.
    """

    id: str
    """Unique identifier (UUID)."""

    user_id: str
    """ID of the user who owns the automation."""

    name: str
    """Display name of the automation."""

    data: dict[str, Any]
    """Serialized automation data defining the prompt, schedule, and model.

    Dict Fields:
        - `prompt` (str, required): Prompt template to execute
        - `model_id` (str, required): Model ID for chat completion
        - `rrule` (str, required): RRULE recurrence rule for scheduling
        - `terminal` (dict, optional): Terminal server config with `server_id` and
          optional `cwd` keys
    """

    meta: Optional[dict[str, Any]] = None
    """Optional metadata for the automation.

    Dict Fields:
        - `system_prompt` (str, optional): System prompt injected before the user prompt
        - `temperature` (float, optional): Sampling temperature override
        - `max_tokens` (int, optional): Maximum tokens override
        - `webhook` (str, optional): Webhook URL notified after execution
    """

    is_active: bool = True
    """Whether the automation is active and eligible for scheduling."""

    last_run_at: Optional[int] = None
    """Timestamp (nanoseconds since epoch) of the last execution."""

    next_run_at: Optional[int] = None
    """Timestamp (nanoseconds since epoch) of the next scheduled execution."""

    created_at: int
    """Timestamp (nanoseconds since epoch) of creation."""

    updated_at: int
    """Timestamp (nanoseconds since epoch) of last update."""

    model_config = ConfigDict(from_attributes=True)


class AutomationRunModel(BaseModel):
    """Record of a single automation execution.

    Each time an automation runs, a run record is created tracking the outcome.
    """

    id: str
    """Unique identifier (UUID)."""

    automation_id: str
    """ID of the parent automation."""

    chat_id: Optional[str] = None
    """ID of the chat created by this run, if successful."""

    status: str
    """Execution status: 'success' or 'error'."""

    error: Optional[str] = None
    """Error message if status is 'error'."""

    created_at: int
    """Timestamp (nanoseconds since epoch) of when the run completed."""

    model_config = ConfigDict(from_attributes=True)


class AutomationForm(BaseModel):
    """Form for creating or updating an automation.

    The `data` field contains the structured automation definition including
    the RRULE schedule. The backend validates the RRULE against the user's
    timezone and enforces rate limits.
    """

    name: str
    """Display name of the automation."""

    data: AutomationData
    """Core automation data: prompt, model, schedule, and optional terminal config."""

    meta: Optional[dict[str, Any]] = None
    """Optional metadata for the automation.

    Dict Fields:
        - `system_prompt` (str, optional): System prompt injected before the user prompt
        - `temperature` (float, optional): Sampling temperature override
        - `max_tokens` (int, optional): Maximum tokens override
        - `webhook` (str, optional): Webhook URL notified after execution
    """

    is_active: Optional[bool] = True
    """Whether the automation should be active on creation. Defaults to True."""


class AutomationResponse(AutomationModel):
    """Enriched automation response with run history and computed next runs.

    Extends `AutomationModel` with the latest run record and a list of
    upcoming execution timestamps.
    """

    last_run: Optional[AutomationRunModel] = None
    """The most recent run record, if any."""

    next_runs: Optional[list[int]] = None
    """List of upcoming execution timestamps (nanoseconds since epoch)."""


class AutomationListResponse(BaseModel):
    """Paginated list of automations with enriched run data.

    Each item includes the latest run record. The `total` field reflects the
    total count before pagination.
    """

    items: list[AutomationResponse] = []
    """List of automations in the current page."""

    total: int = 0
    """Total number of automations matching the query."""
