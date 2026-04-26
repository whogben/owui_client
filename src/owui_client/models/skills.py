from typing import Optional, Any
from pydantic import BaseModel, ConfigDict, Field
from owui_client.models.users import UserResponse
from owui_client.models.access_grants import AccessGrantModel


class SkillMeta(BaseModel):
    """
    Metadata for a skill.
    """

    tags: Optional[list[str]] = []
    """
    List of tags associated with the skill for categorization and filtering.
    """


class SkillModel(BaseModel):
    """
    Model representing a skill in the database.

    Skills are reusable prompt templates or capabilities that can be attached
    to models to enhance their behavior.
    """

    id: str
    """
    Unique identifier for the skill.
    """

    user_id: str
    """
    ID of the user who created the skill.
    """

    name: str
    """
    Name of the skill.
    """

    description: Optional[str] = None
    """
    Description of what the skill does.
    """

    content: str
    """
    The prompt content or instructions that define the skill's behavior.
    """

    meta: SkillMeta
    """
    Metadata associated with the skill.
    """

    is_active: bool = True
    """
    Whether the skill is currently active and available for use.
    """

    access_grants: list[AccessGrantModel] = Field(default_factory=list)
    """
    List of access grants controlling who can read/write this skill.
    """

    updated_at: int
    """
    Timestamp of the last update (epoch).
    """

    created_at: int
    """
    Timestamp of creation (epoch).
    """

    model_config = ConfigDict(from_attributes=True)


class SkillUserModel(SkillModel):
    """
    Skill model with associated user information.
    """

    user: Optional[UserResponse] = None
    """
    Details of the user who owns the skill.
    """


class SkillResponse(BaseModel):
    """
    Response model for skill operations, excluding the content field.

    Used for list responses where the full skill content is not needed.
    """

    id: str
    """
    Unique identifier for the skill.
    """

    user_id: str
    """
    ID of the user who created the skill.
    """

    name: str
    """
    Name of the skill.
    """

    description: Optional[str] = None
    """
    Description of what the skill does.
    """

    meta: SkillMeta
    """
    Metadata associated with the skill.
    """

    is_active: bool = True
    """
    Whether the skill is currently active.
    """

    access_grants: list[AccessGrantModel] = Field(default_factory=list)
    """
    List of access grants controlling who can read/write this skill.
    """

    updated_at: int
    """
    Timestamp of the last update (epoch).
    """

    created_at: int
    """
    Timestamp of creation (epoch).
    """


class SkillUserResponse(SkillResponse):
    """
    Skill response including user details.
    """

    user: Optional[UserResponse] = None
    """
    Details of the user who owns the skill.
    """

    model_config = ConfigDict(extra="allow")
    """
    Allows extra fields which may be dynamically added.
    """


class SkillAccessResponse(SkillUserResponse):
    """
    Skill response including access information.
    """

    write_access: Optional[bool] = False
    """
    Whether the current user has write access to this skill.
    """


class SkillForm(BaseModel):
    """
    Form for creating or updating a skill.
    """

    id: str
    """
    Unique identifier for the skill.
    """

    name: str
    """
    Name of the skill.
    """

    description: Optional[str] = None
    """
    Description of what the skill does.
    """

    content: str
    """
    The prompt content or instructions that define the skill's behavior.
    """

    meta: SkillMeta = SkillMeta()
    """
    Metadata associated with the skill.
    """

    is_active: bool = True
    """
    Whether the skill is currently active.
    """

    access_grants: Optional[list[dict[str, Any]]] = None
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
    Response model for a paginated list of skills.
    """

    items: list[SkillUserResponse] = []
    """
    List of skills on the current page.
    """

    total: int = 0
    """
    Total number of skills matching the query.
    """


class SkillAccessListResponse(BaseModel):
    """
    Response model for a paginated list of skills with access information.
    """

    items: list[SkillAccessResponse] = []
    """
    List of skills with access information on the current page.
    """

    total: int = 0
    """
    Total number of skills matching the query.
    """


class SkillAccessGrantsForm(BaseModel):
    """
    Form for updating skill access grants.
    """

    access_grants: list[dict[str, Any]]
    """
    List of access grants for the skill.

    Dict Fields:
        - `id` (str, optional): Unique identifier for the grant
        - `principal_type` (str, required): 'user' or 'group'
        - `principal_id` (str, required): User/group ID, or '*' for public access
        - `permission` (str, required): 'read' or 'write'
    """
