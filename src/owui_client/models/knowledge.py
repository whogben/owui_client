from typing import Optional, Union
from pydantic import BaseModel, ConfigDict

from owui_client.models.users import UserResponse
from owui_client.models.files import FileMetadataResponse


class KnowledgeModel(BaseModel):
    """
    Represents a knowledge base.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    """The unique identifier of the knowledge base."""

    user_id: str
    """The ID of the user who owns the knowledge base."""

    name: str
    """The name of the knowledge base."""

    description: str
    """A description of the knowledge base."""

    meta: Optional[dict] = None
    """Metadata associated with the knowledge base."""

    access_control: Optional[dict] = None
    """
    Access control settings.

    - `None`: Public access, available to all users with the "user" role.
    - `{}`: Private access, restricted exclusively to the owner.
    - Custom permissions: Specific access control for reading and writing.
      Can specify group or user-level restrictions.
      Example:
      ```python
      {
          "read": {
              "group_ids": ["group_id1", "group_id2"],
              "user_ids":  ["user_id1", "user_id2"]
          },
          "write": {
              "group_ids": ["group_id1", "group_id2"],
              "user_ids":  ["user_id1", "user_id2"]
          }
      }
      ```
    """

    created_at: int
    """Timestamp of creation (epoch)."""

    updated_at: int
    """Timestamp of last update (epoch)."""


class KnowledgeUserModel(KnowledgeModel):
    """
    Represents a knowledge base with user information.
    """

    user: Optional[UserResponse] = None
    """The user who owns the knowledge base."""


class KnowledgeResponse(KnowledgeModel):
    """
    Represents a knowledge base response, optionally including files.
    """

    files: Optional[list[Union[FileMetadataResponse, dict]]] = None
    """List of files associated with the knowledge base."""


class KnowledgeUserResponse(KnowledgeUserModel):
    """
    Represents a knowledge base response including user information and files.
    """

    files: Optional[list[Union[FileMetadataResponse, dict]]] = None
    """List of files associated with the knowledge base."""


class KnowledgeForm(BaseModel):
    """
    Form for creating or updating a knowledge base.
    """

    name: str
    """The name of the knowledge base."""

    description: str
    """A description of the knowledge base."""

    access_control: Optional[dict] = None
    """
    Access control settings.

    - `None`: Public access, available to all users with the "user" role.
    - `{}`: Private access, restricted exclusively to the owner.
    - Custom permissions: Specific access control for reading and writing.
      Can specify group or user-level restrictions.
      Example:
      ```python
      {
          "read": {
              "group_ids": ["group_id1", "group_id2"],
              "user_ids":  ["user_id1", "user_id2"]
          },
          "write": {
              "group_ids": ["group_id1", "group_id2"],
              "user_ids":  ["user_id1", "user_id2"]
          }
      }
      ```
    """


class KnowledgeFilesResponse(KnowledgeResponse):
    """
    Represents a knowledge base response with full file metadata.
    """

    files: list[FileMetadataResponse]
    """List of files with metadata associated with the knowledge base."""

    warnings: Optional[dict] = None
    """
    Warnings returned during processing, e.g., if some files failed to process in a batch operation.
    Structure: `{"message": str, "errors": list[str]}`.
    """


class KnowledgeFileIdForm(BaseModel):
    """
    Form for adding or removing a file from a knowledge base.
    """

    file_id: str
    """The ID of the file to add or remove."""
