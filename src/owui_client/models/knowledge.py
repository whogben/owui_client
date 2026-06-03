"""Knowledge base models, directory structures, and file management forms."""

from typing import Optional, Union
from pydantic import BaseModel, ConfigDict, Field

from owui_client.models.users import UserResponse
from owui_client.models.files import FileMetadataResponse, FileModelResponse
from owui_client.models.access_grants import AccessGrantModel


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

    access_grants: list[AccessGrantModel] = Field(default_factory=list)
    """
    List of access grants controlling who can read/write this knowledge base.
    Replaces the legacy access_control field.
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

    access_grants: Optional[list[dict]] = None
    """
    List of access grants for the knowledge base.
    
    Dict Fields:
    - `id` (str, optional): Unique identifier for the grant
    - `principal_type` (str, required): 'user' or 'group'
    - `principal_id` (str, required): User/group ID, or '*' for public access
    - `permission` (str, required): 'read' or 'write'
    """

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

    files: Optional[list[FileMetadataResponse]] = None
    """List of files associated with the knowledge base."""

    write_access: Optional[bool] = False
    """Whether the current user has write access to the knowledge base."""

    warnings: Optional[dict] = None
    """
    Warnings returned during processing, e.g., if some files failed to process in a batch operation.

    Dict Fields:
        - `message` (str, required): Human-readable warning message describing the issue
        - `errors` (list[str], required): List of specific error details for failed operations
    """


class KnowledgeAccessResponse(KnowledgeUserResponse):
    """
    Response model for knowledge base access information.
    """

    write_access: Optional[bool] = False
    """Whether the current user has write access."""


class KnowledgeAccessListResponse(BaseModel):
    """
    Response model for a list of knowledge bases with access info.
    """

    items: list[KnowledgeAccessResponse]
    """List of knowledge base access items."""

    total: int
    """Total number of items."""


class FileUserResponse(FileModelResponse):
    """
    File response with user details.
    """

    user: Optional[UserResponse] = None
    """The user who owns the file."""


class KnowledgeDirectoryModel(BaseModel):
    """
    Represents a directory within a knowledge base.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    """The unique identifier of the directory."""

    knowledge_id: str
    """The ID of the knowledge base this directory belongs to."""

    parent_id: Optional[str] = None
    """The ID of the parent directory, or None if this is a root directory."""

    name: str
    """The name of the directory."""

    user_id: str
    """The ID of the user who created the directory."""

    created_at: int
    """Timestamp of creation (epoch)."""

    updated_at: int
    """Timestamp of last update (epoch)."""


class KnowledgeDirectoryCreateForm(BaseModel):
    """
    Form for creating a new directory in a knowledge base.
    """

    name: str
    """The name of the new directory."""

    parent_id: Optional[str] = None
    """The ID of the parent directory. None for a root-level directory."""


class KnowledgeDirectoryUpdateForm(BaseModel):
    """
    Form for updating a directory in a knowledge base.
    """

    name: Optional[str] = None
    """New name for the directory. None to leave unchanged."""

    parent_id: Optional[str] = '__unset__'
    """New parent directory ID. Defaults to ``'__unset__'`` (leave unchanged). Set to ``None`` to move to root, or to a directory ID to relocate."""


class KnowledgeFileMoveForm(BaseModel):
    """
    Form for moving a file to a different directory within a knowledge base.
    """

    file_id: str
    """The ID of the file to move."""

    directory_id: Optional[str] = None
    """The target directory ID, or None to move to the root of the knowledge base."""


class FileManifestEntry(BaseModel):
    """
    Represents a file entry in a local manifest for sync diff comparison.
    """

    filename: str
    """The base filename (e.g., 'readme.md')."""

    path: str
    """The relative directory path (e.g., 'docs/api'), or '' for root."""

    checksum: str
    """SHA-256 checksum of the raw file bytes."""

    size: int
    """The file size in bytes."""


class SyncDiffForm(BaseModel):
    """
    Form for computing a sync diff against a knowledge base.
    """

    manifest: list[FileManifestEntry]
    """List of file manifest entries representing the local state."""


class SyncDiffResponse(BaseModel):
    """
    Response containing the diff between a local manifest and a knowledge base.
    """

    added: list[dict]
    """
    Files that exist locally but not in the knowledge base.

    Dict Fields:
        - `filename` (str, required): The base filename of the new file
        - `path` (str, required): The relative directory path, or '' for root
    """

    modified: list[dict]
    """
    Files that exist in both but differ (checksum mismatch).

    Dict Fields:
        - `filename` (str, required): The base filename
        - `path` (str, required): The relative directory path, or '' for root
        - `stale_file_id` (str, required): The file ID of the existing version to replace
    """

    deleted: list[dict]
    """
    Files that exist in the knowledge base but not in the local manifest.

    Dict Fields:
        - `file_id` (str, required): The ID of the file to remove
        - `filename` (str, required): The base filename
    """

    mkdir: list[str]
    """Directory paths that need to be created in the knowledge base."""

    rmdir: list[str]
    """Directory IDs that should be removed from the knowledge base."""

    unmodified_count: int
    """Number of files that are unchanged."""

    directory_map: dict[str, str]
    """
    Mapping of existing directory paths to their IDs in the knowledge base.

    Dict Fields:
        - Key (str): Directory path relative to the knowledge base root
        - Value (str): The directory's unique ID in the database
    """


class SyncCleanupForm(BaseModel):
    """
    Form for cleaning up stale files and directories after a sync.
    """

    file_ids: list[str]
    """List of file IDs to delete from the knowledge base."""

    dir_ids: list[str] = []
    """List of directory IDs to remove from the knowledge base."""


class KnowledgeFileListResponse(BaseModel):
    """
    Response model for a list of knowledge base files.
    """

    items: list[FileUserResponse]
    """List of file items."""

    directories: list[KnowledgeDirectoryModel] = []
    """List of directories at the current level in the knowledge base."""

    breadcrumbs: list[KnowledgeDirectoryModel] = []
    """Ordered list of ancestor directories from root to the current directory (for navigation)."""

    total: int
    """Total number of items."""""


class KnowledgeFileIdForm(BaseModel):
    """
    Form for adding or removing a file from a knowledge base.
    """

    file_id: str
    """The ID of the file to add or remove."""

    directory_id: Optional[str] = None
    """The directory to place the file in. None for root level."""""


class KnowledgeAccessGrantsForm(BaseModel):
    """
    Form for updating access grants on a knowledge base.
    """

    access_grants: list[dict]
    """
    List of access grants to set on the knowledge base.

    Dict Fields:
    - `id` (str, optional): Unique identifier for the grant
    - `principal_type` (str, required): 'user' or 'group'
    - `principal_id` (str, required): User/group ID, or '*' for public access
    - `permission` (str, required): 'read' or 'write'
    """
