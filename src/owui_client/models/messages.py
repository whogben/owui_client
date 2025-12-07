from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from owui_client.models.users import UserNameResponse

"""
Models for message-related operations.
"""


class MessageModel(BaseModel):
    """
    Represents a message in a channel.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    """Unique identifier for the message."""

    user_id: str
    """ID of the user who sent the message."""

    channel_id: Optional[str] = None
    """ID of the channel the message belongs to."""

    reply_to_id: Optional[str] = None
    """ID of the message this message is replying to."""

    parent_id: Optional[str] = None
    """ID of the parent message if this is a thread reply."""

    # Pins
    is_pinned: bool = False
    """Whether the message is pinned."""

    pinned_by: Optional[str] = None
    """ID of the user who pinned the message."""

    pinned_at: Optional[int] = None  # timestamp in epoch (time_ns)
    """Timestamp when the message was pinned (epoch time in nanoseconds)."""

    content: str
    """Content of the message."""

    data: Optional[dict] = None
    """Additional data associated with the message."""

    meta: Optional[dict] = None
    """Metadata associated with the message."""

    created_at: int  # timestamp in epoch (time_ns)
    """Timestamp when the message was created (epoch time in nanoseconds)."""

    updated_at: int  # timestamp in epoch (time_ns)
    """Timestamp when the message was last updated (epoch time in nanoseconds)."""


class MessageForm(BaseModel):
    """
    Form for creating or updating a message.
    """

    temp_id: Optional[str] = None
    """Temporary ID for the message (used for optimistic UI updates)."""

    content: str
    """Content of the message."""

    reply_to_id: Optional[str] = None
    """ID of the message this message is replying to."""

    parent_id: Optional[str] = None
    """ID of the parent message if this is a thread reply."""

    data: Optional[dict] = None
    """Additional data associated with the message."""

    meta: Optional[dict] = None
    """Metadata associated with the message."""


class ReactionForm(BaseModel):
    """
    Form for adding or removing a reaction.
    """

    name: str
    """Name of the reaction (e.g., emoji or shortcode)."""


class Reactions(BaseModel):
    """
    Represents reactions to a message.
    """

    name: str
    """Name of the reaction."""

    users: List[dict]
    """List of users who reacted (contains 'id' and 'name')."""

    count: int
    """Total count of this reaction."""


class MessageUserResponse(MessageModel):
    """
    Message model with user details included.
    """

    user: Optional[UserNameResponse] = None
    """User who sent the message."""


class MessageReplyToResponse(MessageUserResponse):
    """
    Message model with user details and reply-to message details.
    """

    reply_to_message: Optional[MessageUserResponse] = None
    """The message this message is replying to."""


class MessageWithReactionsResponse(MessageUserResponse):
    """
    Message model with user details and reactions.
    """

    reactions: List[Reactions]
    """List of reactions to the message."""


class MessageResponse(MessageReplyToResponse):
    """
    Detailed message response including replies and reactions.
    """

    latest_reply_at: Optional[int] = None
    """Timestamp of the latest reply (epoch time)."""

    reply_count: int = 0
    """Number of replies to this message."""

    reactions: List[Reactions]
    """List of reactions to the message."""

