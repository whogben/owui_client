from typing import Optional
from pydantic import BaseModel, ConfigDict


class GroupModel(BaseModel):
    """
    Represents a user group in Open WebUI.

    Groups allow for organizing users and managing permissions.
    """

    model_config = ConfigDict(from_attributes=True)
    id: str
    """Unique identifier for the group."""

    user_id: str
    """ID of the user who created the group."""

    name: str
    """Name of the group."""

    description: str
    """Description of the group."""

    data: Optional[dict] = None
    """
    Additional data associated with the group.

    Dict Fields:
    - `config` (dict, optional): Configuration settings for the group
        - `share` (bool, optional): Whether the group is shared and visible to non-members. Defaults to True when not specified. Used in frontend UI to control group visibility and in backend filtering logic.

    This field stores group-specific configuration options that affect how the group behaves
    in the system. The `share` setting is particularly important as it determines if the group
    should be visible to users who are not members of the group, and is used in both frontend
    UI controls and backend filtering operations. The backend uses this field for SQL filtering
    operations (e.g., `Group.data["config"]["share"].as_boolean()` and `Group.data.op("->>")("share")`).
    """

    meta: Optional[dict] = None
    """Metadata associated with the group.

    Dict Fields:
        - `export_timestamp` (int, optional): Timestamp when the group was exported (epoch seconds)
        - `exported_by` (str, optional): User ID of who performed the export
        - `version` (str, optional): Version identifier for the export format
        - `source_system` (str, optional): System or platform where the group originated
        - `custom_data` (dict, optional): Additional custom metadata specific to the group

    This field is used to store arbitrary metadata about the group, particularly
    useful for export/import operations and tracking group provenance. The backend
    database schema defines this as a JSON field that can store any key-value pairs,
    but the specific keys documented here represent the primary usage patterns found
    in the codebase. Additional keys may exist in the backend implementation.
    """

    permissions: Optional[dict] = None
    """
    Permissions settings for the group.

    Dict Fields:
        - `workspace` (dict, optional): Workspace access permissions
            - `models` (bool, optional): Access to models
            - `knowledge` (bool, optional): Access to knowledge
            - `prompts` (bool, optional): Access to prompts
            - `tools` (bool, optional): Access to tools
            - `models_import` (bool, optional): Permission to import models
            - `models_export` (bool, optional): Permission to export models
            - `prompts_import` (bool, optional): Permission to import prompts
            - `prompts_export` (bool, optional): Permission to export prompts
            - `tools_import` (bool, optional): Permission to import tools
            - `tools_export` (bool, optional): Permission to export tools
        - `sharing` (dict, optional): Sharing permissions
            - `models` (bool, optional): Permission to share models
            - `public_models` (bool, optional): Permission to share models publicly
            - `knowledge` (bool, optional): Permission to share knowledge
            - `public_knowledge` (bool, optional): Permission to share knowledge publicly
            - `prompts` (bool, optional): Permission to share prompts
            - `public_prompts` (bool, optional): Permission to share prompts publicly
            - `tools` (bool, optional): Permission to share tools
            - `public_tools` (bool, optional): Permission to share tools publicly
            - `notes` (bool, optional): Permission to share notes
            - `public_notes` (bool, optional): Permission to share notes publicly
        - `chat` (dict, optional): Chat feature permissions
            - `controls` (bool, optional): Access to chat controls
            - `valves` (bool, optional): Access to chat valves
            - `system_prompt` (bool, optional): Access to system prompt
            - `params` (bool, optional): Access to chat parameters
            - `file_upload` (bool, optional): Permission to upload files
            - `delete` (bool, optional): Permission to delete chats
            - `delete_message` (bool, optional): Permission to delete messages
            - `continue_response` (bool, optional): Permission to continue responses
            - `regenerate_response` (bool, optional): Permission to regenerate responses
            - `rate_response` (bool, optional): Permission to rate responses
            - `edit` (bool, optional): Permission to edit chats
            - `share` (bool, optional): Permission to share chats
            - `export` (bool, optional): Permission to export chats
            - `stt` (bool, optional): Permission to use speech-to-text
            - `tts` (bool, optional): Permission to use text-to-speech
            - `call` (bool, optional): Permission to make calls
            - `multiple_models` (bool, optional): Permission to use multiple models
            - `temporary` (bool, optional): Permission to use temporary chats
            - `temporary_enforced` (bool, optional): Enforced temporary chat usage
        - `features` (dict, optional): General feature permissions
            - `api_keys` (bool, optional): Access to API keys
            - `notes` (bool, optional): Access to notes
            - `folders` (bool, optional): Access to folders
            - `channels` (bool, optional): Access to channels
            - `direct_tool_servers` (bool, optional): Access to direct tool servers
            - `web_search` (bool, optional): Access to web search
            - `image_generation` (bool, optional): Access to image generation
            - `code_interpreter` (bool, optional): Access to code interpreter

    This dictionary follows the structure of `USER_PERMISSIONS` in the backend configuration.
    Values are typically booleans indicating if the permission is granted.
    """

    created_at: int  # timestamp in epoch
    """Timestamp of creation (epoch seconds)."""

    updated_at: int  # timestamp in epoch
    """Timestamp of last update (epoch seconds)."""


