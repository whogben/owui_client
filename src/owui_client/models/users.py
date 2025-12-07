import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class UpdateProfileForm(BaseModel):
    """
    Form for updating a user's profile information.

    Note: This form is primarily used by the Auths router for profile updates,
    not by the Users router.
    """

    profile_image_url: str
    """The URL of the profile image."""

    name: str
    """The full name of the user."""

    bio: Optional[str] = None
    """A brief biography or description of the user."""

    gender: Optional[str] = None
    """The user's gender."""

    date_of_birth: Optional[datetime.date] = None
    """The user's date of birth."""


class UserSettings(BaseModel):
    """
    User settings configuration.

    This model stores various user preferences, primarily related to the UI.
    It allows extra fields to accommodate future settings without strict schema changes.
    """

    ui: Optional[dict] = {}
    """Dictionary containing UI-specific settings (e.g., theme, notifications)."""

    model_config = ConfigDict(extra="allow")


class UserModel(BaseModel):
    """
    Represents a user in the system.

    This is the main user model containing profile information, status, settings,
    and system metadata.
    """

    id: str
    """Unique identifier for the user."""

    name: str
    """The user's full name."""

    email: str
    """The user's email address."""

    username: Optional[str] = None
    """The user's username (optional)."""

    role: str = "pending"
    """The user's role. Common values: 'admin', 'user', 'pending'."""

    profile_image_url: Optional[str] = None
    """URL to the user's profile image."""

    profile_banner_image_url: Optional[str] = None
    """URL to the user's profile banner image."""

    bio: Optional[str] = None
    """User's biography."""

    gender: Optional[str] = None
    """User's gender."""

    date_of_birth: Optional[datetime.date] = None
    """User's date of birth."""

    timezone: Optional[str] = None
    """User's timezone."""

    presence_state: Optional[str] = None
    """Current presence state (e.g., 'online', 'idle')."""

    status_emoji: Optional[str] = None
    """Emoji representing the user's current status."""

    status_message: Optional[str] = None
    """Text message representing the user's current status."""

    status_expires_at: Optional[int] = None
    """Timestamp when the status message expires."""

    info: Optional[dict] = None
    """Additional user information dictionary."""

    settings: Optional[UserSettings] = None
    """User-specific settings."""

    api_key: Optional[str] = None
    """User's API key (if generated)."""

    oauth: Optional[dict] = None
    """OAuth provider data."""

    oauth_sub: Optional[str] = None
    """OAuth subject identifier."""

    last_active_at: int  # timestamp in epoch
    """Timestamp of the last user activity (Unix epoch)."""

    updated_at: int  # timestamp in epoch
    """Timestamp when the user was last updated (Unix epoch)."""

    created_at: int  # timestamp in epoch
    """Timestamp when the user was created (Unix epoch)."""

    model_config = ConfigDict(from_attributes=True)


class UserGroupIdsModel(UserModel):
    """
    User model with associated group IDs.
    """

    group_ids: list[str] = []
    """List of group IDs that the user belongs to."""


class UserGroupIdsListResponse(BaseModel):
    """
    Response model for listing users with their group IDs.
    """

    users: list[UserGroupIdsModel]
    """List of users with group IDs."""

    total: int
    """Total number of users matching the query."""


class UserModelResponse(UserModel):
    """
    User model response that allows extra fields.
    """

    model_config = ConfigDict(extra="allow")


class UserListResponse(BaseModel):
    """
    Response model for listing users.
    """

    users: list[UserModelResponse]
    """List of users."""

    total: int
    """Total number of users matching the query."""


class UserStatus(BaseModel):
    """
    User status information.
    """

    status_emoji: Optional[str] = None
    """Emoji status."""

    status_message: Optional[str] = None
    """Text status message."""

    status_expires_at: Optional[int] = None
    """Timestamp when the status expires (Unix epoch)."""


class UserInfoResponse(UserStatus):
    """
    Abbreviated user information including status.
    """

    id: str
    """User ID."""

    name: str
    """User name."""

    email: str
    """User email."""

    role: str
    """User role."""


class UserInfoListResponse(BaseModel):
    """
    Response model for listing abbreviated user info.
    """

    users: list[UserInfoResponse]
    """List of user info objects."""

    total: int
    """Total count of users."""


class ActiveUsersResponse(BaseModel):
    """
    Response model for listing active user IDs.
    """

    user_ids: list[str]
    """List of active user IDs."""


class UserActiveResponse(UserStatus):
    """
    User response including active status.
    """

    name: str
    """User name."""

    profile_image_url: Optional[str] = None
    """URL to profile image."""

    is_active: bool
    """Whether the user is currently active (based on recent activity)."""

    model_config = ConfigDict(extra="allow")


class UserIdNameResponse(BaseModel):
    """
    Minimal user response with ID and name.
    """

    id: str
    """User ID."""

    name: str
    """User name."""


