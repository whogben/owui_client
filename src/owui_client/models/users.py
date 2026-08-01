"""User models, forms, and API key management."""

import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


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
    """Dictionary containing UI-specific settings and preferences.

    Dict Fields:
        - `pinnedModels` (list[str], optional): List of model IDs pinned to the sidebar
        - `toolServers` (list[dict], optional): List of tool server configurations
        - `detectArtifacts` (bool, optional): Enable artifact detection in responses
        - `showUpdateToast` (bool, optional): Show update notification toasts
        - `showChangelog` (bool, optional): Show changelog notifications
        - `showEmojiInCall` (bool, optional): Show emoji during call interactions
        - `voiceInterruption` (bool, optional): Allow voice interruption during calls
        - `collapseCodeBlocks` (bool, optional): Collapse code blocks by default
        - `expandDetails` (bool, optional): Expand detail sections by default
        - `notificationSound` (bool, optional): Enable notification sounds
        - `notificationSoundAlways` (bool, optional): Always play notification sounds
        - `stylizedPdfExport` (bool, optional): Use stylized PDF export format
        - `notifications` (dict, optional): Notification configuration
        - `imageCompression` (bool, optional): Enable image compression
        - `imageCompressionSize` (any, optional): Image compression size settings
        - `textScale` (number, optional): Text scaling factor
        - `widescreenMode` (null, optional): Widescreen mode setting
        - `largeTextAsFile` (bool, optional): Treat large text as file attachments
        - `promptAutocomplete` (bool, optional): Enable prompt autocomplete
        - `hapticFeedback` (bool, optional): Enable haptic feedback
        - `responseAutoCopy` (any, optional): Auto-copy response settings
        - `richTextInput` (bool, optional): Enable rich text input
        - `params` (any, optional): Additional UI parameters
        - `userLocation` (any, optional): User location settings
        - `webSearch` (any, optional): Web search configuration
        - `memory` (bool, optional): Enable memory features
        - `autoTags` (bool, optional): Enable automatic tagging
        - `autoFollowUps` (bool, optional): Enable automatic follow-ups
        - `backgroundImageUrl` (null, optional): Background image URL
        - `landingPageMode` (str, optional): Landing page display mode
        - `iframeSandboxAllowForms` (bool, optional): Allow forms in iframe sandbox
        - `iframeSandboxAllowSameOrigin` (bool, optional): Allow same-origin in iframe sandbox
        - `scrollOnBranchChange` (bool, optional): Scroll on branch change
        - `directConnections` (null, optional): Direct connections setting
        - `chatBubble` (bool, optional): Show chat bubble interface
        - `copyFormatted` (bool, optional): Copy formatted text
        - `models` (list[str], optional): List of available model IDs
        - `conversationMode` (bool, optional): Enable conversation mode
        - `speechAutoSend` (bool, optional): Auto-send speech input
        - `responseAutoPlayback` (bool, optional): Auto-playback responses
        - `audio` (AudioSettings, optional): Audio settings configuration
        - `showUsername` (bool, optional): Show username in UI
        - `notificationEnabled` (bool, optional): Enable notifications
        - `highContrastMode` (bool, optional): Enable high contrast mode
        - `title` (TitleSettings, optional): Title settings configuration
        - `showChatTitleInTab` (bool, optional): Show chat title in browser tab
        - `splitLargeDeltas` (bool, optional): Split large delta updates
        - `chatDirection` (str, optional): Chat direction ('LTR', 'RTL', 'auto')
        - `ctrlEnterToSend` (bool, optional): Use Ctrl+Enter to send messages
        - `system` (str, optional): System configuration
        - `seed` (number, optional): Random seed value
        - `temperature` (str, optional): Temperature setting
        - `repeat_penalty` (str, optional): Repeat penalty value
        - `top_k` (str, optional): Top-k sampling value
        - `top_p` (str, optional): Top-p sampling value
        - `num_ctx` (str, optional): Context window size
        - `num_batch` (str, optional): Batch size
        - `num_keep` (str, optional): Number of tokens to keep
        - `options` (ModelOptions, optional): Model-specific options

    The `notifications` field contains:
        - `webhook_url` (str, optional): Webhook URL for notifications
    """

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
    """Additional user information dictionary.

    Dict Fields:
        - `location` (str, optional): User's location information, used for geolocation features and template variable replacement (e.g., {{USER_LOCATION}} in prompts)
        - Additional arbitrary key-value pairs may be stored as needed. This field is a flexible JSON storage that can contain any user-specific metadata.
    """

    variables: dict = Field(default_factory=dict, exclude=True)
    """Per-user template variables, substitutable in system prompts via `{{ user.variables.KEY }}`.

    Excluded from `UserModel` serialization (matches the backend `exclude=True`);
    read and written through the dedicated user-variables endpoints which expose
    it normalized to `dict[str, str]`.

    Dict Fields:
        - `<key>` (str): A variable value. Keys must match `^[a-z][a-z0-9_]*$` (lowercase, start with a letter, then lowercase alphanumerics/underscores); values must be strings of at most 20,000 characters and the total payload must be under 100,000 characters.
    """

    settings: Optional[UserSettings] = None
    """User-specific settings."""

    api_key: Optional[str] = None
    """User's API key (if generated)."""

    oauth: Optional[dict] = None
    """OAuth provider data.

    Dict Fields:
        - `google` (dict, optional): Google OAuth provider data
        - `github` (dict, optional): GitHub OAuth provider data
        - `microsoft` (dict, optional): Microsoft OAuth provider data
        - `oidc` (dict, optional): OpenID Connect OAuth provider data
        - `feishu` (dict, optional): Feishu OAuth provider data

    Each provider dictionary contains:
        - `sub` (str, required): Subject identifier from the OAuth provider
    """

    scim: Optional[dict] = None
    """SCIM provider data for external identity management.

    Dict Fields:
        - `microsoft` (dict, optional): Microsoft SCIM provider data
        - `okta` (dict, optional): Okta SCIM provider data

    Each provider dictionary contains:
        - `external_id` (str, required): External identifier from the SCIM provider
    """

    oauth_sub: Optional[str] = None
    """OAuth subject identifier."""

    last_active_at: int  # timestamp in epoch
    """Timestamp of the last user activity (Unix epoch)."""

    updated_at: int  # timestamp in epoch
    """Timestamp when the user was last updated (Unix epoch)."""

    created_at: int  # timestamp in epoch
    """Timestamp when the user was created (Unix epoch)."""

    model_config = ConfigDict(from_attributes=True)

    @field_validator("variables", mode="before")
    @classmethod
    def _normalize_variables(cls, value):
        """Coerce non-dict values (e.g. null) to an empty dict, mirroring the backend."""
        return value if isinstance(value, dict) else {}


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

    bio: Optional[str] = None
    """User's biography."""

    groups: Optional[list] = []
    """List of groups the user belongs to."""

    is_active: bool = False
    """Whether the user is currently active (based on recent activity)."""


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

    groups: Optional[list] = []
    """List of groups the user belongs to."""

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

    skills: bool = False
    """Access to skills."""

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

    skills_import: bool = False
    """Permission to import skills."""

    skills_export: bool = False
    """Permission to export skills."""


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

    skills: bool = False
    """Can share skills."""

    public_skills: bool = False
    """Can share skills publicly."""

    notes: bool = False
    """Can share notes."""

    public_notes: bool = True
    """Can share notes publicly (default True)."""

    folders: bool = False
    """Can share folders."""

    public_chats: bool = False
    """Can share chats publicly."""

    public_calendars: bool = False
    """Can share calendars publicly."""


