"""Models for prompt history."""

from typing import Optional
from pydantic import BaseModel
from owui_client.models.users import UserResponse


class PromptHistoryModel(BaseModel):
    """A snapshot of a prompt at a point in time."""
    id: str
    prompt_id: str
    parent_id: Optional[str] = None
    snapshot: dict
    """Snapshot of the prompt's content and settings at this point in time.

    Dict Fields:
        - `title` (str, optional): Title of the prompt.
        - `content` (str, optional): Full content/definition of the prompt.
        - `meta` (dict, optional): Metadata associated with the prompt, including tags.
    """
    user_id: str
    commit_message: Optional[str] = None
    created_at: int


class PromptHistoryResponse(PromptHistoryModel):
    """Prompt history response with user information."""
    user: Optional[UserResponse] = None
