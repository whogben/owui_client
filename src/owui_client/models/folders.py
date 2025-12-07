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
    """Dictionary of items contained in the folder (contents)."""

    meta: Optional[dict] = None
    """Metadata for the folder, such as icon."""

    data: Optional[dict] = None
    """Additional data associated with the folder, such as file references (e.g. `{"files": [...]}`)."""

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
    """Additional data for the folder, such as files."""

    meta: Optional[dict] = None
    """Metadata for the folder, such as icon."""

    model_config = ConfigDict(extra="allow")


class FolderUpdateForm(BaseModel):
    """
    Form for updating an existing folder.
    """

    name: Optional[str] = None
    """New name for the folder."""

    data: Optional[dict] = None
    """New additional data for the folder."""

    meta: Optional[dict] = None
    """New metadata for the folder."""

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

