"""Models for the Skills endpoints."""

from typing import Optional
from pydantic import BaseModel
from owui_client.models.access_grants import AccessGrantModel
from owui_client.models.users import UserResponse


class SkillMeta(BaseModel):
    """Metadata for a skill.

    Dict Fields:
        - `tags` (list[str], optional): Tags associated with the skill.
    """
    tags: Optional[list[str]] = []


class SkillModel(BaseModel):
    """Complete skill model with all data."""
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    content: str
    meta: SkillMeta
    is_active: bool = True
    access_grants: list[AccessGrantModel] = []
    updated_at: int
    created_at: int


class SkillResponse(BaseModel):
    """Skill response returned by create/update operations."""
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    meta: SkillMeta
    is_active: bool = True
    access_grants: list[AccessGrantModel] = []
    updated_at: int
    created_at: int


class SkillUserResponse(SkillResponse):
    """Skill response with user information."""
    user: Optional[UserResponse] = None


class SkillAccessResponse(SkillUserResponse):
    """Skill response with write access information."""
    write_access: Optional[bool] = False


class SkillForm(BaseModel):
    """Form for creating or updating a skill."""
    id: str
    name: str
    description: Optional[str] = None
    content: str
    meta: SkillMeta = SkillMeta()
    is_active: bool = True
    access_grants: Optional[list[dict]] = None
    """Access grants controlling who can use this skill.

    Dict Fields:
        Each dict in the list is an access grant entry. See
        `AccessGrantModel` for the expected keys: `user_id`, `group_id`,
        `type` ('user' or 'group'), and `permission` ('read' or 'write').
    """


class SkillListResponse(BaseModel):
    """Paginated list of skills."""
    items: list[SkillUserResponse] = []
    total: int = 0


class SkillAccessListResponse(BaseModel):
    """Paginated list of skills with access information."""
    items: list[SkillAccessResponse] = []
    total: int = 0
