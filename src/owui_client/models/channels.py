from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from owui_client.models.users import UserIdNameStatusResponse, UserListResponse

class ChannelModel(BaseModel):
    """
    Channel model representing a communication channel.
    """
    model_config = ConfigDict(from_attributes=True)

    id: str
    """Unique identifier for the channel."""

    user_id: str
    """ID of the user who created the channel."""

    type: Optional[str] = None
    """Type of the channel. Can be 'group', 'dm', or None for standard channels."""

    name: str
    """Name of the channel."""

    description: Optional[str] = None
    """Description of the channel."""

    is_private: Optional[bool] = None
    """Indicates if the channel is private (typically used for 'group' type channels)."""

    data: Optional[dict] = None
    """Additional arbitrary data for the channel."""

    meta: Optional[dict] = None
    """Metadata associated with the channel."""

    access_control: Optional[dict] = None
    """Access control settings for the channel."""

    created_at: int  # timestamp in epoch (time_ns)
    """Timestamp when the channel was created (in nanoseconds)."""

    updated_at: int  # timestamp in epoch (time_ns)
    """Timestamp when the channel was last updated (in nanoseconds)."""

    updated_by: Optional[str] = None
    """ID of the user who last updated the channel."""

    archived_at: Optional[int] = None  # timestamp in epoch (time_ns)
    """Timestamp when the channel was archived (in nanoseconds)."""

    archived_by: Optional[str] = None
    """ID of the user who archived the channel."""

    deleted_at: Optional[int] = None  # timestamp in epoch (time_ns)
    """Timestamp when the channel was deleted (in nanoseconds)."""

    deleted_by: Optional[str] = None
    """ID of the user who deleted the channel."""


class ChannelMemberModel(BaseModel):
    """
    Model representing a member's relationship with a channel.
    """
    model_config = ConfigDict(from_attributes=True)

    id: str
    """Unique identifier for the membership record."""

    channel_id: str
    """ID of the channel."""

    user_id: str
    """ID of the user."""

    role: Optional[str] = None
    """Role of the user in the channel (e.g., 'manager')."""

    status: Optional[str] = None
    """Status of the membership (e.g., 'joined', 'left')."""

    is_active: bool = True
    """Whether the user is currently an active member of the channel."""

    is_channel_muted: bool = False
    """Whether the user has muted the channel."""

    is_channel_pinned: bool = False
    """Whether the user has pinned the channel."""

    data: Optional[dict] = None
    """Additional arbitrary data for the membership."""

    meta: Optional[dict] = None
    """Metadata associated with the membership."""

    invited_at: Optional[int] = None  # timestamp in epoch (time_ns)
    """Timestamp when the user was invited (in nanoseconds)."""

    invited_by: Optional[str] = None
    """ID of the user who invited this member."""

    joined_at: Optional[int] = None  # timestamp in epoch (time_ns)
    """Timestamp when the user joined the channel (in nanoseconds)."""

    left_at: Optional[int] = None  # timestamp in epoch (time_ns)
    """Timestamp when the user left the channel (in nanoseconds)."""

    last_read_at: Optional[int] = None  # timestamp in epoch (time_ns)
    """Timestamp when the user last read the channel (in nanoseconds)."""

    created_at: Optional[int] = None  # timestamp in epoch (time_ns)
    """Timestamp when the membership record was created (in nanoseconds)."""

    updated_at: Optional[int] = None  # timestamp in epoch (time_ns)
    """Timestamp when the membership record was last updated (in nanoseconds)."""


class ChannelWebhookModel(BaseModel):
    """
    Model representing a webhook associated with a channel.
    """
    model_config = ConfigDict(from_attributes=True)

    id: str
    """Unique identifier for the webhook."""

    channel_id: str
    """ID of the channel the webhook belongs to."""

    user_id: str
    """ID of the user who created the webhook."""

    name: str
    """Name of the webhook."""

    profile_image_url: Optional[str] = None
    """URL of the profile image for the webhook."""

    token: str
    """Authentication token for the webhook."""

    last_used_at: Optional[int] = None  # timestamp in epoch (time_ns)
    """Timestamp when the webhook was last used (in nanoseconds)."""

    created_at: int  # timestamp in epoch (time_ns)
    """Timestamp when the webhook was created (in nanoseconds)."""

    updated_at: int  # timestamp in epoch (time_ns)
    """Timestamp when the webhook was last updated (in nanoseconds)."""


class ChannelForm(BaseModel):
    """
    Form for updating a channel.
    """
    name: str = ""
    """Name of the channel."""

    description: Optional[str] = None
    """Description of the channel."""

    is_private: Optional[bool] = None
    """Whether the channel is private."""

    data: Optional[dict] = None
    """Additional arbitrary data."""

    meta: Optional[dict] = None
    """Metadata."""

    access_control: Optional[dict] = None
    """Access control settings."""

    group_ids: Optional[list[str]] = None
    """List of group IDs (primarily used during creation to add members)."""

    user_ids: Optional[list[str]] = None
    """List of user IDs (primarily used during creation to add members)."""


class CreateChannelForm(ChannelForm):
    """
    Form for creating a new channel.
    """
    type: Optional[str] = None
    """Type of the channel (e.g., 'group', 'dm'). If None, creates a standard channel."""


class ChannelResponse(ChannelModel):
    """
    Extended channel model with user-specific permissions and stats.
    """
    is_manager: bool = False
    """Whether the current user is a manager of the channel."""

    write_access: bool = False
    """Whether the current user has write access to the channel."""

    user_count: Optional[int] = None
    """Total number of users in the channel."""


# Router-level models

class ChannelListItemResponse(ChannelModel):
    """
    Response model for listing channels.
    """
    user_ids: Optional[list[str]] = None  # 'dm' channels only
    """List of user IDs in the channel (typically for 'dm' channels)."""

    users: Optional[list[UserIdNameStatusResponse]] = None  # 'dm' channels only
    """List of user details in the channel (typically for 'dm' channels)."""

    last_message_at: Optional[int] = None  # timestamp in epoch (time_ns)
    """Timestamp of the last message in the channel (in nanoseconds)."""

    unread_count: int = 0
    """Number of unread messages for the current user."""


class ChannelFullResponse(ChannelResponse):
    """
    Full channel response with detailed member information.
    """
    user_ids: Optional[list[str]] = None  # 'group'/'dm' channels only
    """List of user IDs in the channel."""

    users: Optional[list[UserIdNameStatusResponse]] = None  # 'group'/'dm' channels only
    """List of user details in the channel."""

    last_read_at: Optional[int] = None  # timestamp in epoch (time_ns)
    """Timestamp when the current user last read the channel."""

    unread_count: int = 0
    """Number of unread messages for the current user."""


class UpdateActiveMemberForm(BaseModel):
    """
    Form for updating a member's active status.
    """
    is_active: bool
    """New active status."""


class UpdateMembersForm(BaseModel):
    """
    Form for adding members to a channel.
    """
    user_ids: list[str] = []
    """List of user IDs to add."""

    group_ids: list[str] = []
    """List of group IDs to add (adds all members of these groups)."""


class RemoveMembersForm(BaseModel):
    """
    Form for removing members from a channel.
    """
    user_ids: list[str] = []
    """List of user IDs to remove."""

