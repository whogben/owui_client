from typing import Optional
from pydantic import BaseModel, ConfigDict

from owui_client.models.access_grants import AccessGrantModel


class FolderMetadataResponse(BaseModel):
    """
    Response model for folder metadata.
    """

    icon: Optional[str] = None
    """The icon for the folder, typically an emoji or URL."""


class FolderModel(BaseModel):
    """
    Model representing a folder in the system.
    """

    id: str
    """Unique identifier for the folder."""

    parent_id: Optional[str] = None
    """ID of the parent folder, or None if it's a root folder."""

    user_id: str
    """ID of the user who owns the folder."""

    name: str
    """Name of the folder."""

    items: Optional[dict] = None
    """Dictionary of items contained in the folder (contents).

    Dict Fields:
        - `chat_ids` (list[str], optional): List of chat IDs contained in the folder
        - `file_ids` (list[str], optional): List of file IDs contained in the folder

    This field represents the contents of the folder, including references to chats and files.
    The frontend uses this to manage folder contents via the `/folders/{id}/update/items` endpoint.
    """

    meta: Optional[dict] = None
    """Metadata for the folder, such as icon.

    Dict Fields:
        - `icon` (str, optional): Emoji icon for the folder (e.g., "📁", "🗂️", "📂"). Used for visual representation in the UI. When not provided, a default folder icon is displayed. The icon can be set or updated via the emoji picker in the frontend interface.
    """

    data: Optional[dict] = None
    """Additional data associated with the folder, containing configuration and file references.

    Dict Fields:
        - `system_prompt` (str, optional): System prompt associated with the folder. Used to provide context or instructions for chats within this folder.
        - `files` (list, optional): List of file references associated with the folder. Each file reference can have a `type` field (e.g., "file" or "collection") and an `id` field for the file/collection ID. Used for knowledge management and chat context.
        - `model_ids` (list[str], optional): List of model IDs associated with the folder. Determines which models are available/selected when chatting within this folder.

    The `data` field is used extensively in the frontend for:
    - Setting default models for chats within the folder (via `model_ids`)
    - Providing system prompts that apply to all chats in the folder
    - Managing knowledge files that should be available in folder chats
    - Synchronizing folder settings between frontend and backend

    When a folder is selected in the UI, the frontend automatically applies the folder's `model_ids` to the chat interface and makes the folder's files available for knowledge retrieval.
    """

    is_expanded: bool = False
    """Whether the folder is expanded in the UI."""

    created_at: int
    """Timestamp of creation (Unix epoch)."""

    updated_at: int
    """Timestamp of last update (Unix epoch)."""

    access_grants: list[AccessGrantModel] = []
    """Access grants on the folder. Populated by the backend on `get_folder_by_id`
    and `update_folder_access_by_id`; empty for endpoints that do not surface grants.
    See `AccessGrantModel` for the entry shape."""

    model_config = ConfigDict(from_attributes=True)


class FolderNameIdResponse(BaseModel):
    """
    Response model containing minimal folder information.
    """

    id: str
    """Unique identifier for the folder."""

    name: str
    """Name of the folder."""

    meta: Optional[FolderMetadataResponse] = None
    """Metadata for the folder, containing the icon."""

    parent_id: Optional[str] = None
    """ID of the parent folder."""

    is_expanded: bool = False
    """Whether the folder is expanded in the UI."""

    unread_count: int = 0
    """Number of chats in this folder with unread messages (added in Open WebUI 0.11.0)."""

    created_at: int
    """Timestamp of creation (Unix epoch)."""

    updated_at: int
    """Timestamp of last update (Unix epoch)."""


