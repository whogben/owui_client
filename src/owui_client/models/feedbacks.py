from typing import Optional
from pydantic import BaseModel, ConfigDict


class FeedbackModel(BaseModel):
    """
    Represents a feedback entry in the database.
    """

    id: str
    """Unique identifier for the feedback."""

    user_id: str
    """ID of the user who submitted the feedback."""

    version: int
    """Schema version of the feedback."""

    type: str
    """Type of feedback (e.g., 'rating', 'comment')."""

    data: Optional[dict] = None
    """Content of the feedback, structure depends on 'type'.

    Dict Fields:
        - `model_id` (str, optional): ID of the model being rated
        - `rating` (str|int, optional): The rating value (e.g., 1, 0, -1 for win/draw/lose)
        - `sibling_model_ids` (list[str], optional): IDs of sibling models in comparison scenarios (e.g., arena)
        - `tags` (list[str], optional): Tags associated with the feedback
        - `reason` (str, optional): Reason for the rating
        - `comment` (str, optional): Additional comment provided by the user
    """

    meta: Optional[dict] = None
    """Metadata associated with the feedback.

    Dict Fields:
        - `arena` (bool, optional): Whether the feedback is related to the arena feature
        - `chat_id` (str, optional): ID of the chat session where feedback was given
        - `message_id` (str, optional): ID of the message being rated or commented on
        - `tags` (list[str], optional): Tags associated with the feedback
        - `model_id` (str, optional): ID of the model being rated
        - `message_index` (int, optional): Index of the message in the chat history
        - `base_models` (dict[str, str], optional): Mapping of model IDs to their base model IDs
    """

    snapshot: Optional[dict] = None
    """Snapshot of the context (e.g., chat history) when feedback was given.

    Dict Fields:
        - `chat` (dict, optional): Complete chat object containing the conversation state
        - `chat.chat` (dict, optional): Nested chat data structure
        - `chat.chat.history` (dict, optional): Chat history information
        - `chat.chat.history.messages` (dict[str, object], optional): Message history mapping message IDs to message objects
        - `chat.chat.history.messages[*].parentId` (str, optional): ID of parent message
        - `chat.chat.history.messages[*].childrenIds` (list[str], optional): List of child message IDs
        - `chat.chat.history.messages[*].content` (str, optional): Message content text
        - `chat.chat.history.messages[*].role` (str, optional): Message role (e.g., 'user', 'assistant')
        - `chat.chat.history.messages[*].model` (str, optional): Model used for the message
        - `chat.chat.history.messages[*].done` (bool, optional): Whether message processing is complete
    """

    created_at: int
    """Timestamp when feedback was created (epoch)."""

    updated_at: int
    """Timestamp when feedback was last updated (epoch)."""

    model_config = ConfigDict(from_attributes=True)


class FeedbackResponse(BaseModel):
    """
    Response model for feedback items.
    """

    id: str
    """Unique identifier for the feedback."""

    user_id: str
    """ID of the user who submitted the feedback."""

    version: int
    """Schema version of the feedback."""

    type: str
    """Type of feedback (e.g., 'rating', 'comment')."""

    data: Optional[dict] = None
    """Content of the feedback, structure depends on 'type'.

    Dict Fields:
        - `model_id` (str, optional): ID of the model being rated
        - `rating` (str|int, optional): The rating value (e.g., 1, 0, -1 for win/draw/lose)
        - `sibling_model_ids` (list[str], optional): IDs of sibling models in comparison scenarios (e.g., arena)
        - `tags` (list[str], optional): Tags associated with the feedback
        - `reason` (str, optional): Reason for the rating
        - `comment` (str, optional): Additional comment provided by the user
    """

    meta: Optional[dict] = None
    """Metadata associated with the feedback.

    Dict Fields:
        - `arena` (bool, optional): Whether the feedback is related to the arena feature
        - `chat_id` (str, optional): ID of the chat session where feedback was given
        - `message_id` (str, optional): ID of the message being rated or commented on
        - `tags` (list[str], optional): Tags associated with the feedback
        - `model_id` (str, optional): ID of the model being rated
        - `message_index` (int, optional): Index of the message in the chat history
        - `base_models` (dict[str, str], optional): Mapping of model IDs to their base model IDs
    """

    snapshot: Optional[dict] = None
    """Snapshot of the context (e.g., chat history) when feedback was given.

    Dict Fields:
        - `chat` (dict, optional): Complete chat object containing the conversation state
        - `chat.chat` (dict, optional): Nested chat data structure
        - `chat.chat.history` (dict, optional): Chat history information
        - `chat.chat.history.messages` (dict[str, object], optional): Message history mapping message IDs to message objects
        - `chat.chat.history.messages[*].parentId` (str, optional): ID of parent message
        - `chat.chat.history.messages[*].childrenIds` (list[str], optional): List of child message IDs
        - `chat.chat.history.messages[*].content` (str, optional): Message content text
        - `chat.chat.history.messages[*].role` (str, optional): Message role (e.g., 'user', 'assistant')
        - `chat.chat.history.messages[*].model` (str, optional): Model used for the message
        - `chat.chat.history.messages[*].done` (bool, optional): Whether message processing is complete
    """

    created_at: int
    """Timestamp when feedback was created (epoch)."""

    updated_at: int
    """Timestamp when feedback was last updated (epoch)."""


