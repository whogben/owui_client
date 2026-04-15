from typing import Optional
from pydantic import BaseModel, ConfigDict


"""
Models for File management.
"""


class FileMeta(BaseModel):
    """
    Metadata information for a file.

    This model is flexible and allows extra fields, but defines common metadata fields used by the system.
    """

    name: Optional[str] = None
    """Original name of the file."""

    content_type: Optional[str] = None
    """MIME type of the file (e.g., 'application/pdf', 'image/png')."""

    size: Optional[int] = None
    """Size of the file in bytes."""

    model_config = ConfigDict(extra="allow")


class FileModelResponse(BaseModel):
    """
    Response model for file operations, containing file details and metadata.
    """

    id: str
    """Unique identifier for the file."""

    user_id: str
    """ID of the user who uploaded or owns the file."""

    hash: Optional[str] = None
    """MD5 or other hash of the file content for integrity verification."""

    filename: str
    """Name of the file as stored in the system (often UUID prefixed)."""

    data: Optional[dict] = None
    """Additional data associated with the file, such as processing status or extracted content.

    Dict Fields:
        - `status` (str, optional): Processing status of the file - 'pending', 'completed', or 'failed'
        - `error` (str, optional): Error message if file processing failed
        - `content` (str, optional): Extracted text content from the file

    The data dictionary stores file processing metadata and content. During file upload, the status starts as 'pending',
    changes to 'completed' when processing succeeds, or 'failed' with an error message when processing fails.
    The content field contains the extracted text from the file after successful processing.
    """

    meta: Optional[FileMeta] = None
    """Metadata about the file including original name, size, and content type."""

    created_at: int
    """Unix timestamp when the file was created."""

    updated_at: Optional[int] = None
    """Unix timestamp when the file was last updated. Optional for legacy files."""

    model_config = ConfigDict(extra="allow")


class FileMetadataResponse(BaseModel):
    """
    Simplified response model focusing on file metadata.
    """

    id: str
    """Unique identifier for the file."""

    hash: Optional[str] = None
    """File content hash."""

    meta: Optional[dict] = None
    """File metadata dictionary.

    Dict Fields:
        - `name` (str, optional): Original name of the file
        - `content_type` (str, optional): MIME type of the file (e.g., 'application/pdf', 'image/png')
        - `size` (int, optional): Size of the file in bytes
        - `data` (dict, optional): Additional metadata associated with the file
    """

    created_at: int
    """Unix timestamp when the file was created."""

    updated_at: int
    """Unix timestamp when the file was last updated."""


class FileModel(BaseModel):
    """
    Complete internal representation of a file in the system.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    """Unique identifier for the file."""

    user_id: str
    """ID of the user who owns the file."""

    hash: Optional[str] = None
    """File content hash."""

    filename: str
    """Name of the file as stored."""

    path: Optional[str] = None
    """Physical path or storage reference for the file content."""

    data: Optional[dict] = None
    """Additional data associated with the file, including processing status and extracted content.

    Dict Fields:
        - `status` (str, optional): Processing status of the file - 'pending', 'completed', or 'failed'
        - `error` (str, optional): Error message if file processing failed
        - `content` (str, optional): Extracted text content from the file
    """

    meta: Optional[dict] = None
    """File metadata containing information about the file.

    Dict Fields:
        - `name` (str, optional): Original name of the file as uploaded
        - `content_type` (str, optional): MIME type of the file (e.g., 'application/pdf', 'image/png', 'text/plain')
        - `size` (int, optional): Size of the file in bytes
        - `data` (dict, optional): Additional metadata associated with the file, can contain custom key-value pairs
        - `collection_name` (str, optional): Knowledge base collection name this file belongs to, used for access control

    The meta dictionary stores core file attributes and can be extended with additional custom metadata.
    Common usage includes file identification, content type handling, and knowledge base association.
    """

    created_at: Optional[int]
    """Unix timestamp when the file was created."""

    updated_at: Optional[int]
    """Unix timestamp when the file was last updated."""


class FileForm(BaseModel):
    """Form for creating a new file."""

    id: str
    """Unique identifier for the file."""

    hash: Optional[str] = None
    """Hash of the file content for integrity verification."""

    filename: str
    """Name of the file."""

    path: str
    """Physical path or storage reference for the file content."""

    data: dict = {}
    """Additional data associated with the file.

    Dict Fields:
        - `status` (str, optional): Processing status - 'pending', 'completed', or 'failed'
        - `error` (str, optional): Error message if processing failed
        - `content` (str, optional): Extracted text content from the file
    """

    meta: dict = {}
    """File metadata dictionary.

    Dict Fields:
        - `name` (str, optional): Original name of the file
        - `content_type` (str, optional): MIME type (e.g., 'application/pdf')
        - `size` (int, optional): Size of the file in bytes
    """


class FileUpdateForm(BaseModel):
    """Form for updating an existing file."""

    hash: Optional[str] = None
    """Hash of the file content for integrity verification."""

    data: Optional[dict] = None
    """Additional data to merge into the file's existing data.

    Dict Fields:
        - `status` (str, optional): Processing status - 'pending', 'completed', or 'failed'
        - `error` (str, optional): Error message if processing failed
        - `content` (str, optional): Extracted text content from the file
    """

    meta: Optional[dict] = None
    """Metadata to merge into the file's existing metadata.

    Dict Fields:
        - `name` (str, optional): Original name of the file
        - `content_type` (str, optional): MIME type (e.g., 'application/pdf')
        - `size` (int, optional): Size of the file in bytes
    """


class FileListResponse(BaseModel):
    """Paginated list of file responses."""

    items: list[FileModelResponse]
    """List of file response items."""

    total: int
    """Total number of files matching the query."""


class ContentForm(BaseModel):
    """
    Form for updating file content text.
    """

    content: str
    """The new text content for the file."""
