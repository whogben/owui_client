"""
Models for Memory-related operations.

Memories are durable per-user notes the backend recalls to give a model
context across chats. Since Open WebUI 0.10.0 the memory system distinguishes
two `type`s of memory (`user` vs `context`), optionally scopes each under a
hierarchical `path`, and tracks provenance in a backend-managed `meta` dict.
"""

from typing import Any, Literal, Optional
from pydantic import BaseModel, ConfigDict


class MemoryModel(BaseModel):
    """
    Represents a memory item stored for a user.

    Memories are split by `type` into durable personal facts (`user`) versus
    reusable conversation `context`, and optionally scoped under a
    slash-delimited `path`. The `meta` dict is populated by the backend to
    record provenance (creator, source chat/message/model) and is merged
    additively on updates; it is never set by client request forms.
    """

    id: str
    """Unique identifier for the memory."""

    user_id: str
    """ID of the user who owns this memory."""

    type: Literal["user", "context"] = "context"
    """Memory category. `user` = long-lived personal facts/preferences/instructions; `context` = other durable context that may help future chats. Defaults to `context`."""

    path: Optional[str] = None
    """Optional slash-delimited scope path (e.g. `projects/alpha`) used to group and hierarchically navigate memories. `None` means unscoped/global; normalized server-side (leading/trailing slashes stripped, consecutive slashes collapsed, empty segments / `.` / `..` / control chars rejected)."""

    content: str
    """The actual text content of the memory."""

    meta: Optional[dict] = None
    """Backend-managed provenance metadata; never set by client forms and merged additively on update.

    Dict Fields:
        - `created_by` (str, optional): Origin of the memory. One of `manual`, `tool`, or `background_review`.
        - `chat_id` (str, optional): ID of the chat that produced the memory (set for `tool`/`background_review` sources).
        - `message_id` (str, optional): ID of the message that produced the memory (set for `tool`/`background_review` sources).
        - `model` (str, optional): Model ID that produced the memory (set for `tool`/`background_review` sources).
    """

    updated_at: int
    """Unix timestamp (epoch) of when the memory was last updated."""

    created_at: int
    """Unix timestamp (epoch) of when the memory was created."""

    model_config = ConfigDict(from_attributes=True)


class AddMemoryForm(BaseModel):
    """
    Form for adding a new memory.

    The backend model defaults `type` to `context`, but the Open WebUI
    frontend (`addNewMemory`) sends `type='user'` by default, so manually
    added memories are usually `user` typed in practice.
    """

    content: str
    """The text content to be stored as memory (must be non-empty after trimming)."""

    type: Literal["user", "context"] = "context"
    """Memory category to create. `user` = long-lived personal fact/preference/instruction; `context` = durable conversation context. Defaults to `context`."""

    path: Optional[str] = None
    """Optional slash-delimited scope path (e.g. `projects/alpha`). `None` or empty creates an unscoped/global memory; normalized server-side."""


class MemoryUpdateModel(BaseModel):
    """
    Form for updating an existing memory.

    All fields are optional. Because the client serializes with
    `exclude_none=True`, `path`/`type` only reach the server when given a
    non-`None` value. Omitting all of `content`, `type`, and `path` is
    rejected by the server with HTTP 400.
    """

    content: Optional[str] = None
    """New text content for the memory. If provided, replaces the existing content (must be non-empty after trimming)."""

    type: Optional[Literal["user", "context"]] = None
    """New memory category. `None` leaves the type unchanged."""

    path: Optional[str] = None
    """New scope path for the memory; provide a non-`None` value to change it (the client omits `None`, so `None` here is treated as "leave unchanged" rather than "clear")."""


class QueryMemoryForm(BaseModel):
    """
    Form for querying memories using vector search.
    """

    content: str
    """The search query text."""

    k: Optional[int] = 1
    """The number of results to return. Defaults to 1."""


class ListMemoryPathsForm(BaseModel):
    """
    Form for `POST /memories/paths` — list memory paths grouped into a tree.

    Groups memories by `(path, type)` and returns one entry per group with a
    member count, most-recent `updated_at`, and immediate child paths.
    """

    query: Optional[str] = None
    """Optional case-insensitive substring filtered against each memory's `content` and `path`. `None`/empty matches all."""

    type: Literal["user", "context", "all"] = "all"
    """Restrict grouping to a memory category, or `all` (default) to include both."""

    limit: int = 100
    """Maximum number of path groups to return (clamped server-side to 1..500). Defaults to 100."""


class ReadMemoryPathForm(BaseModel):
    """
    Form for `POST /memories/path` — read the memories at a specific path.

    Returns the memories located exactly at `path` plus, optionally, those in
    descendant paths, along with the ancestor (`parents`) and immediate child
    paths for navigation.
    """

    path: str
    """Required slash-delimited scope path to read (e.g. `projects/alpha`). Normalized server-side; an empty/invalid path yields HTTP 400."""

    type: Literal["user", "context", "all"] = "all"
    """Restrict results to a memory category, or `all` (default) to include both."""

    include_children: bool = True
    """When `True` (default), also include memories in descendant paths of `path`."""

    limit: int = 50
    """Maximum number of memory rows to return (clamped server-side to 1..100). Defaults to 50."""