class GroupResponse(GroupModel):
    """
    Response model for group details, including member count.

    This model extends `GroupModel` to include additional response-specific information
    such as the number of members in the group. The inherited data field contains
    group configuration that affects how the group is displayed and filtered.
    """

    member_count: Optional[int] = None
    """Number of members in the group."""


class GroupExportResponse(GroupResponse):
    """
    Response model for exporting a group, including user IDs.

    This model is used when exporting complete group data for backup and migration purposes.
    It includes all standard group information plus the list of member user IDs.

    The permissions attribute in this context represents the complete set of permissions
    that will be exported with the group, preserving the group's access control configuration
    for restoration in another system or instance.
    """

    user_ids: list[str] = []
    """List of user IDs that are members of the group."""


class GroupForm(BaseModel):
    """
    Form for creating a new group.
    """

    name: str
    """Name of the group."""

    description: str
    """Description of the group."""

    permissions: Optional[dict] = None
    """
    Permissions settings for the group.

    Dict Fields:
        - `workspace` (dict, optional): Workspace access permissions
            - `models` (bool, optional): Access to models
            - `knowledge` (bool, optional): Access to knowledge
            - `prompts` (bool, optional): Access to prompts
            - `tools` (bool, optional): Access to tools
            - `models_import` (bool, optional): Permission to import models
            - `models_export` (bool, optional): Permission to export models
            - `prompts_import` (bool, optional): Permission to import prompts
            - `prompts_export` (bool, optional): Permission to export prompts
            - `tools_import` (bool, optional): Permission to import tools
            - `tools_export` (bool, optional): Permission to export tools
        - `sharing` (dict, optional): Sharing permissions
            - `models` (bool, optional): Permission to share models
            - `public_models` (bool, optional): Permission to share models publicly
            - `knowledge` (bool, optional): Permission to share knowledge
            - `public_knowledge` (bool, optional): Permission to share knowledge publicly
            - `prompts` (bool, optional): Permission to share prompts
            - `public_prompts` (bool, optional): Permission to share prompts publicly
            - `tools` (bool, optional): Permission to share tools
            - `public_tools` (bool, optional): Permission to share tools publicly
            - `notes` (bool, optional): Permission to share notes
            - `public_notes` (bool, optional): Permission to share notes publicly
        - `chat` (dict, optional): Chat feature permissions
            - `controls` (bool, optional): Access to chat controls
            - `valves` (bool, optional): Access to chat valves
            - `system_prompt` (bool, optional): Access to system prompt
            - `params` (bool, optional): Access to chat parameters
            - `file_upload` (bool, optional): Permission to upload files
            - `delete` (bool, optional): Permission to delete chats
            - `delete_message` (bool, optional): Permission to delete messages
            - `continue_response` (bool, optional): Permission to continue responses
            - `regenerate_response` (bool, optional): Permission to regenerate responses
            - `rate_response` (bool, optional): Permission to rate responses
            - `edit` (bool, optional): Permission to edit chats
            - `share` (bool, optional): Permission to share chats
            - `export` (bool, optional): Permission to export chats
            - `stt` (bool, optional): Permission to use speech-to-text
            - `tts` (bool, optional): Permission to use text-to-speech
            - `call` (bool, optional): Permission to make calls
            - `multiple_models` (bool, optional): Permission to use multiple models
            - `temporary` (bool, optional): Permission to use temporary chats
            - `temporary_enforced` (bool, optional): Enforced temporary chat usage
        - `features` (dict, optional): General feature permissions
            - `api_keys` (bool, optional): Access to API keys
            - `notes` (bool, optional): Access to notes
            - `folders` (bool, optional): Access to folders
            - `channels` (bool, optional): Access to channels
            - `direct_tool_servers` (bool, optional): Access to direct tool servers
            - `web_search` (bool, optional): Access to web search
            - `image_generation` (bool, optional): Access to image generation
            - `code_interpreter` (bool, optional): Access to code interpreter

    This dictionary follows the structure of `USER_PERMISSIONS` in the backend configuration.
    Values are typically booleans indicating if the permission is granted.
    """

    data: Optional[dict] = None
    """
    Additional data for the group.

    Dict Fields:
        - `config` (dict, optional): Configuration settings for the group
            - `share` (bool, optional): Whether the group is shared and visible to non-members

    This field is used to store group-specific configuration options.
    The `share` setting determines if the group should be visible to users who are not members.
    """


class UserIdsForm(BaseModel):
    """
    Form for adding/removing users from a group.
    """

    user_ids: Optional[list[str]] = None
    """List of user IDs."""


class GroupUpdateForm(GroupForm):
    """
    Form for updating an existing group.
    """

    pass
