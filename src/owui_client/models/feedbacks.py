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
    """Content of the feedback, structure depends on 'type'."""

    meta: Optional[dict] = None
    """Metadata associated with the feedback (e.g., tags, context)."""

    snapshot: Optional[dict] = None
    """Snapshot of the context (e.g., chat history) when feedback was given."""

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
    """Content of the feedback."""

    meta: Optional[dict] = None
    """Metadata associated with the feedback."""

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
    """The state of the chat when feedback was submitted."""

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
    """Metadata for the feedback."""

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

