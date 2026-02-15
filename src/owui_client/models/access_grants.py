"""Access grant models for resource permissions.

Access grants provide fine-grained permission control over resources like models,
tools, notes, channels, and knowledge collections.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class AccessGrantModel(BaseModel):
    """
    Full access grant model with all fields.

    Used when storing and retrieving access grants from the database.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    """Unique identifier for the grant."""

    resource_type: str
    """Type of resource: 'knowledge', 'model', 'prompt', 'tool', 'note', 'channel', or 'file'."""

    resource_id: str
    """ID of the resource this grant applies to."""

    principal_type: str
    """Type of principal: 'user' or 'group'."""

    principal_id: str
    """ID of the user or group, or '*' for wildcard (public access)."""

    permission: str
    """Permission level: 'read' or 'write'."""

    created_at: int
    """Timestamp when the grant was created (epoch time)."""


class AccessGrantResponse(BaseModel):
    """
    Slim grant model for API responses.

    Resource context (resource_type, resource_id) is implicit from the parent response.
    """

    id: str
    """Unique identifier for the grant."""

    principal_type: str
    """Type of principal: 'user' or 'group'."""

    principal_id: str
    """ID of the user or group, or '*' for wildcard (public access)."""

    permission: str
    """Permission level: 'read' or 'write'."""
