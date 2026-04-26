"""Models for the Automations endpoints.

This module provides Pydantic models for automation scheduling, execution,
and run history. Automations allow recurring chat completions based on an
RRULE schedule.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class AutomationTerminalConfig(BaseModel):
    """Terminal server configuration for an automation."""

    server_id: str
    """The terminal server ID to use for execution."""

    cwd: Optional[str] = None
    """Optional working directory for the terminal session."""


class AutomationData(BaseModel):
    """Core automation execution data.

    Defines the prompt, model, schedule rule, and optional terminal
    configuration used when the automation runs.
    """

    prompt: str
    """The prompt text sent to the model on each execution."""

    model_id: str
    """The model identifier to use for generating responses."""

    rrule: str
    """Recurrence rule string defining the schedule (e.g., 'FREQ=DAILY;INTERVAL=1')."""

    terminal: Optional[AutomationTerminalConfig] = None
    """Optional terminal server configuration for headless execution."""


class AutomationModel(BaseModel):
    """Base automation record model.

    Represents a stored automation with its schedule configuration and status.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    """Unique automation identifier."""

    user_id: str
    """ID of the user who owns this automation."""

    name: str
    """Display name of the automation."""

    data: dict
    """Serialized automation execution data.

    Dict Fields:
        - `prompt` (str, required): The prompt text sent to the model
        - `model_id` (str, required): The model identifier
        - `rrule` (str, required): Recurrence rule string
        - `terminal` (dict, optional): Terminal server config with `server_id` and optional `cwd`
    """

    meta: Optional[dict] = None
    """Optional metadata for the automation.

    Dict Fields:
        - `system_prompt` (str, optional): Custom system prompt override
        - `temperature` (float, optional): Sampling temperature
        - `max_tokens` (int, optional): Maximum tokens to generate
        - `webhook` (str, optional): Webhook URL for notifications
    """

    is_active: bool
    """Whether the automation is currently active."""

    last_run_at: Optional[int] = None
    """Timestamp of the last execution in epoch nanoseconds."""

    next_run_at: Optional[int] = None
    """Timestamp of the next scheduled execution in epoch nanoseconds."""

    created_at: int
    """Creation timestamp in epoch nanoseconds."""

    updated_at: int
    """Last update timestamp in epoch nanoseconds."""


class AutomationRunModel(BaseModel):
    """Record of a single automation execution."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    """Unique run identifier."""

    automation_id: str
    """ID of the parent automation."""

    chat_id: Optional[str] = None
    """ID of the chat created by this run, if successful."""

    status: str
    """Execution status: 'success' or 'error'."""

    error: Optional[str] = None
    """Error message if the run failed."""

    created_at: int
    """Run timestamp in epoch nanoseconds."""


class AutomationForm(BaseModel):
    """Form data for creating or updating an automation."""

    name: str
    """Display name for the automation."""

    data: AutomationData
    """Core execution data including prompt, model, and schedule."""

    meta: Optional[dict] = None
    """Optional metadata.

    Dict Fields:
        - `system_prompt` (str, optional): Custom system prompt override
        - `temperature` (float, optional): Sampling temperature
        - `max_tokens` (int, optional): Maximum tokens to generate
        - `webhook` (str, optional): Webhook URL for notifications
    """

    is_active: Optional[bool] = True
    """Whether the automation should be active. Defaults to True."""


class AutomationResponse(AutomationModel):
    """Enriched automation response including run history and upcoming schedule.

    Extends `AutomationModel` with computed fields for the latest run
    and next scheduled execution times.
    """

    last_run: Optional[AutomationRunModel] = None
    """The most recent execution record for this automation."""

    next_runs: Optional[list[int]] = None
    """List of upcoming execution timestamps in epoch nanoseconds."""


class AutomationListResponse(BaseModel):
    """Paginated list of automations."""

    items: list[AutomationResponse]
    """List of automation records for the current page."""

    total: int
    """Total number of automations matching the query."""
