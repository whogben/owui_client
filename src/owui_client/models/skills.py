"""Skill models for the Open WebUI Skills workspace.

Skills are prompt-style content blocks that get injected into the chat context
as system messages when referenced via `<$skillId|label>` mention syntax.
Unlike Tools, Skills are plain text/markdown (not Python code).
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from owui_client.models.users import UserResponse
from owui_client.models.access_grants import AccessGrantModel


class SkillMeta(BaseModel):
    """
    Metadata for a skill.
    """

    tags: Optional[list[str]] = []
    """
    List of tags for categorizing and filtering skills.
    """


class SkillModel(BaseModel):
    """
    Full skill model as stored in the database.

    Represents a skill with all its fields including content and access grants.
    """

    id: str
    """Unique identifier for the skill, derived from the skill name (slugified, lowercased)."""

    user_id: str
    """ID of the user who created the skill."""

    name: str
    """Display name of the skill."""

    description: Optional[str] = None
    """Brief description of what the skill does."""

    content: str
    """
    The text/markdown content of the skill. When a skill is invoked in chat,
    this content is wrapped in `<skill name="...">` tags and injected as a
    system message.
    """

    meta: SkillMeta
    """Metadata associated with the skill."""

    is_active: bool = True
    """Whether the skill is active and available for use. Inactive skills are hidden from selectors."""

    access_grants: list[AccessGrantModel] = Field(default_factory=list)
    """List of access grants controlling who can read/write this skill."""

    updated_at: int
    """Timestamp of the last update (epoch)."""

    created_at: int
    """Timestamp of creation (epoch)."""

    model_config = ConfigDict(from_attributes=True)


class SkillUserModel(SkillModel):
    """
    Skill model with associated user information.
    """

    user: Optional[UserResponse] = None
    """Details of the user who owns the skill."""


class SkillResponse(BaseModel):
    """
    Response model for skill operations, excluding the heavy content field.
    """

    id: str
    """Unique identifier for the skill."""

    user_id: str
    """ID of the user who created the skill."""

    name: str
    """Display name of the skill."""

    description: Optional[str] = None
    """Brief description of what the skill does."""

    meta: SkillMeta
    """Metadata associated with the skill."""

    is_active: bool = True
    """Whether the skill is active and available for use."""

    access_grants: list[AccessGrantModel] = Field(default_factory=list)
    """List of access grants controlling who can read/write this skill."""

    updated_at: int
    """Timestamp of the last update (epoch)."""

    created_at: int
    """Timestamp of creation (epoch)."""


class SkillUserResponse(SkillResponse):
    """
    Skill response including user details.
    """

    user: Optional[UserResponse] = None
    """Details of the user who owns the skill."""

    model_config = ConfigDict(extra="allow")
    """Allows extra fields which may be dynamically added."""


class SkillAccessResponse(SkillUserResponse):
    """
    Skill response with write access indicator.

    Used by list endpoints to communicate whether the requesting user
    has write permission on each skill.
    """

    write_access: Optional[bool] = False
    """Whether the requesting user has write access to this skill."""


class SkillForm(BaseModel):
    """
    Form for creating or updating a skill.
    """

    id: str
    """Unique identifier for the skill. Lowercased and spaces replaced with hyphens on create."""

    name: str
    """Display name of the skill."""

    description: Optional[str] = None
    """Brief description of what the skill does."""

    content: str
    """The text/markdown content of the skill."""

    meta: SkillMeta = SkillMeta()
    """Metadata associated with the skill."""

    is_active: bool = True
    """Whether the skill is active and available for use."""

    access_grants: Optional[list[dict]] = None
    """
    List of access grants for the skill.

    Dict Fields:
        - `id` (str, optional): Unique identifier for the grant
        - `principal_type` (str, required): 'user' or 'group'
        - `principal_id` (str, required): User/group ID, or '*' for public access
        - `permission` (str, required): 'read' or 'write'
    """


class SkillListResponse(BaseModel):
    """
    Paginated list of skills with user details.
    """

    items: list[SkillUserResponse] = []
    """List of skills in the current page."""

    total: int = 0
    """Total number of skills matching the query."""


class SkillAccessListResponse(BaseModel):
    """
    Paginated list of skills with access information.
    """

    items: list[SkillAccessResponse] = []
    """List of skills with write access indicators."""

    total: int = 0
    """Total number of skills matching the query."""


class SkillAccessGrantsForm(BaseModel):
    """
    Form for updating skill access grants.
    """

    access_grants: list[dict]
    """
    List of access grants for the skill.

    Dict Fields:
        - `id` (str, optional): Unique identifier for the grant
        - `principal_type` (str, required): 'user' or 'group'
        - `principal_id` (str, required): User/group ID, or '*' for public access
        - `permission` (str, required): 'read' or 'write'
    """
