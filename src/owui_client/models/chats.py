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
    This dictionary represents the complete chat structure used throughout the Open WebUI system.

    Dict Fields:
        - `title` (str, optional): The title of the chat conversation
        - `name` (str, optional): Alternative name for the chat
        - `description` (str, optional): Description of the chat
        - `tags` (list[str], optional): List of tag names associated with this chat
        - `history` (dict, required): Contains the conversation history with:
            - `currentId` (str, required): ID of the current message in the conversation
            - `messages` (dict[str, object], required): Map of message IDs to message objects
        - `models` (list[str], optional): List of model IDs used in this chat
        - `params` (dict, optional): Model parameters and configuration
        - `options` (dict, optional): Additional chat options and settings
        - `timestamp` (int, optional): Creation timestamp (Unix epoch)
        - `originalChatId` (str, optional): ID of the original chat if this is a clone
        - `branchPointMessageId` (str, optional): Message ID where branching occurred for cloned chats

    The `chat` dictionary is the core data structure that stores all conversation state,
    message history, and metadata. It's used for creating, updating, and managing chats.
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

    The meta dictionary stores various metadata about the chat, primarily used for organizational and filtering purposes.
    This field is used extensively throughout the Open WebUI system for tagging, searching, and managing chats.

    Dict Fields:
        - `tags` (list[str], optional): List of tag identifiers associated with this chat for categorization and filtering.
          Tags are used throughout the system for organizing chats and enabling tag-based search functionality.
          When chats are archived, tags may be automatically cleaned up if no other chats use them.
          Tag names are normalized to lowercase with spaces replaced by underscores (e.g., "my tag" becomes "my_tag").

    The meta field is preserved when chats are cloned, shared, or imported, maintaining the organizational structure.
    It plays a crucial role in the chat management system, particularly in tag-based operations.
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

    Contains the full conversation state including messages, metadata, and configuration.
    This dictionary represents the complete chat structure used throughout the Open WebUI system.

    Dict Fields:
        - `title` (str, optional): The title of the chat conversation
        - `name` (str, optional): Alternative name for the chat
        - `description` (str, optional): Description of the chat
        - `tags` (list[str], optional): List of tag names associated with this chat
        - `history` (dict, required): Contains the conversation history with:
            - `currentId` (str, required): ID of the current message in the conversation
            - `messages` (dict[str, object], required): Map of message IDs to message objects
        - `models` (list[str], optional): List of model IDs used in this chat
        - `params` (dict, optional): Model parameters and configuration
        - `options` (dict, optional): Additional chat options and settings
        - `timestamp` (int, optional): Creation timestamp (Unix epoch)
        - `originalChatId` (str, optional): ID of the original chat if this is a clone
        - `branchPointMessageId` (str, optional): Message ID where branching occurred for cloned chats

    The `chat` dictionary is the core data structure that stores all conversation state,
    message history, and metadata. It's used for creating, updating, and managing chats.
    """

    folder_id: Optional[str] = None
    """Optional ID of the folder to place this chat in."""


class ChatImportForm(ChatForm):
    """
    Form for importing a chat, including metadata and timestamps.

    This form extends `ChatForm` to include additional metadata and timestamps
    for chat import operations. The chat attribute contains the complete
    conversation state including messages, metadata, and configuration.
    """

    meta: Optional[dict] = {}
    """Metadata for the chat import operation.

    Dict Fields:
        - `tags` (list[str], optional): List of tag names associated with this chat for categorization and filtering

    The meta dictionary stores additional metadata about the chat, primarily used for organizational purposes.
    The most common and well-documented key is 'tags', which allows chats to be categorized and filtered.
    """

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
    """List of message objects from the chat history.

    Dict Fields:
        - `role` (str, required): The role of the message sender, typically 'user' or 'assistant'
        - `content` (str, required): The text content of the message
        - `timestamp` (float, optional): UNIX timestamp (seconds since epoch) when the message was created
        - `model` (str, optional): The model identifier used for generating assistant messages (e.g., 'gpt-4', 'claude-3')

    This list contains the complete conversation history in chronological order, used for PDF generation
    and other export operations. Each message represents one turn in the conversation between user and assistant.
    """


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
    """The full chat content and history.

    Contains the messages, model configuration, and other conversation state.
    This dictionary represents the complete chat structure used throughout the Open WebUI system.

    Dict Fields:
        - `title` (str, optional): The title of the chat conversation
        - `name` (str, optional): Alternative name for the chat
        - `description` (str, optional): Description of the chat
        - `tags` (list[str], optional): List of tag names associated with this chat
        - `history` (dict, required): Contains the conversation history with:
            - `currentId` (str, required): ID of the current message in the conversation
            - `messages` (dict[str, object], required): Map of message IDs to message objects
        - `models` (list[str], optional): List of model IDs used in this chat
        - `params` (dict, optional): Model parameters and configuration
        - `options` (dict, optional): Additional chat options and settings
        - `timestamp` (int, optional): Creation timestamp (Unix epoch)
        - `originalChatId` (str, optional): ID of the original chat if this is a clone
        - `branchPointMessageId` (str, optional): Message ID where branching occurred for cloned chats

    The `chat` dictionary is the core data structure that stores all conversation state,
    message history, and metadata. It's used for creating, updating, and managing chats.
    """

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
    """Additional metadata for the chat.

    The meta dictionary stores various metadata about the chat, primarily used for organizational and filtering purposes.
    This field is used extensively throughout the Open WebUI system for tagging, searching, and managing chats.

    Dict Fields:
        - `tags` (list[str], optional): List of tag identifiers associated with this chat for categorization and filtering.
          Tags are used throughout the system for organizing chats and enabling tag-based search functionality.
          When chats are archived, tags may be automatically cleaned up if no other chats use them.
          Tag names are normalized to lowercase with spaces replaced by underscores (e.g., "my tag" becomes "my_tag").

    The meta field is preserved when chats are cloned, shared, or imported, maintaining the organizational structure.
    It plays a crucial role in the chat management system, particularly in tag-based operations.
    """

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
    """The data payload for the event.

    Contains event-specific data that varies based on the event type.
    This dictionary holds the actual content and metadata for the event being triggered.

    Dict Fields:
        - `content` (str, optional): Text content for message-related events (used in 'message' and 'replace' event types)
        - `embeds` (list, optional): List of embed objects for embed-related events
        - `files` (list, optional): List of file objects for file-related events
        - `status` (dict, optional): Status information for status-related events
        - `type` (str, optional): Additional type specification for certain event types
        - `source` (dict, optional): Source information for source/citation events
        - `citation` (dict, optional): Citation information for source/citation events

    The data structure is event-type specific:
    - For 'message' events: contains `content` field with additional message text
    - For 'replace' events: contains `content` field with replacement message text
    - For 'embeds' events: contains `embeds` field with list of embed objects
    - For 'files' events: contains `files` field with list of file objects
    - For 'status' events: contains status information in the data object
    - For 'source'/'citation' events: contains source/citation data with optional `type` field

    Event types discovered in backend code:
    - 'status': Updates message status information
    - 'message': Appends content to existing messages
    - 'replace': Replaces entire message content
    - 'embeds': Adds embed objects to messages
    - 'files': Adds file objects to messages
    - 'source'/'citation': Handles source and citation data

    The data field is passed through the event emission system and processed based on the event type.
    """


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
