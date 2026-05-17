"""Models for the Analytics endpoints.

Analytics provides read-only admin dashboards for message counts, token usage,
user activity, and model performance. All endpoints require admin privileges.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class ModelAnalyticsEntry(BaseModel):
    """Message count for a single model."""

    model_id: str
    """Identifier of the model (e.g. 'gpt-4o', 'llama3')."""

    count: int
    """Number of messages sent using this model."""


class ModelAnalyticsResponse(BaseModel):
    """Response from the model analytics endpoint."""

    models: list[ModelAnalyticsEntry]
    """List of models sorted by message count descending."""


class UserAnalyticsEntry(BaseModel):
    """Message count and token usage for a single user."""

    user_id: str
    """Unique identifier of the user."""

    name: Optional[str] = None
    """Display name of the user."""

    email: Optional[str] = None
    """Email address of the user."""

    count: int
    """Number of messages sent by this user."""

    input_tokens: int = 0
    """Total input (prompt) tokens consumed."""

    output_tokens: int = 0
    """Total output (completion) tokens consumed."""

    total_tokens: int = 0
    """Sum of input and output tokens."""


class UserAnalyticsResponse(BaseModel):
    """Response from the user analytics endpoint."""

    users: list[UserAnalyticsEntry]
    """List of users sorted by message count descending, limited by the request limit."""


class SummaryResponse(BaseModel):
    """Dashboard summary statistics."""

    total_messages: int
    """Total number of messages across all models."""

    total_chats: int
    """Total number of distinct chats."""

    total_models: int
    """Number of distinct models used."""

    total_users: int
    """Number of distinct users who sent messages."""


class DailyStatsEntry(BaseModel):
    """Message counts per model for a single date (or hour)."""

    date: str
    """Date string in 'YYYY-MM-DD' format, or 'YYYY-MM-DD HH:00' for hourly granularity."""

    models: dict[str, int]
    """Message counts keyed by model ID.

    Dict Fields:
        Keys are model ID strings (e.g. 'gpt-4o'). Values are the number of
        messages sent using that model on this date/hour.
    """


class DailyStatsResponse(BaseModel):
    """Response from the daily (or hourly) stats endpoint."""

    data: list[DailyStatsEntry]
    """Time-series entries sorted chronologically."""


class TokenUsageEntry(BaseModel):
    """`Token` usage for a single model."""

    model_id: str
    """Identifier of the model."""

    input_tokens: int
    """Total input (prompt) tokens consumed by this model."""

    output_tokens: int
    """Total output (completion) tokens consumed by this model."""

    total_tokens: int
    """Sum of input and output tokens for this model."""

    message_count: int
    """Number of messages sent using this model."""


class TokenUsageResponse(BaseModel):
    """Response from the token usage endpoint."""

    models: list[TokenUsageEntry]
    """List of models sorted by total tokens descending."""

    total_input_tokens: int
    """Aggregate input tokens across all models."""

    total_output_tokens: int
    """Aggregate output tokens across all models."""

    total_tokens: int
    """Aggregate total tokens across all models."""


class ModelChatEntry(BaseModel):
    """Preview of a chat that used a specific model."""

    chat_id: str
    """Unique identifier of the chat."""

    user_id: Optional[str] = None
    """ID of the user who sent the first user message in the chat."""

    user_name: Optional[str] = None
    """Display name of the user."""

    first_message: Optional[str] = None
    """Truncated preview (up to 200 chars) of the first user message content."""

    updated_at: int
    """Unix timestamp of the most recent message in the chat."""


class ModelChatsResponse(BaseModel):
    """Response from the model chats browser endpoint."""

    chats: list[ModelChatEntry]
    """List of chats that used the specified model."""

    total: int
    """Total number of chats returned."""


class HistoryEntry(BaseModel):
    """Daily feedback counts (thumbs up / thumbs down)."""

    date: str
    """Date string in 'YYYY-MM-DD' format."""

    won: int = 0
    """Number of positive (thumbs up / rating=1) feedbacks on this date."""

    lost: int = 0
    """Number of negative (thumbs down / rating=-1) feedbacks on this date."""


class TagEntry(BaseModel):
    """A chat tag and its usage count."""

    tag: str
    """Tag label."""

    count: int
    """Number of chats with this tag."""


class ModelOverviewResponse(BaseModel):
    """Model overview with feedback history and top chat tags."""

    history: list[HistoryEntry]
    """Daily feedback counts, with gaps filled (zero-count days included)."""

    tags: list[TagEntry]
    """Top 10 chat tags sorted by count descending."""
