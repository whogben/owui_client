"""Models for the Analytics endpoints."""

from typing import Optional, Any
from pydantic import BaseModel
from owui_client.models.chat_messages import ChatMessageModel


class ModelAnalyticsEntry(BaseModel):
    """Message count for a single model."""
    model_id: str
    count: int


class ModelAnalyticsResponse(BaseModel):
    """Message counts per model."""
    models: list[ModelAnalyticsEntry]


class UserAnalyticsEntry(BaseModel):
    """Message count and token usage for a single user."""
    user_id: str
    name: Optional[str] = None
    email: Optional[str] = None
    count: int
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0


class UserAnalyticsResponse(BaseModel):
    """Message counts and token usage per user."""
    users: list[UserAnalyticsEntry]


class SummaryResponse(BaseModel):
    """Dashboard summary statistics."""
    total_messages: int
    total_chats: int
    total_models: int
    total_users: int


class DailyStatsEntry(BaseModel):
    """Message counts by model for a single time period."""

    date: str
    """Date string in YYYY-MM-DD format."""
    models: dict[str, int]
    """Message counts keyed by model ID.

    Dict Fields:
        - `<model_id>` (int, required): Number of messages sent to the model with this ID.
    """


class DailyStatsResponse(BaseModel):
    """Time-series message counts grouped by model."""
    data: list[DailyStatsEntry]


class TokenUsageEntry(BaseModel):
    """LLM `Token` usage for a single model."""
    model_id: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    message_count: int


class TokenUsageResponse(BaseModel):
    """LLM `Token` usage aggregated by model."""
    models: list[TokenUsageEntry]
    total_input_tokens: int
    total_output_tokens: int
    total_tokens: int


class ModelChatEntry(BaseModel):
    """A chat that used a specific model, with preview info."""
    chat_id: str
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    first_message: Optional[str] = None
    updated_at: int


class ModelChatsResponse(BaseModel):
    """List of chats that used a specific model."""
    chats: list[ModelChatEntry]
    total: int


class HistoryEntry(BaseModel):
    """Feedback history for a single day."""
    date: str
    won: int = 0
    lost: int = 0


class TagEntry(BaseModel):
    """Tag usage count."""
    tag: str
    count: int


class ModelOverviewResponse(BaseModel):
    """Model overview with feedback history and chat tags."""
    history: list[HistoryEntry]
    tags: list[TagEntry]