class SharedFolderResponse(BaseModel):
    """
    Response model for a folder shared with the current user (the "shared with me" view).

    Returned by `GET /folders/shared`. The backend builds each entry from the folder's
    full model dump plus `owner_name` (display name of the owning user) and `permission`
    (the highest access level the current user holds on that folder). Child folders of a
    shared root inherit the root's permission.

    Note: `permission` is always 'read' or 'write'. Entries the current user owns are
    excluded by the backend, so this model only describes folders owned by others.
    The raw API payload also includes the full folder fields (such as `items` and `data`),
    which are dropped when parsing into this model.
    """

    id: str
    """Unique identifier for the folder."""

    name: str
    """Name of the folder."""

    parent_id: Optional[str] = None
    """ID of the parent folder, or None for a root folder."""

    user_id: str
    """ID of the user who owns the folder."""

    owner_name: Optional[str] = None
    """Display name of the folder owner, resolved by the backend for display."""

    permission: str = "read"
    """Highest access level the current user has on this folder: 'read' or 'write'."""

    access_grants: list[AccessGrantModel] = []
    """Access grants on the folder.

    Always an empty list in `GET /folders/shared` responses (the backend does not populate
    it for the shared listing). Grants are fetched separately via `get_folder_by_id` or
    `update_folder_access_by_id`. See `AccessGrantModel` for the entry shape."""

    is_expanded: bool = False
    """Whether the folder is expanded in the UI."""

    meta: Optional[dict] = None
    """Folder metadata for display.

    Dict Fields:
        - `icon` (str, optional): Emoji icon for the folder (e.g. "📁", "🗂️"). When absent, the UI shows a default folder icon.
    """

    created_at: int
    """Timestamp of creation (Unix epoch)."""

    updated_at: int
    """Timestamp of last update (Unix epoch)."""


class FolderForm(BaseModel):
    """
    Form for creating a new folder.
    """

    name: str
    """Name of the folder."""

    data: Optional[dict] = None
    """Additional data for the folder, such as files.

    Dict Fields:
        - `system_prompt` (str, optional): System prompt associated with the folder
        - `files` (list, optional): List of file references associated with the folder
        - `model_ids` (list, optional): List of model IDs associated with the folder
    """

    meta: Optional[dict] = None
    """Metadata for the folder, such as icon.

    Dict Fields:
        - `icon` (str, optional): Emoji icon for the folder (e.g., "📁", "🗂️", "📂"). Used for visual representation in the UI.
    """

    parent_id: Optional[str] = None
    """ID of the parent folder. Set this to place the new folder inside an existing folder. Use None to create a root-level folder."""

    model_config = ConfigDict(extra="allow")


class FolderUpdateForm(BaseModel):
    """
    Form for updating an existing folder.
    """

    name: Optional[str] = None
    """New name for the folder."""

    data: Optional[dict] = None
    """New additional data for the folder.

    Dict Fields:
        - `system_prompt` (str, optional): System prompt associated with the folder
        - `files` (list, optional): List of file references associated with the folder. Each file reference can have a `type` field (e.g., "file" or "collection") and an `id` field for the file/collection ID.
        - `model_ids` (list, optional): List of model IDs associated with the folder
    """

    meta: Optional[dict] = None
    """New metadata for the folder.

    Dict Fields:
        - `icon` (str, optional): Emoji icon for the folder (e.g., "📁", "🗂️", "📂"). Used for visual representation in the UI.
    """

    model_config = ConfigDict(extra="allow")


class FolderParentIdForm(BaseModel):
    """
    Form for updating a folder's parent ID.
    """

    parent_id: Optional[str] = None
    """The new parent folder ID, or None to move to root."""


class FolderIsExpandedForm(BaseModel):
    """
    Form for updating a folder's expansion state.
    """

    is_expanded: bool
    """Whether the folder should be expanded."""


class FolderAccessGrantsForm(BaseModel):
    """
    Form for updating access grants on a folder (folder sharing).

    Replaces all existing grants on the folder with the supplied list. Used by
    `POST /folders/{id}/access/update` to share a folder with specific users, groups,
    or everyone, with read or write access. Only the folder owner, an admin, or a user
    with write access may call it; non-admins are subject to sharing permission filters
    (public/individual user grants may be stripped)."""

    access_grants: list[dict]
    """List of access grants to set on the folder, replacing all existing grants.

    Dict Fields:
        - `id` (str, optional): Unique identifier for the grant. If omitted the backend generates one.
        - `principal_type` (str, required): 'user' or 'group'
        - `principal_id` (str, required): User ID, group ID, or '*' for public (everyone)
        - `permission` (str, required): 'read' or 'write'
    """
