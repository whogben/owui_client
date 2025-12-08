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
    
    Known keys:
    - `config`: A dictionary containing configuration settings.
        - `share` (bool): Whether the group is shared.
    """

    meta: Optional[dict] = None
    """Metadata associated with the group."""

    permissions: Optional[dict] = None
    """
    Permissions settings for the group.
    
    This dictionary follows the structure of `USER_PERMISSIONS` in the backend configuration.
    It contains nested dictionaries for different categories:
    - `workspace`: access to models, knowledge, prompts, tools, etc.
    - `sharing`: permissions to share different resources.
    - `chat`: permissions for chat features (delete, edit, upload, etc.).
    - `features`: access to general features like api_keys, notes, folders, web_search, etc.
    
    Values are typically booleans indicating if the permission is granted.
    """

    created_at: int  # timestamp in epoch
    """Timestamp of creation (epoch seconds)."""

    updated_at: int  # timestamp in epoch
    """Timestamp of last update (epoch seconds)."""


class GroupResponse(GroupModel):
    """
    Response model for group details, including member count.
    """

    member_count: Optional[int] = None
    """Number of members in the group."""


class GroupExportResponse(GroupResponse):
    """
    Response model for exporting a group, including user IDs.
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
    
    See `GroupModel.permissions` for structure details.
    """

    data: Optional[dict] = None
    """
    Additional data for the group.
    
    See `GroupModel.data` for structure details.
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
