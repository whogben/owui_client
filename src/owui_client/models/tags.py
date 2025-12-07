"""
Models for Tag-related operations.
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional

class TagModel(BaseModel):
    """
    Represents a tag assigned to a chat or other entity.
    """

    id: str
    """The unique identifier for the tag. Usually derived from the name (lowercase, spaces replaced with underscores)."""

    name: str
    """The display name of the tag."""

    user_id: str
    """The ID of the user who created this tag."""

    meta: Optional[dict] = None
    """Optional metadata associated with the tag."""

    model_config = ConfigDict(from_attributes=True)

class TagChatIdForm(BaseModel):
    """
    Form for associating a tag with a chat ID.
    
    Note: This model is defined in the backend but appears to be unused in the current codebase.
    """

    name: str
    """The name of the tag."""

    chat_id: str
    """The ID of the chat to associate with the tag."""

