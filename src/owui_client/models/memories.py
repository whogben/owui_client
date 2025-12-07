from typing import Optional
from pydantic import BaseModel, ConfigDict


class MemoryModel(BaseModel):
    """
    Represents a memory item stored for a user.
    """

    id: str
    """Unique identifier for the memory."""

    user_id: str
    """ID of the user who owns this memory."""

    content: str
    """The actual text content of the memory."""

    updated_at: int
    """Unix timestamp (epoch) of when the memory was last updated."""

    created_at: int
    """Unix timestamp (epoch) of when the memory was created."""

    model_config = ConfigDict(from_attributes=True)


class AddMemoryForm(BaseModel):
    """
    Form for adding a new memory.
    """

    content: str
    """The text content to be stored as memory."""


class MemoryUpdateModel(BaseModel):
    """
    Form for updating an existing memory.
    """

    content: Optional[str] = None
    """The new text content for the memory. If provided, replaces the existing content."""


class QueryMemoryForm(BaseModel):
    """
    Form for querying memories using vector search.
    """

    content: str
    """The search query text."""

    k: Optional[int] = 1
    """The number of results to return. Defaults to 1."""

