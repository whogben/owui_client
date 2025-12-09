from typing import Optional
from pydantic import BaseModel, ConfigDict
from owui_client.models.users import UserResponse


class NoteModel(BaseModel):
    """
    Model representing a Note.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    """The unique identifier of the note."""

    user_id: str
    """The ID of the user who created the note."""

    title: str
    """The title of the note."""

    data: Optional[dict] = None
    """
    The content of the note.

    Dict Fields:
        - `content` (dict, required): Content in multiple formats
        - `content.json` (Any, optional): JSON representation of content, typically null
        - `content.html` (str, optional): HTML formatted content
        - `content.md` (str, optional): Markdown formatted content
        - `versions` (list, optional): Historical versions of the note content
        - `versions[].content` (dict, optional): Version content structure
        - `versions[].timestamp` (int, optional): Version timestamp in epoch
        - `versions[].user_id` (str, optional): User ID who created the version
    """

    meta: Optional[dict] = None
    """Metadata associated with the note.

    Dict Fields:
        This dictionary is used to store additional metadata about the note.
        It can contain arbitrary key-value pairs for extensibility.
        No specific keys are enforced by the backend - it accepts any valid JSON structure.
        Common usage patterns include storing custom attributes, tags, or application-specific metadata.
        When updating notes, the backend merges new meta data with existing meta data.
    """

    access_control: Optional[dict] = None
    """Access control settings for the note.

    Dict Fields:
        - `read` (dict, optional): Read access control configuration
        - `read.group_ids` (list[str], optional): List of group IDs that have read access
        - `read.user_ids` (list[str], optional): List of user IDs that have read access
        - `write` (dict, optional): Write access control configuration
        - `write.group_ids` (list[str], optional): List of group IDs that have write access
        - `write.user_ids` (list[str], optional): List of user IDs that have write access

    When None: Public read access, no write access (except owner)
    When {}: No special access control (public access for both read and write)
    """

    created_at: int  # timestamp in epoch
    """Timestamp when the note was created (in epoch)."""

    updated_at: int  # timestamp in epoch
    """Timestamp when the note was last updated (in epoch)."""


class NoteForm(BaseModel):
    """
    Form data for creating a new note.
    """

    title: str
    """The title of the note."""

    data: Optional[dict] = None
    """
    The content of the note.

    Dict Fields:
        - `content` (dict, required): Content in multiple formats
        - `content.json` (Any, optional): JSON representation of content, typically null
        - `content.html` (str, optional): HTML formatted content
        - `content.md` (str, optional): Markdown formatted content
        - `versions` (list, optional): Historical versions of the note content
        - `versions[].content` (dict, optional): Version content structure
        - `versions[].timestamp` (int, optional): Version timestamp in epoch
        - `versions[].user_id` (str, optional): User ID who created the version
    """

    meta: Optional[dict] = None
    """Metadata associated with the note.

    Dict Fields:
        This dictionary is used to store additional metadata about the note.
        It can contain arbitrary key-value pairs for extensibility.
        No specific keys are enforced by the backend - it accepts any valid JSON structure.
        Common usage patterns include storing custom attributes, tags, or application-specific metadata.
    """

    access_control: Optional[dict] = None
    """Access control settings for the note.

    Dict Fields:
        - `read` (dict, optional): Read access control configuration
        - `read.group_ids` (list[str], optional): List of group IDs that have read access
        - `read.user_ids` (list[str], optional): List of user IDs that have read access
        - `write` (dict, optional): Write access control configuration
        - `write.group_ids` (list[str], optional): List of group IDs that have write access
        - `write.user_ids` (list[str], optional): List of user IDs that have write access

    When None: Public read access, no write access (except owner)
    When {}: No special access control (public access for both read and write)
    """


class NoteUpdateForm(BaseModel):
    """
    Form data for updating an existing note.
    """

    title: Optional[str] = None
    """The title of the note."""

    data: Optional[dict] = None
    """
    The content of the note.

    Dict Fields:
        - `content` (dict, required): Content in multiple formats
        - `content.json` (Any, optional): JSON representation of content, typically null
        - `content.html` (str, optional): HTML formatted content
        - `content.md` (str, optional): Markdown formatted content
        - `versions` (list, optional): Historical versions of the note content
        - `versions[].content` (dict, optional): Version content structure
        - `versions[].timestamp` (int, optional): Version timestamp in epoch
        - `versions[].user_id` (str, optional): User ID who created the version
    """

    meta: Optional[dict] = None
    """Metadata associated with the note.

    Dict Fields:
        This dictionary is used to store additional metadata about the note.
        It can contain arbitrary key-value pairs for extensibility.
        No specific keys are enforced by the backend - it accepts any valid JSON structure.
        Common usage patterns include storing custom attributes, tags, or application-specific metadata.
        When updating notes, the backend merges new meta data with existing meta data using shallow merge.
        If the same key exists in both existing and new meta, the new value overwrites the existing one.
    """

    access_control: Optional[dict] = None
    """Access control settings for the note.

    Dict Fields:
        - `read` (dict, optional): Read access control configuration
        - `read.group_ids` (list[str], optional): List of group IDs that have read access
        - `read.user_ids` (list[str], optional): List of user IDs that have read access
        - `write` (dict, optional): Write access control configuration
        - `write.group_ids` (list[str], optional): List of group IDs that have write access
        - `write.user_ids` (list[str], optional): List of user IDs that have write access

    When None: Public read access, no write access (except owner)
    When {}: No special access control (public access for both read and write)
    """


class NoteUserResponse(NoteModel):
    """
    Note model with user information.
    """

    user: Optional[UserResponse] = None
    """The user who created the note."""


class NoteTitleIdResponse(BaseModel):
    """
    Simplified note model containing only ID, title and timestamps.
    """

    id: str
    """The unique identifier of the note."""

    title: str
    """The title of the note."""

    updated_at: int
    """Timestamp when the note was last updated (in epoch)."""

    created_at: int
    """Timestamp when the note was created (in epoch)."""