class ChatPermissions(BaseModel):
    """
    Permissions related to chat functionality.

    The `import_` field is serialized under the JSON key `import` (a Pydantic
    alias) because `import` is a reserved Python keyword. With
    `populate_by_name=True`, the field accepts both the alias `import` and the
    field name `import_` on input.
    """

    model_config = ConfigDict(populate_by_name=True)

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

    web_upload: bool = True
    """Permission to upload content from the web."""

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

    import_: bool = Field(default=True, alias='import')
    """Permission to import chats. JSON key is `import` (Python keyword)."""

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

    memories: bool = True
    """Access to memories."""

    automations: bool = False
    """Access to automations."""

    calendar: bool = True
    """Access to calendar."""

    webhooks: bool = False
    """Access to user webhooks."""


class SettingsPermissions(BaseModel):
    """
    Permissions related to settings.
    """

    interface: bool = True
    """Access to interface settings."""


class AccessGrantsPermissions(BaseModel):
    """
    Permissions related to access grants.
    """

    allow_users: bool = True
    """Whether to allow users to grant access to others."""

    allow_groups: bool = True
    """Whether to allow groups to grant access to others."""


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

    settings: SettingsPermissions
    """Settings-related permissions."""

    access_grants: AccessGrantsPermissions
    """Access grants related permissions."""


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


