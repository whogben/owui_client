from typing import Optional
from pydantic import BaseModel, ConfigDict


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
