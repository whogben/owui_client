"""Models for the Skills endpoints."""

from typing import Optional
from pydantic import BaseModel
from owui_client.models.access_grants import AccessGrantModel
from owui_client.models.users import UserResponse


class SkillMeta(BaseModel):
    """Metadata for a skill."""
    tags: Optional[list[str]] = []
    """Tags associated with the skill."""


class SkillModel(BaseModel):
    """Complete skill model with all data."""
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    content: str
    """The skill's prompt content."""
    meta: SkillMeta
    """Skill metadata including tags."""
    is_active: bool = True
    """Whether the skill is active."""
    access_grants: list[AccessGrantModel] = []
    """List of access grants controlling who can use this skill."""
    updated_at: int
    created_at: int


class SkillResponse(BaseModel):
    """Skill response returned by create/update operations.

    Note: This response omits the `content` field for performance. Use
    `SkillModel` (via `export_skills`) to retrieve full skill data including content.
    """
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    meta: SkillMeta
    """Skill metadata including tags."""
    is_active: bool = True
    """Whether the skill is active."""
    access_grants: list[AccessGrantModel] = []
    """List of access grants controlling who can use this skill."""
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
    """The skill's prompt content."""
    meta: SkillMeta = SkillMeta()
    is_active: bool = True
    access_grants: Optional[list[dict]] = None
    """Access grants controlling who can use this skill.

    Dict Fields:
        Each dict in the list is an access grant entry with the following keys:
        - `principal_type` (str, required): Type of principal, 'user' or 'group'.
        - `principal_id` (str, required): ID of the user or group, or '*' for wildcard (public access).
        - `permission` (str, required): Permission level, 'read' or 'write'.
    """


class SkillListResponse(BaseModel):
    """Paginated list of skills."""
    items: list[SkillUserResponse] = []
    total: int = 0


class SkillAccessListResponse(BaseModel):
    """Paginated list of skills with access information."""
    items: list[SkillAccessResponse] = []
    total: int = 0