class ResourcePreviewItem(BaseModel):
    """
    Minimal resource reference (id, name) used in preview responses.
    """

    id: str
    """Unique identifier of the resource."""

    name: str
    """Display name of the resource."""


class ResourcePreviewList(BaseModel):
    """
    Wrapper for a list of accessible resources plus a total count.
    """

    items: List[ResourcePreviewItem]
    """List of accessible resources the principal can read."""

    total: int
    """Total number of resources of this type in the system (active for models)."""


class UserPreviewUser(BaseModel):
    """
    User reference embedded in the user preview response.
    """

    id: str
    """Unique identifier of the user."""

    name: str
    """Display name of the user."""


class UserPreview(BaseModel):
    """
    Response model for the user preview endpoint.

    Shows what resources a specific user can access across all of their groups.
    Returned by `GET /v1/users/{user_id}/preview` (admin-only).
    """

    user: UserPreviewUser
    """The user being previewed."""

    groups: List[ResourcePreviewItem] = []
    """List of groups the user belongs to."""

    models: ResourcePreviewList
    """Models accessible to the user (active models only) with total count."""

    knowledge: ResourcePreviewList
    """Knowledge bases accessible to the user with total count."""

    tools: ResourcePreviewList
    """Tools accessible to the user with total count."""


class UserVariablesForm(BaseModel):
    """
    Request body for updating the calling user's variables.

    Sent to `POST /v1/users/user/variables/update`. The backend validates each
    key/value and rejects the request with HTTP 400 on invalid input.
    """

    variables: dict = Field(default_factory=dict)
    """Variables to store for the calling user.

    Dict Fields:
        - `<key>` (str, optional): A variable value. Keys must match `^[a-z][a-z0-9_]*$` (lowercase, start with a letter, then lowercase alphanumerics/underscores); values must be strings of at most 20,000 characters and the total payload must be under 100,000 characters. Invalid keys or non-string values are rejected with HTTP 400.
    """


class UserVariablesResponse(BaseModel):
    """
    Response for the user-variables endpoints.

    Returned by `GET /v1/users/user/variables` and
    `POST /v1/users/user/variables/update`. Variables are normalized to
    `dict[str, str]`: only string keys with string values are retained.
    """

    variables: dict[str, str] = Field(default_factory=dict)
    """The calling user's variables, normalized to string keys and string values.

    Dict Fields:
        - `<key>` (str): A variable value. Keys match `^[a-z][a-z0-9_]*$`; values are strings. Referenced in system prompts via `{{ user.variables.KEY }}`.
    """


