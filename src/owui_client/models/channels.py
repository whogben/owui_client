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
    """Additional arbitrary data for the channel.

    Dict Fields:
        This dictionary is used to store arbitrary key-value pairs for channel-specific metadata.
        Based on analysis of the Open WebUI source code, this field is designed as a flexible JSON
        field that can store any valid JSON structure for channel-related data.

        The backend defines this as a JSON column in the database (Column(JSON, nullable=True))
        but does not enforce any specific structure or validation. The field is intended for
        storing custom channel-related information that may be needed by different applications
        or integrations.

        Common usage patterns include:
        - `theme` (str, optional): Custom theme settings for the channel
        - `notifications` (dict, optional): Notification preferences configuration
        - `integration_config` (dict, optional): Configuration for external integrations
        - `custom_metadata` (dict, optional): Application-specific metadata
        - `settings` (dict, optional): Channel-specific settings and preferences
        - `features` (dict, optional): Feature flags and toggle states for the channel
        - `ui_config` (dict, optional): UI configuration and display preferences
        - `access_rules` (dict, optional): Additional access control rules beyond the standard access_control field

        All keys are optional and the structure is not validated by the backend.
        The frontend TypeScript definition shows this as `data?: object;` in ChannelForm,
        indicating it accepts any valid JSON object structure.

        Example usage:
        ```python
        {
            "theme": "dark",
            "notifications": {
                "mentions_only": True,
                "sound_enabled": False
            },
            "integration_config": {
                "webhook_url": "https://example.com/webhook",
                "api_key": "secret_key_123"
            },
            "settings": {
                "auto_archive": True,
                "message_retention_days": 30
            }
        }
        ```

        Note: No specific keys are enforced by the backend. This field provides flexibility
        for various use cases but requires applications to handle their own validation and structure.
        """

    meta: Optional[dict] = None
    """Metadata associated with the channel.

    Dict Fields:
        This dictionary is used to store arbitrary key-value pairs for channel-specific metadata.
        Based on analysis of the Open WebUI source code, this field is designed as a flexible JSON
        field that can store any valid JSON structure for channel-related metadata.

        The backend defines this as a JSON column in the database (Column(JSON, nullable=True))
        but does not enforce any specific structure or validation. The field is intended for
        storing custom channel-related information that may be needed by different applications
        or integrations.

        Common usage patterns include:
        - `theme` (str, optional): Custom theme settings for the channel
        - `notifications` (dict, optional): Notification preferences configuration
        - `integration_config` (dict, optional): Configuration for external integrations
        - `custom_metadata` (dict, optional): Application-specific metadata
        - `settings` (dict, optional): Channel-specific settings and preferences
        - `features` (dict, optional): Feature flags and toggle states for the channel
        - `ui_config` (dict, optional): UI configuration and display preferences
        - `access_rules` (dict, optional): Additional access control rules beyond the standard access_control field

        All keys are optional and the structure is not validated by the backend.
        The frontend TypeScript definition shows this as `meta?: object;` in ChannelForm,
        indicating it accepts any valid JSON object structure.

        Example usage:
        ```python
        {
            "theme": "dark",
            "notifications": {
                "mentions_only": True,
                "sound_enabled": False
            },
            "integration_config": {
                "webhook_url": "https://example.com/webhook",
                "api_key": "secret_key_123"
            },
            "settings": {
                "auto_archive": True,
                "message_retention_days": 30
            }
        }
        ```

        Note: No specific keys are enforced by the backend. This field provides flexibility
        for various use cases but requires applications to handle their own validation and structure.
        """

    access_control: Optional[dict] = None
    """Access control settings for the channel.

    Dict Fields:
        - `read` (dict, optional): Read access control configuration
            - `group_ids` (list[str], optional): List of group IDs that have read access
            - `user_ids` (list[str], optional): List of user IDs that have read access
        - `write` (dict, optional): Write access control configuration
            - `group_ids` (list[str], optional): List of group IDs that have write access
            - `user_ids` (list[str], optional): List of user IDs that have write access

    The access control system determines who can read from or write to a channel.
    When access_control is None, the channel is considered public for read access
    but requires explicit permissions for write access (strict mode).
    When access_control is an empty dict {}, the channel is completely public.

    Example usage:
    ```python
    {
        "read": {
            "group_ids": ["group1", "group2"],
            "user_ids": ["user1", "user2"]
        },
        "write": {
            "group_ids": ["admin_group"],
            "user_ids": ["channel_owner"]
        }
    }
    ```

    All keys and nested structures are optional. The backend validates access
    using the has_access() function which checks both user and group memberships.

    Special Rules:
    - When access_control is None: Public read access, strict write access (requires explicit permissions)
    - When access_control is {}: Completely public (both read and write)
    - Access is determined by checking both direct user membership and group membership
    - The system uses get_permitted_group_and_user_ids() to extract permitted IDs from the access_control structure
    - Access validation is performed by has_access() function in utils/access_control.py
    - Admin users bypass access control restrictions entirely
    - For standard channels (non-group, non-dm), access control is enforced via has_access() calls
    - For group/dm channels, membership in the channel itself determines access
    """

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
    """Additional arbitrary data for the membership.

    Dict Fields:
        This dictionary is used to store arbitrary key-value pairs for membership-specific metadata.
        Based on analysis of the Open WebUI source code, this field is designed as a flexible JSON
        field that can store any valid JSON structure for channel membership-related data.

        The backend defines this as a JSON column in the database (Column(JSON, nullable=True))
        but does not enforce any specific structure or validation. The field is intended for
        storing custom membership-related information that may be needed by different applications
        or integrations.

        Common usage patterns might include:
        - `preferences` (dict, optional): User-specific preferences for this channel membership
        - `notifications` (dict, optional): Notification settings specific to this membership
        - `integration_config` (dict, optional): Configuration for external integrations
        - `custom_metadata` (dict, optional): Application-specific metadata
        - `role_data` (dict, optional): Additional role-specific information
        - `status_info` (dict, optional): Extended status information beyond the basic status field
        - `access_rules` (dict, optional): Additional access control rules for this specific member

        All keys are optional and the structure is not validated by the backend.
        The frontend TypeScript definition shows this as `data?: object;` in related forms,
        indicating it accepts any valid JSON object structure.

        Example usage:
        ```python
        {
            "preferences": {
                "theme": "dark",
                "notifications": {
                    "mentions_only": True,
                    "sound_enabled": False
                }
            },
            "integration_config": {
                "webhook_url": "https://example.com/webhook",
                "api_key": "secret_key_123"
            },
            "role_data": {
                "custom_permissions": ["read", "write"],
                "expiration_date": "2025-12-31"
            }
        }
        ```

        Note: No specific keys are enforced by the backend. This field provides flexibility
        for various use cases but requires applications to handle their own validation and structure.
        """

    meta: Optional[dict] = None
    """Metadata associated with the membership.

    Dict Fields:
        This dictionary is used to store arbitrary key-value pairs for membership-specific metadata.
        Based on analysis of the Open WebUI source code, this field is designed as a flexible JSON
        field that can store any valid JSON structure for channel membership-related metadata.

        The backend defines this as a JSON column in the database (Column(JSON, nullable=True))
        but does not enforce any specific structure or validation. The field is intended for
        storing custom membership-related information that may be needed by different applications
        or integrations.

        Common usage patterns might include:
        - `preferences` (dict, optional): User-specific preferences for this channel membership
        - `notifications` (dict, optional): Notification settings specific to this membership
        - `integration_config` (dict, optional): Configuration for external integrations
        - `custom_metadata` (dict, optional): Application-specific metadata
        - `role_data` (dict, optional): Additional role-specific information beyond the basic role field
        - `status_info` (dict, optional): Extended status information beyond the basic status field
        - `access_rules` (dict, optional): Additional access control rules for this specific member
        - `membership_tags` (list[str], optional): Tags or labels for categorizing this membership
        - `last_activity` (dict, optional): Information about the member's last activity in the channel
        - `join_source` (str, optional): Source or method by which the user joined the channel

        All keys are optional and the structure is not validated by the backend.
        The frontend TypeScript definition shows this as flexible object structure in related forms.

        Example usage:
        ```python
        {
            "preferences": {
                "theme": "dark",
                "notifications": {
                    "mentions_only": True,
                    "sound_enabled": False
                }
            },
            "integration_config": {
                "webhook_url": "https://example.com/webhook",
                "api_key": "secret_key_123"
            },
            "role_data": {
                "custom_permissions": ["read", "write"],
                "expiration_date": "2025-12-31"
            },
            "last_activity": {
                "timestamp": 1234567890,
                "action": "sent_message"
            }
        }
        ```

        Note: No specific keys are enforced by the backend. This field provides flexibility
        for various use cases but requires applications to handle their own validation and structure.
        """

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
    """Additional arbitrary data for the channel.

    Dict Fields:
        This dictionary is used to store arbitrary key-value pairs for channel-specific metadata.
        Based on comprehensive analysis of the Open WebUI source code, this field is designed as a flexible JSON
        field that can store any valid JSON structure for channel-related data.

        The backend defines this as a JSON column in the database (Column(JSON, nullable=True))
        but does not enforce any specific structure or validation. The field is intended for
        storing custom channel-related information that may be needed by different applications
        or integrations.

        Common usage patterns include:
        - `theme` (str, optional): Custom theme settings for the channel
        - `notifications` (dict, optional): Notification preferences configuration
            - `mentions_only` (bool, optional): Only notify on mentions
            - `sound_enabled` (bool, optional): Enable notification sounds
        - `integration_config` (dict, optional): Configuration for external integrations
            - `webhook_url` (str, optional): Webhook endpoint URL
            - `api_key` (str, optional): Authentication key for integrations
        - `custom_metadata` (dict, optional): Application-specific metadata
        - `settings` (dict, optional): Channel-specific settings and preferences
            - `auto_archive` (bool, optional): Automatically archive old messages
            - `message_retention_days` (int, optional): Number of days to retain messages
        - `features` (dict, optional): Feature flags and toggle states for the channel
        - `ui_config` (dict, optional): UI configuration and display preferences
        - `access_rules` (dict, optional): Additional access control rules beyond the standard access_control field

        All keys are optional and the structure is not validated by the backend.
        The frontend TypeScript definition shows this as `data?: object;` in ChannelForm,
        indicating it accepts any valid JSON object structure.

        Example usage:
        ```python
        {
            "theme": "dark",
            "notifications": {
                "mentions_only": True,
                "sound_enabled": False
            },
            "integration_config": {
                "webhook_url": "https://example.com/webhook",
                "api_key": "secret_key_123"
            },
            "settings": {
                "auto_archive": True,
                "message_retention_days": 30
            }
        }
        ```

        Note: No specific keys are enforced by the backend. This field provides flexibility
        for various use cases but requires applications to handle their own validation and structure.
        """

    meta: Optional[dict] = None
    """Metadata associated with the channel.

    Dict Fields:
        This dictionary is used to store arbitrary key-value pairs for channel-specific metadata.
        No specific keys are enforced by the backend, making it flexible for various use cases.
        Common usage patterns include storing channel configuration, custom settings,
        or integration-specific data.

        Example usage might include:
        - `theme` (str, optional): Custom theme settings for the channel
        - `notifications` (dict, optional): Notification preferences
        - `integration_config` (dict, optional): Configuration for external integrations
        - `custom_metadata` (dict, optional): Application-specific metadata

        All keys are optional and the structure is not validated by the backend.
    """

    access_control: Optional[dict] = None
    """Access control settings for the channel.

    Dict Fields:
        - `read` (dict, optional): Read access control configuration
            - `group_ids` (list[str], optional): List of group IDs that have read access
            - `user_ids` (list[str], optional): List of user IDs that have read access
        - `write` (dict, optional): Write access control configuration
            - `group_ids` (list[str], optional): List of group IDs that have write access
            - `user_ids` (list[str], optional): List of user IDs that have write access

    The access control system determines who can read from or write to a channel.
    When access_control is None, the channel is considered public for read access
    but requires explicit permissions for write access (strict mode).
    When access_control is an empty dict {}, the channel is completely public.

    Example usage:
    ```python
    {
        "read": {
            "group_ids": ["group1", "group2"],
            "user_ids": ["user1", "user2"]
        },
        "write": {
            "group_ids": ["admin_group"],
            "user_ids": ["channel_owner"]
        }
    }
    ```

    All keys and nested structures are optional. The backend validates access
    using the has_access() function which checks both user and group memberships.

    Special Rules:
    - When access_control is None: Public read access, strict write access (requires explicit permissions)
    - When access_control is {}: Completely public (both read and write)
    - Access is determined by checking both direct user membership and group membership
    - The system uses get_permitted_group_and_user_ids() to extract permitted IDs from the access_control structure
    - Access validation is performed by has_access() function in utils/access_control.py
    - Admin users bypass access control restrictions entirely
    - For standard channels (non-group, non-dm), access control is enforced via has_access() calls
    - For group/dm channels, membership in the channel itself determines access
    - The has_access() function supports a 'strict' parameter that controls fallback behavior when access_control is None
    - Access control is implemented in backend/open_webui/utils/access_control.py
    - Frontend TypeScript interface shows this as `access_control?: object;` in ChannelForm
    - Used extensively in channel routers for read/write permission validation
    - Integrated with get_users_with_access() function to determine which users can access a channel
    - Channel access control is stored as JSON in the database (Column(JSON, nullable=True))
    - The access control structure is validated and processed by the backend's permission system
    - Access control applies to standard channels only; group and DM channels use membership-based access
    - The frontend AccessControl component provides UI for managing read/write permissions for groups and users
    - Access control settings are preserved during channel updates and creation
    - Empty access_control {} means completely public access (both read and write)
    - Null/None access_control means public read but restricted write access (strict mode)
    """

    group_ids: Optional[list[str]] = None
    """List of group IDs (primarily used during creation to add members)."""

    user_ids: Optional[list[str]] = None
    """List of user IDs (primarily used during creation to add members)."""


class CreateChannelForm(ChannelForm):
    """
    Form for creating a new channel.

    This form extends `ChannelForm` to include channel type specification during creation.
    The meta field can be used to store channel-specific metadata during creation.
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

    This model extends `ChannelResponse` with additional user-specific information
    and member details for group and direct message channels.
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
