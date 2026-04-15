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
    """Snapshot of the prompt at a point in time.

    Dict Fields:
        - `name` (str, optional): Prompt name at the time of snapshot.
        - `content` (str, optional): Prompt content at the time of snapshot.
        - `data` (dict, optional): Prompt data at the time of snapshot.
        - `meta` (dict, optional): Prompt metadata at the time of snapshot.
        - `tags` (list, optional): Prompt tags at the time of snapshot.
    """
    user_id: str
    commit_message: Optional[str] = None
    created_at: int


class PromptHistoryResponse(PromptHistoryModel):
    """Prompt history response with user information."""
    user: Optional[UserResponse] = None
