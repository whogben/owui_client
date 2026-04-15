"""Models for chat messages."""

from typing import Any, Optional
from pydantic import BaseModel


class ChatMessageModel(BaseModel):
    """A chat message within a conversation."""
    id: str
    chat_id: str
    user_id: str
    role: str
    """Message role, typically 'user', 'assistant', or 'system'."""
    parent_id: Optional[str] = None
    content: Optional[Any] = None
    """Message content. Can be a string, list of content blocks, or None."""
    output: Optional[list] = None
    """Model output content blocks."""
    model_id: Optional[str] = None
    files: Optional[list] = None
    """List of file attachments."""
    sources: Optional[list] = None
    """List of retrieval sources cited in the response."""
    embeds: Optional[list] = None
    """List of embedded content items."""
    done: bool = True
    """Whether the model has finished generating."""
    status_history: Optional[list] = None
    """List of status updates during generation."""
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