class RatingData(BaseModel):
    """
    Data structure for rating-type feedback.
    """

    rating: Optional[str | int] = None
    """The rating value (e.g., 1-5, 'thumbs_up')."""

    model_id: Optional[str] = None
    """ID of the model being rated."""

    sibling_model_ids: Optional[list[str]] = None
    """IDs of sibling models in comparison scenarios (e.g., arena)."""

    reason: Optional[str] = None
    """Reason for the rating."""

    comment: Optional[str] = None
    """Additional comment provided by the user."""

    model_config = ConfigDict(extra="allow", protected_namespaces=())


class MetaData(BaseModel):
    """
    Metadata for feedback entries.
    """

    arena: Optional[bool] = None
    """Whether the feedback is related to the arena feature."""

    chat_id: Optional[str] = None
    """ID of the chat session where feedback was given."""

    message_id: Optional[str] = None
    """ID of the message being rated or commented on."""

    tags: Optional[list[str]] = None
    """Tags associated with the feedback."""

    model_config = ConfigDict(extra="allow")


class SnapshotData(BaseModel):
    """
    Snapshot data capturing context at the time of feedback.
    """

    chat: Optional[dict] = None
    """The state of the chat when feedback was submitted.

    Dict Fields:
        - `chat` (dict, optional): Nested chat data structure
        - `chat.chat` (dict, optional): Chat data structure
        - `chat.chat.history` (dict, optional): Chat history information
        - `chat.chat.history.messages` (dict[str, object], optional): Message history mapping message IDs to message objects
        - `chat.chat.history.messages[*].parentId` (str, optional): ID of parent message
        - `chat.chat.history.messages[*].childrenIds` (list[str], optional): List of child message IDs
        - `chat.chat.history.messages[*].content` (str, optional): Message content text
        - `chat.chat.history.messages[*].role` (str, optional): Message role (e.g., 'user', 'assistant')
        - `chat.chat.history.messages[*].model` (str, optional): Model used for the message
        - `chat.chat.history.messages[*].done` (bool, optional): Whether message processing is complete
    """

    model_config = ConfigDict(extra="allow")


class FeedbackForm(BaseModel):
    """
    Form for creating or updating feedback.
    """

    type: str
    """Type of feedback (e.g., 'rating')."""

    data: Optional[RatingData] = None
    """Specific data for the feedback type."""

    meta: Optional[dict] = None
    """Metadata associated with the feedback.

    Dict Fields:
        - `arena` (bool, optional): Whether the feedback is related to the arena feature
        - `chat_id` (str, optional): ID of the chat session where feedback was given
        - `message_id` (str, optional): ID of the message being rated or commented on
        - `tags` (list[str], optional): Tags associated with the feedback
        - `model_id` (str, optional): ID of the model being rated
        - `message_index` (int, optional): Index of the message in the chat history
        - `base_models` (dict[str, str], optional): Mapping of model IDs to their base model IDs
    """

    snapshot: Optional[SnapshotData] = None
    """Context snapshot."""

    model_config = ConfigDict(extra="allow")


class UserResponse(BaseModel):
    """
    User details associated with feedback.
    """

    id: str
    """User ID."""

    name: str
    """User's display name."""

    email: str
    """User's email address."""

    role: str = "pending"
    """User's role (e.g., 'admin', 'user')."""

    last_active_at: int  # timestamp in epoch
    """Timestamp of last activity (epoch)."""

    updated_at: int  # timestamp in epoch
    """Timestamp of last update (epoch)."""

    created_at: int  # timestamp in epoch
    """Timestamp of account creation (epoch)."""

    model_config = ConfigDict(from_attributes=True)


class FeedbackUserResponse(FeedbackResponse):
    """
    Feedback response including user details.
    """

    user: Optional[UserResponse] = None
    """The user who submitted the feedback."""


class FeedbackListResponse(BaseModel):
    """
    Response model for a list of feedbacks with pagination.
    """

    items: list[FeedbackUserResponse]
    """List of feedback items."""

    total: int
    """Total number of feedbacks matching the query."""