class UserUsageTotals(BaseModel):
    """
    Aggregate usage totals for the calling user.

    `lifetime_tokens`, `input_tokens`, `output_tokens`, `models_used`,
    `total_chats`, and `longest_chat_seconds` are lifetime values; `messages`,
    `user_messages`, `assistant_messages`, `active_days`, `peak_daily_tokens`,
    and the streaks are scoped to the requested period.
    """

    lifetime_tokens: int = 0
    """Total tokens consumed across all time."""

    input_tokens: int = 0
    """Input/prompt tokens (lifetime)."""

    output_tokens: int = 0
    """Output/completion tokens (lifetime)."""

    peak_daily_tokens: int = 0
    """Highest single-day token count within the period."""

    longest_chat_seconds: int = 0
    """Duration of the longest single chat, in seconds (lifetime)."""

    current_streak: int = 0
    """Current consecutive-day activity streak (period)."""

    longest_streak: int = 0
    """Longest consecutive-day activity streak observed (period)."""

    total_chats: int = 0
    """Total number of chats attributable to the user (lifetime)."""

    active_days: int = 0
    """Distinct days with activity in the period."""

    models_used: int = 0
    """Number of distinct models the user has used (lifetime)."""

    messages: int = 0
    """Total messages (user + assistant) in the period."""

    user_messages: int = 0
    """Messages authored by the user in the period."""

    assistant_messages: int = 0
    """Messages authored by the assistant in the period."""


class UserUsageHeatmapEntry(BaseModel):
    """
    One day (or one aggregated week) of activity in a usage heatmap.
    """

    date: str
    """Calendar date (or week-start date) as `YYYY-MM-DD`."""

    messages: int = 0
    """Total messages on that day."""

    chats: int = 0
    """Distinct chats with activity on that day."""

    tokens: int = 0
    """Total tokens consumed on that day."""

    models: dict[str, int] = Field(default_factory=dict)
    """Per-model message counts for that day.

    Dict Fields:
        - `<model_id>` (int): Number of messages sent using this model on that day.
    """


class UserUsageModelEntry(BaseModel):
    """
    Usage breakdown for a single model within the period.
    """

    model_id: str
    """Identifier of the model."""

    messages: int = 0
    """Messages sent using this model."""

    input_tokens: int = 0
    """Input tokens attributed to this model."""

    output_tokens: int = 0
    """Output tokens attributed to this model."""

    total_tokens: int = 0
    """Total tokens (input + output) attributed to this model."""


class UserUsageToolEntry(BaseModel):
    """
    Invocation count for a single tool within the period.
    """

    name: str
    """Tool name/identifier."""

    count: int
    """Number of times the tool was invoked."""


class UserUsageInsights(BaseModel):
    """
    Derived summary insights for the period.
    """

    most_used_model: Optional[str] = None
    """Model id with the most messages in the period, or null if none."""

    average_tokens_per_chat: float = 0
    """Lifetime tokens divided by total chats (rounded to 1 decimal)."""

    average_messages_per_active_day: float = 0
    """Period messages divided by active days (rounded to 1 decimal)."""

    user_message_share: float = 0
    """Percentage (0-100) of messages authored by the user."""

    assistant_message_share: float = 0
    """Percentage (0-100) of messages authored by the assistant."""


class UserUsagePeriod(BaseModel):
    """
    The inclusive time window covered by the usage report.
    """

    start_date: int
    """Period start as a Unix epoch timestamp (seconds)."""

    end_date: int
    """Period end as a Unix epoch timestamp (seconds)."""

    days: int
    """Number of days spanned (inclusive): floor((end-start)/86400) + 1, minimum 1."""


class UserUsageResponse(BaseModel):
    """
    Response for `GET /v1/users/usage`.

    Combines totals, daily/weekly/cumulative activity heatmaps, derived
    insights, and top models/tools for the calling user over a period.
    """

    totals: UserUsageTotals
    """Aggregate lifetime and period totals."""

    heatmap: list[UserUsageHeatmapEntry]
    """Daily activity entries within the period."""

    weekly_heatmap: list[UserUsageHeatmapEntry]
    """Activity aggregated by ISO week (week-start Monday)."""

    cumulative_heatmap: list[UserUsageHeatmapEntry]
    """Daily activity with running cumulative counts."""

    insights: UserUsageInsights
    """Derived summary metrics for the period."""

    top_models: list[UserUsageModelEntry]
    """Models ranked by usage in the period (most messages first)."""

    top_tools: list[UserUsageToolEntry] = []
    """Tools ranked by invocation count in the period."""

    period: UserUsagePeriod
    """The time window the report covers."""
