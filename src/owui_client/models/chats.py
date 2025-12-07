from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class ChatModel(BaseModel):
    """
    Represents a chat conversation in the Open WebUI system.

    This model stores the core chat data including the conversation history,
    metadata, and status flags like archived or pinned.
    """
    model_config = ConfigDict(from_attributes=True)

    id: str
    """Unique identifier for the chat."""

    user_id: str
    """The ID of the user who owns this chat."""

    title: str
    """The title of the chat conversation."""

    chat: dict
    """
    The full chat content and history.

    Contains the messages, model configuration, and other conversation state.
    Key fields typically include:
    - `history`: Dict containing `messages` (map of message IDs to message objects) and `currentId`.
    - `models`: List of model IDs used in this chat.
    - `params`: Model parameters used.
    """

    created_at: int
    """Timestamp when the chat was created (Unix epoch)."""

    updated_at: int
    """Timestamp when the chat was last updated (Unix epoch)."""

    share_id: Optional[str] = None
    """
    ID of the shared version of this chat, if shared.
    
    If set, this points to a separate read-only copy of the chat accessible via sharing.
    """

    archived: bool = False
    """Whether the chat has been archived."""

    pinned: Optional[bool] = False
    """Whether the chat is pinned to the top of the list."""
    
    meta: dict = {}
    """
    Additional metadata for the chat.
    
    Common keys:
    - `tags`: List of tag names associated with this chat.
    """

    folder_id: Optional[str] = None
    """ID of the folder containing this chat, if any."""

class ChatForm(BaseModel):
    """
    Form for creating or updating a chat.
    """
    chat: dict
    """
    The chat content.
    
    Must minimally contain the `history` or initial state of the conversation.
    """

    folder_id: Optional[str] = None
    """Optional ID of the folder to place this chat in."""

class ChatImportForm(ChatForm):
    """
    Form for importing a chat, including metadata and timestamps.
    """
    meta: Optional[dict] = {}
    """Metadata for the chat (e.g., tags)."""

    pinned: Optional[bool] = False
    """Whether the imported chat should be pinned."""

    created_at: Optional[int] = None
    """Original creation timestamp (Unix epoch)."""

    updated_at: Optional[int] = None
    """Original update timestamp (Unix epoch)."""

class ChatsImportForm(BaseModel):
    """
    Form for importing multiple chats at once.
    """
    chats: List[ChatImportForm]
    """List of chats to import."""

class ChatTitleMessagesForm(BaseModel):
    """
    Form containing a title and messages, used for utility operations like PDF generation.
    """
    title: str
    """Title of the chat."""

    messages: List[dict]
    """List of message objects from the chat history."""

class ChatTitleForm(BaseModel):
    """
    Form for updating a chat title.
    """
    title: str
    """The new title."""

class ChatResponse(BaseModel):
    """
    Response model for chat operations.
    """
    id: str
    """Unique identifier for the chat."""

    user_id: str
    """The ID of the user who owns this chat."""

    title: str
    """The title of the chat conversation."""

    chat: dict
    """The full chat content and history."""

    updated_at: int
    """Timestamp when the chat was last updated (Unix epoch)."""

    created_at: int
    """Timestamp when the chat was created (Unix epoch)."""

    share_id: Optional[str] = None
    """ID of the shared version of this chat, if shared."""

    archived: bool
    """Whether the chat has been archived."""

    pinned: Optional[bool] = False
    """Whether the chat is pinned."""

    meta: dict = {}
    """Additional metadata for the chat."""

    folder_id: Optional[str] = None
    """ID of the folder containing this chat, if any."""

class ChatTitleIdResponse(BaseModel):
    """
    Lightweight chat response containing only essential metadata.
    
    Used for list views to reduce payload size.
    """
    id: str
    """Unique identifier for the chat."""

    title: str
    """The title of the chat conversation."""

    updated_at: int
    """Timestamp when the chat was last updated (Unix epoch)."""

    created_at: int
    """Timestamp when the chat was created (Unix epoch)."""

# Models from router
class TagForm(BaseModel):
    """
    Form for adding a tag to a chat.
    """
    name: str
    """The name of the tag."""

class TagFilterForm(TagForm):
    """
    Form for filtering chats by tag.
    """
    skip: Optional[int] = 0
    """Number of items to skip."""
    
    limit: Optional[int] = 50
    """Maximum number of items to return."""

class MessageForm(BaseModel):
    """
    Form for updating a specific message content.
    """
    content: str
    """The new content of the message."""

class EventForm(BaseModel):
    """
    Form for sending an event related to a specific message.
    
    Used to trigger socket events for a message.
    """
    type: str
    """The type of event."""
    
    data: dict
    """The data payload for the event."""

class CloneForm(BaseModel):
    """
    Form for cloning a chat.
    """
    title: Optional[str] = None
    """Optional new title for the cloned chat."""

class ChatFolderIdForm(BaseModel):
    """
    Form for moving a chat to a folder.
    """
    folder_id: Optional[str] = None
    """The ID of the target folder, or None to remove from folder."""

