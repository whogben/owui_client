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
    """
    Metadata associated with the knowledge base.

    Dict Fields:
        - `legacy` (bool, optional): Whether this is a legacy knowledge base migrated from older versions
        - `document` (bool, optional): Whether this knowledge base represents a document-type structure
        - `tags` (list[str], optional): List of tags associated with the knowledge base
        - `id` (str, optional): Knowledge base ID
        - `name` (str, optional): Knowledge base name
        - `collection_name` (str, optional): Collection name
        - `type` (str, optional): Type of knowledge (e.g., 'file', 'collection')
        - `collection_names` (list[str], optional): List of collection names for collection-type knowledge

    Additional keys may exist. Complete structure not found in reference code.
    """

    access_control: Optional[dict] = None
    """
    Access control settings.

    - `None`: Public access, available to all users with the "user" role.
      Requires "sharing.public_knowledge" permission for non-admin users to set.
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

    Dict Fields:
        - `read` (dict, optional): Read access permissions
        - `write` (dict, optional): Write access permissions
        - `read.group_ids` (list[str], optional): List of group IDs with read access
        - `read.user_ids` (list[str], optional): List of user IDs with read access
        - `write.group_ids` (list[str], optional): List of group IDs with write access
        - `write.user_ids` (list[str], optional): List of user IDs with write access
    """

    created_at: int
    """Timestamp of creation (epoch)."""

    updated_at: int
    """Timestamp of last update (epoch)."""


class KnowledgeUserModel(KnowledgeModel):
    """
    Represents a knowledge base with user information.

    Inherits access_control from `KnowledgeModel`. Access is determined by:
    - Direct user ownership (user_id matches)
    - Access control permissions (read/write for groups and users)
    - Admin users have full access regardless of access_control settings
    """

    user: Optional[UserResponse] = None
    """The user who owns the knowledge base."""


class KnowledgeResponse(KnowledgeModel):
    """
    Represents a knowledge base response, optionally including files.

    Inherits meta from `KnowledgeModel`. See `KnowledgeModel.meta` for complete documentation
    of the metadata structure and valid fields.
    """

    files: Optional[list[Union[FileMetadataResponse, dict]]] = None
    """List of files associated with the knowledge base."""


class KnowledgeUserResponse(KnowledgeUserModel):
    """
    Represents a knowledge base response including user information and files.

    Inherits access_control from `KnowledgeModel`. See `KnowledgeModel.access_control`
    for complete documentation of the access control structure and permissions.
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

    Dict Fields:
        - `read` (dict, optional): Read access permissions
        - `write` (dict, optional): Write access permissions
        - `read.group_ids` (list[str], optional): List of group IDs with read access
        - `read.user_ids` (list[str], optional): List of user IDs with read access
        - `write.group_ids` (list[str], optional): List of group IDs with write access
        - `write.user_ids` (list[str], optional): List of user IDs with write access
    """


class KnowledgeFilesResponse(KnowledgeResponse):
    """
    Represents a knowledge base response with full file metadata.

    Inherits access_control from `KnowledgeModel`. Access control determines who can read and write to this knowledge base.
    """

    files: list[FileMetadataResponse]
    """List of files associated with the knowledge base."""

    warnings: Optional[dict] = None
    """
    Warnings returned during processing, e.g., if some files failed to process in a batch operation.

    Dict Fields:
        - `message` (str, required): Human-readable warning message describing the issue
        - `errors` (list[str], required): List of specific error details for failed operations
    """


class KnowledgeFileIdForm(BaseModel):
    """
    Form for adding or removing a file from a knowledge base.
    """

    file_id: str
    """The ID of the file to add or remove."""