class UserIdNameStatusResponse(UserStatus):
    """
    User response with ID, name, and active status.
    """

    id: str
    """User ID."""

    name: str
    """User name."""

    is_active: Optional[bool] = None
    """Whether the user is currently active."""


class UserIdNameListResponse(BaseModel):
    """
    Response model for listing users with ID and name.
    """

    users: list[UserIdNameResponse]
    """List of user objects (ID and name)."""

    total: int
    """Total number of users."""


class UserNameResponse(BaseModel):
    """
    User response with ID, name, and role.
    """

    id: str
    """User ID."""

    name: str
    """User name."""

    role: str
    """User role."""


class UserProfileImageResponse(UserNameResponse):
    """
    User response with profile image URL.
    """

    email: str
    """User email."""

    profile_image_url: str
    """URL to the user's profile image."""


class WorkspacePermissions(BaseModel):
    """
    Permissions related to workspace features.
    """

    models: bool = False
    """Access to models."""

    knowledge: bool = False
    """Access to knowledge base."""

    prompts: bool = False
    """Access to prompts."""

    tools: bool = False
    """Access to tools."""

    models_import: bool = False
    """Permission to import models."""

    models_export: bool = False
    """Permission to export models."""

    prompts_import: bool = False
    """Permission to import prompts."""

    prompts_export: bool = False
    """Permission to export prompts."""

    tools_import: bool = False
    """Permission to import tools."""

    tools_export: bool = False
    """Permission to export tools."""


class SharingPermissions(BaseModel):
    """
    Permissions related to sharing features.
    """

    models: bool = False
    """Can share models."""

    public_models: bool = False
    """Can share models publicly."""

    knowledge: bool = False
    """Can share knowledge."""

    public_knowledge: bool = False
    """Can share knowledge publicly."""

    prompts: bool = False
    """Can share prompts."""

    public_prompts: bool = False
    """Can share prompts publicly."""

    tools: bool = False
    """Can share tools."""

    public_tools: bool = True
    """Can share tools publicly (default True)."""

    notes: bool = False
    """Can share notes."""

    public_notes: bool = True
    """Can share notes publicly (default True)."""


class ChatPermissions(BaseModel):
    """
    Permissions related to chat functionality.
    """

    controls: bool = True
    """Access to chat controls."""

    valves: bool = True
    """Access to valves."""

    system_prompt: bool = True
    """Ability to edit system prompt."""

    params: bool = True
    """Ability to edit chat parameters."""

    file_upload: bool = True
    """Permission to upload files."""

    delete: bool = True
    """Permission to delete chats."""

    delete_message: bool = True
    """Permission to delete individual messages."""

    continue_response: bool = True
    """Permission to use 'continue' for responses."""

    regenerate_response: bool = True
    """Permission to regenerate responses."""

    rate_response: bool = True
    """Permission to rate responses."""

    edit: bool = True
    """Permission to edit messages."""

    share: bool = True
    """Permission to share chats."""

    export: bool = True
    """Permission to export chats."""

    stt: bool = True
    """Access to Speech-to-Text."""

    tts: bool = True
    """Access to Text-to-Speech."""

    call: bool = True
    """Access to call feature."""

    multiple_models: bool = True
    """Permission to use multiple models."""

    temporary: bool = True
    """Permission to use temporary chats."""

    temporary_enforced: bool = False
    """Whether temporary chat is enforced."""


class FeaturesPermissions(BaseModel):
    """
    Permissions related to general features.
    """

    api_keys: bool = False
    """Access to API keys."""

    direct_tool_servers: bool = False
    """Access to direct tool servers."""

    web_search: bool = True
    """Access to web search."""

    image_generation: bool = True
    """Access to image generation."""

    code_interpreter: bool = True
    """Access to code interpreter."""

    notes: bool = True
    """Access to notes."""

    channels: bool = True
    """Access to channels."""

    folders: bool = True
    """Access to folders."""


class UserPermissions(BaseModel):
    """
    Comprehensive user permissions.

    This model represents the structure of permissions returned by the system.
    It is used for default permissions configuration and user-specific permission checks.
    """

    workspace: WorkspacePermissions
    """Workspace-related permissions."""

    sharing: SharingPermissions
    """Sharing-related permissions."""

    chat: ChatPermissions
    """Chat-related permissions."""

    features: FeaturesPermissions
    """Feature-related permissions."""


class UserResponse(UserNameResponse):
    """
    User response with ID, name, role, and email.
    """

    email: str
    """User email."""


class UserUpdateForm(BaseModel):
    """
    Form for updating a user.
    """

    role: str
    """User role. Can be used to promote/demote users."""

    name: str
    """User name."""

    email: str
    """User email."""

    profile_image_url: str
    """Profile image URL."""

    password: Optional[str] = None
    """New password (optional). If provided, the user's password will be updated."""
