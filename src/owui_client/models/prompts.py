"""Prompt models for Open WebUI prompt commands.

Prompts are reusable command templates that can be invoked with `/command` syntax.
"""

from typing import Optional, Any
from pydantic import BaseModel, ConfigDict, Field
from owui_client.models.users import UserResponse
from owui_client.models.access_grants import AccessGrantModel


class PromptModel(BaseModel):
    """Represents a prompt command with all stored attributes.

    Prompts are reusable text templates invoked via slash commands (e.g., `/help`).
    They support versioning, tagging, and access control via access grants.
    """

    model_config = ConfigDict(from_attributes=True)

    id: Optional[str] = None
    """Unique identifier for the prompt (UUID)."""

    command: str
    """The command trigger (e.g., 'help'). Stored without leading slash."""

    user_id: str
    """The ID of the user who created the prompt."""

    name: str
    """Display name for the prompt (changed from 'title' in earlier versions)."""

    content: str
    """The content/template text of the prompt."""

    data: Optional[dict[str, Any]] = None
    """Additional structured data associated with the prompt.

    Dict Fields:
        Arbitrary key-value pairs for prompt-specific data. Used by frontend
        for prompt configuration and rendering.
    """

    meta: Optional[dict[str, Any]] = None
    """Metadata for the prompt.

    Dict Fields:
        Arbitrary key-value pairs for prompt metadata. Can include display
        preferences, source information, or other metadata.
    """

    tags: Optional[list[str]] = None
    """List of tags for categorizing and filtering prompts."""

    is_active: Optional[bool] = True
    """Whether the prompt is active (soft-delete support)."""

    version_id: Optional[str] = None
    """ID of the active version in prompt history. Points to a history entry."""

    created_at: Optional[int] = None
    """Timestamp when the prompt was created (epoch time)."""

    updated_at: Optional[int] = None
    """Timestamp when the prompt was last updated (epoch time)."""

    access_grants: list[AccessGrantModel] = Field(default_factory=list)
    """List of access grants controlling who can read/write this prompt."""


class PromptUserResponse(PromptModel):
    """Response model for a prompt including user details."""

    user: Optional[UserResponse] = None
    """Details of the user who created the prompt."""


class PromptAccessResponse(PromptUserResponse):
    """Response model for a prompt with access information."""

    write_access: Optional[bool] = False
    """Whether the current user has write access to this prompt."""


class PromptListResponse(BaseModel):
    """Paginated list of prompts."""

    items: list[PromptUserResponse]
    """List of prompt items in the current page."""

    total: int
    """Total number of items matching the query."""


class PromptAccessListResponse(BaseModel):
    """Paginated list of prompts with access information."""

    items: list[PromptAccessResponse]
    """List of prompt items with access info in the current page."""

    total: int
    """Total number of items matching the query."""


class PromptForm(BaseModel):
    """Form for creating or updating a prompt.

    When updating, only changed fields need to be provided. The `name` field
    was previously called `title` in earlier API versions.
    """

    command: str
    """The command trigger. Stored without leading slash (e.g., 'help')."""

    name: str
    """Display name for the prompt."""

    content: str
    """The content/template text of the prompt."""

    data: Optional[dict[str, Any]] = None
    """Additional structured data for the prompt.

    Dict Fields:
        Arbitrary key-value pairs for prompt-specific data.
    """

    meta: Optional[dict[str, Any]] = None
    """Metadata for the prompt.

    Dict Fields:
        Arbitrary key-value pairs for prompt metadata.
    """

    tags: Optional[list[str]] = None
    """List of tags for categorizing the prompt."""

    access_grants: Optional[list[dict[str, Any]]] = None
    """Access grants to set on the prompt.

    Dict Fields:
        - `id` (str, optional): Unique identifier for the grant
        - `principal_type` (str, required): 'user' or 'group'
        - `principal_id` (str, required): ID of user/group, or '*' for public
        - `permission` (str, required): 'read' or 'write'
    """

    version_id: Optional[str] = None
    """Active version ID. Set when restoring a specific version."""

    commit_message: Optional[str] = None
    """Commit message for history tracking when updating content."""

    is_production: Optional[bool] = True
    """Whether to set the new version as production (active) version."""


class PromptVersionUpdateForm(BaseModel):
    """Form for updating the active version of a prompt.

    Used to roll back to a previous version by specifying its history entry ID.
    """

    version_id: str
    """ID of the history entry to set as the active version."""


class PromptMetadataForm(BaseModel):
    """Form for updating prompt metadata only.

    Updates name, command, and tags without creating a history entry.
    Used for lightweight metadata changes that don't affect content.
    """

    name: str
    """Display name for the prompt."""

    command: str
    """The command trigger. Stored without leading slash (e.g., 'help')."""

    tags: Optional[list[str]] = None
    """List of tags for categorizing the prompt."""


class PromptAccessGrantsForm(BaseModel):
    """Form for updating access grants on a prompt.

    Used to control who can read or write the prompt.
    """

    access_grants: list[dict[str, Any]]
    """List of access grants to set on the prompt.

    Dict Fields:
        Each dict should contain:
        - `principal_type` (str): 'user' or 'group'
        - `principal_id` (str): ID of user/group, or '*' for public
        - `permission` (str): 'read' or 'write'
    """


class PromptHistoryModel(BaseModel):
    """Represents a version history entry for a prompt.

    Each time a prompt's content is updated, a history entry is created
    to track the change. History entries form a tree structure via parent_id.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    """Unique identifier for this history entry (UUID)."""

    prompt_id: str
    """ID of the prompt this history entry belongs to."""

    parent_id: Optional[str] = None
    """ID of the parent history entry (previous version)."""

    snapshot: dict[str, Any]
    """Snapshot of the prompt data at this version.

    Dict Fields:
        - `command` (str): Command trigger
        - `name` (str): Display name
        - `content` (str): Prompt content
        - `tags` (list[str], optional): Tags
        - `data` (dict, optional): Additional data
        - `meta` (dict, optional): Metadata
    """

    user_id: str
    """ID of the user who created this version."""

    commit_message: Optional[str] = None
    """Optional commit message describing the change."""

    created_at: int
    """Timestamp when this history entry was created (epoch time)."""


class PromptHistoryResponse(PromptHistoryModel):
    """Response model for prompt history with user details."""

    user: Optional["UserResponse"] = None
    """Details of the user who created this version."""


class PromptDiffResponse(BaseModel):
    """Response model for diff between two prompt versions."""

    from_id: str
    """ID of the source (from) history entry."""

    to_id: str
    """ID of the target (to) history entry."""

    from_snapshot: dict[str, Any]
    """Snapshot of the source version.

    Dict Fields:
        - `command` (str): Command trigger
        - `name` (str): Display name
        - `content` (str): Prompt content
        - `tags` (list[str], optional): Tags
    """

    to_snapshot: dict[str, Any]
    """Snapshot of the target version.

    Dict Fields:
        - `command` (str): Command trigger
        - `name` (str): Display name
        - `content` (str): Prompt content
        - `tags` (list[str], optional): Tags
    """

    content_diff: list[str]
    """Unified diff lines showing content changes between versions."""

    name_changed: bool
    """Whether the name field changed between versions."""
