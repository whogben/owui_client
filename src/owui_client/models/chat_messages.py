"""Models for chat messages."""

from typing import Any, Optional
from pydantic import BaseModel


class ChatMessageModel(BaseModel):
    """A chat message within a conversation."""
    id: str
    chat_id: str
    user_id: str
    role: str
    parent_id: Optional[str] = None
    content: Optional[Any] = None
    output: Optional[list] = None
    model_id: Optional[str] = None
    files: Optional[list] = None
    sources: Optional[list] = None
    embeds: Optional[list] = None
    done: bool = True
    status_history: Optional[list] = None
    error: Optional[dict | str] = None
    """Error information if the message generation failed.

    When a string, contains the raw error message text.

    Dict Fields:
        - `message` (str, required): Human-readable error message.
        - `type` (str, optional): Error type/classification.
        - Additional keys may provide stack trace or provider-specific details.
    """
    usage: Optional[dict] = None
    """Token usage statistics for this message.

    Dict Fields:
        - `prompt_tokens` (int, optional): Number of tokens in the prompt.
        - `completion_tokens` (int, optional): Number of tokens in the completion.
        - `total_tokens` (int, optional): Total tokens used.
        - `prompt_tokens_details` (dict, optional): Breakdown of prompt token usage.
        - `completion_tokens_details` (dict, optional): Breakdown of completion token usage.
    """
    created_at: int
    updated_at: int
