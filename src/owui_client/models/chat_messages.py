from typing import Optional, Any, Union
from pydantic import BaseModel, ConfigDict


class ChatMessageModel(BaseModel):
    """
    Represents a single message within a chat conversation.

    This model is used for analytics and message retrieval endpoints.
    It stores the message content, metadata, and token usage information.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    """Unique identifier for the message (composite ID: `{chat_id}-{message_id}`)."""

    chat_id: str
    """ID of the chat this message belongs to."""

    user_id: str
    """ID of the user who sent this message."""

    role: str
    """Message role: 'user', 'assistant', or 'system'."""

    parent_id: Optional[str] = None
    """ID of the parent message in the conversation thread."""

    content: Optional[Any] = None
    """Message content. Can be a string or a list of content blocks.

    Dict Fields:
        When content is a list of blocks, each block may contain:
        - `type` (str, required): Block type, e.g. 'text', 'image_url'
        - `text` (str, optional): Text content for text blocks
        - `image_url` (dict, optional): Image URL object for image blocks
            - `url` (str, required): The image URL
    """

    output: Optional[list[Any]] = None
    """Generated output from the model, typically a list of output blocks."""

    model_id: Optional[str] = None
    """ID of the model that generated this message (for assistant messages)."""

    files: Optional[list[Any]] = None
    """List of attached file objects."""

    sources: Optional[list[Any]] = None
    """List of source citations or references."""

    embeds: Optional[list[Any]] = None
    """List of embedded content objects."""

    done: bool = True
    """Whether the message generation is complete."""

    status_history: Optional[list[Any]] = None
    """History of status changes during message generation."""

    error: Optional[Union[dict[str, Any], str]] = None
    """Error information if message generation failed.

    Dict Fields:
        - `message` (str, optional): Error message text
        - `code` (str, optional): Error code
    """

    usage: Optional[dict[str, Any]] = None
    """Token usage and timing information.

    Dict Fields:
        - `prompt_tokens` (int, optional): Number of input tokens
        - `completion_tokens` (int, optional): Number of output tokens
        - `total_tokens` (int, optional): Total token count
        - `prompt_ms` (int, optional): Time spent on prompt processing in milliseconds
        - `completion_ms` (int, optional): Time spent on completion generation in milliseconds
        - `total_duration` (int, optional): Total generation duration in milliseconds
    """

    created_at: int
    """Timestamp when the message was created (Unix epoch)."""

    updated_at: int
    """Timestamp when the message was last updated (Unix epoch)."""
