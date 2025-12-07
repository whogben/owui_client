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

    Structure:
    ```json
    {
      "content": {
        "json": null,
        "html": "string",
        "md": "string"
      }
    }
    ```
    """

    meta: Optional[dict] = None
    """Metadata associated with the note."""

    access_control: Optional[dict] = None
    """Access control settings for the note."""

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

    Structure:
    ```json
    {
      "content": {
        "json": null,
        "html": "string",
        "md": "string"
      }
    }
    ```
    """

    meta: Optional[dict] = None
    """Metadata associated with the note."""

    access_control: Optional[dict] = None
    """Access control settings for the note."""

class NoteUpdateForm(BaseModel):
    """
    Form data for updating an existing note.
    """
    title: Optional[str] = None
    """The title of the note."""

    data: Optional[dict] = None
    """
    The content of the note.

    Structure:
    ```json
    {
      "content": {
        "json": null,
        "html": "string",
        "md": "string"
      }
    }
    ```
    """

    meta: Optional[dict] = None
    """Metadata associated with the note."""

    access_control: Optional[dict] = None
    """Access control settings for the note."""

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

