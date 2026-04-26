from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any, Union


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

    tasks: Optional[list] = None
    """List of tasks associated with this chat.

    Tasks represent background operations or automation runs linked to the chat.
    Each item is a task object describing its type, status, and result.
    """

    summary: Optional[str] = None
    """Summary or digest of the chat conversation."""

    last_read_at: Optional[int] = None
    """Timestamp when the chat was last read by the user (Unix epoch)."""


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

    tasks: Optional[list] = None
    """List of tasks associated with this chat.

    Tasks represent background operations or automation runs linked to the chat.
    Each item is a task object describing its type, status, and result.
    """

    summary: Optional[str] = None
    """Summary or digest of the chat conversation."""


class ChatListResponse(BaseModel):
    """
    Response model for a list of chats with pagination.
    """

    items: list[ChatModel]
    """List of chat items."""

    total: int
    """Total number of chats."""


class ChatUsageStatsResponse(BaseModel):
    """
    Response model for chat usage statistics.
    """

    id: str
    """Unique identifier for the chat."""

    models: dict = {}
    """Models used in the chat with their usage counts.

    Dict Fields:
        - `key` (str): The model ID.
        - `value` (int): The usage count for that model.
    """

    message_count: int
    """Number of messages in the chat."""

    history_models: dict = {}
    """Models used in the chat history with their usage counts.

    Dict Fields:
        - `key` (str): The model ID.
        - `value` (int): The usage count for that model.
    """

    history_message_count: int
    """Number of messages in the chat history."""

    history_user_message_count: int
    """Number of user messages in the chat history."""

    history_assistant_message_count: int
    """Number of assistant messages in the chat history."""

    average_response_time: float
    """Average response time of assistant messages in seconds."""

    average_user_message_content_length: float
    """Average length of user message contents."""

    average_assistant_message_content_length: float
    """Average length of assistant message contents."""

    tags: list[str] = []
    """Tags associated with the chat."""

    last_message_at: int
    """Timestamp of the last message (epoch)."""

    updated_at: int
    """Timestamp when the chat was last updated (epoch)."""

    created_at: int
    """Timestamp when the chat was created (epoch)."""

    model_config = ConfigDict(extra="allow")


class ChatUsageStatsListResponse(BaseModel):
    """
    Response model for a list of chat usage statistics with pagination.
    """

    items: list[ChatUsageStatsResponse]
    """List of chat usage statistics."""

    total: int
    """Total number of chats."""

    model_config = ConfigDict(extra="allow")


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

    last_read_at: Optional[int] = None
    """Timestamp when the chat was last read by the user (Unix epoch)."""


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


class ChatAccessGrantsForm(BaseModel):
    """Form for updating access grants on a shared chat."""

    access_grants: list[dict]
    """List of access grants to apply to the shared chat.

    Dict Fields:
        - `principal_type` (str, required): Type of principal. Valid values: "user", "group"
        - `principal_id` (str, required): ID of the user or group, or "*" for wildcard/public access
        - `permission` (str, optional): Permission level. Valid values: "read", "write". Defaults to "read"
    """


class MessageStats(BaseModel):
    """
    Statistics for a single message.
    """

    id: str
    """Unique identifier for the message."""

    role: str
    """The role of the message sender (e.g., 'user', 'assistant')."""

    model: Optional[str] = None
    """The model used to generate the message (if assistant)."""

    content_length: int
    """Length of the message content."""

    token_count: Optional[int] = None
    """Number of tokens in the message."""

    timestamp: Optional[int] = None
    """Timestamp of the message."""

    rating: Optional[int] = None
    """Rating of the message."""

    tags: Optional[list[str]] = None
    """Tags associated with the message."""


class ChatHistoryStats(BaseModel):
    """
    Statistics for chat history.
    """

    messages: dict[str, MessageStats]
    """
    Map of message IDs to message statistics.

    Dict Fields:
        - `key` (str): Message ID
        - `value` (MessageStats): Statistics for the message
    """

    currentId: Optional[str] = None
    """ID of the current message in the conversation."""


class ChatBody(BaseModel):
    """
    Body of a chat with history statistics.
    """

    history: ChatHistoryStats
    """History statistics for the chat."""


class AggregateChatStats(BaseModel):
    """
    Aggregated statistics for a chat session.

    Includes metrics such as average response time, message length, and model usage counts.
    """

    average_response_time: float
    """Average response time of assistant messages in seconds."""

    average_user_message_content_length: float
    """Average length of user message contents."""

    average_assistant_message_content_length: float
    """Average length of assistant message contents."""

    models: dict[str, int]
    """
    Counts of models used in the current message path.

    Dict Fields:
        - `key` (str): Model ID
        - `value` (int): Usage count
    """

    message_count: int
    """Total number of messages in the current path."""

    history_models: dict[str, int]
    """
    Counts of models used in the entire history.

    Dict Fields:
        - `key` (str): Model ID
        - `value` (int): Usage count
    """

    history_message_count: int
    """Total number of messages in the history."""

    history_user_message_count: int
    """Total number of user messages in the history."""

    history_assistant_message_count: int
    """Total number of assistant messages in the history."""


class ChatStatsExport(BaseModel):
    """
    Export model for chat statistics.
    """

    id: str
    """Unique identifier for the chat."""

    user_id: str
    """ID of the user who owns the chat."""

    created_at: int
    """Timestamp when the chat was created."""

    updated_at: int
    """Timestamp when the chat was last updated."""

    tags: list[str] = []
    """List of tags associated with the chat."""

    stats: AggregateChatStats
    """Aggregated statistics for the chat."""

    chat: ChatBody
    """Body of the chat containing history statistics."""


class ChatStatsExportList(BaseModel):
    """
    List of exported chat statistics.
    """

    type: str = "chats"
    """Type of export (default: 'chats')."""

    items: list[ChatStatsExport]
    """List of chat export items."""

    total: int
    """Total number of items."""

    page: int
    """Current page number."""


class ChatCompletionForm(BaseModel):
    """
    Request form for chat completion generation.

    This model accepts OpenAI-compatible chat completion parameters along with
    Open WebUI-specific metadata for chat management, file attachments, tools, and more.
    Uses `extra="allow"` to pass through any additional OpenAI API parameters.
    """

    model: str
    """The model ID to use for generation (e.g., "gpt-4", "claude-3")."""

    messages: list[dict]
    """List of message objects representing the conversation history.

    Dict Fields:
        - `role` (str, required): The role of the message sender. Valid values: "system", "user", "assistant", "tool"
        - `content` (str or list, required): The message content. Can be a string or a list of content blocks (for multimodal)
        - `name` (str, optional): Name of the participant (for role-based naming)
        - `tool_calls` (list, optional): List of tool calls made by the assistant
        - `tool_call_id` (str, optional): ID of the tool call being responded to (for tool role)
    """

    chat_id: Optional[str] = None
    """Optional chat ID to associate this completion with an existing chat."""

    id: Optional[str] = None
    """Optional message ID for the user message being completed."""

    parent_message: Optional[dict] = None
    """Optional parent message object for threading.

    Dict Fields:
        - `id` (str, required): The parent message ID
        - `role` (str, required): The parent message role
        - `content` (str, required): The parent message content
        - Additional message metadata fields
    """

    parent_id: Optional[str] = None
    """Optional parent message ID for threading."""

    session_id: Optional[str] = None
    """Optional session ID for async processing. When provided, returns a task_id instead of the completion."""

    filter_ids: Optional[list[str]] = None
    """Optional list of filter IDs to apply for retrieval-augmented generation."""

    tool_ids: Optional[list[str]] = None
    """Optional list of tool IDs to make available to the model."""

    tool_servers: Optional[dict] = None
    """Optional tool server configurations.

    Dict Fields:
        - Server-specific configuration for MCP (Model Context Protocol) tools
        - Connection details and authentication for external tool servers
    """

    files: Optional[list[dict]] = None
    """Optional list of file attachments for multimodal inputs.

    Dict Fields:
        - `id` (str, required): File ID
        - `type` (str, required): File type (e.g., "file", "image")
        - `name` (str, optional): File name
        - Additional file metadata
    """

    features: Optional[dict] = None
    """Optional feature flags and configurations.

    Dict Fields:
        - Feature-specific settings for enabling/disabling capabilities
        - Experimental feature flags
    """

    variables: Optional[dict] = None
    """Optional template variables for prompt templating.

    Dict Fields:
        - Variable name to value mappings
        - Used for substituting placeholders in system prompts or templates
    """

    params: Optional[dict] = None
    """Optional model parameters and generation settings.

    Dict Fields:
        - `stream_delta_chunk_size` (int, optional): Chunk size for streaming responses
        - `reasoning_tags` (str, optional): Tags for reasoning output
        - `function_calling` (str, optional): Function calling mode. Valid values: "native", "default"
    """

    model_item: Optional[dict] = None
    """Optional direct model configuration for bypassing model registry.

    Dict Fields:
        - `direct` (bool, required): Must be True to use direct model configuration
        - Model-specific configuration fields (base_url, api_key, etc.)
    """

    background_tasks: Optional[list] = None
    """Optional background tasks to execute after completion."""

    stream: Optional[bool] = None
    """Whether to stream the response as SSE events."""

    temperature: Optional[float] = None
    """Sampling temperature between 0.0 and 2.0."""

    max_tokens: Optional[int] = None
    """Maximum number of tokens to generate."""

    top_p: Optional[float] = None
    """Nucleus sampling parameter between 0.0 and 1.0."""

    frequency_penalty: Optional[float] = None
    """Frequency penalty between -2.0 and 2.0."""

    presence_penalty: Optional[float] = None
    """Presence penalty between -2.0 and 2.0."""

    stop: Optional[Union[str, list[str]]] = None
    """Stop sequences where generation should halt."""

    model_config = ConfigDict(extra="allow")


class ChatCompletionResponse(BaseModel):
    """
    Response model for chat completion.

    The response format varies based on whether the request was processed synchronously
    or asynchronously (when session_id is provided).
    """

    status: Optional[bool] = None
    """Status flag for async responses. True if task was created successfully."""

    task_id: Optional[str] = None
    """Task ID for async processing. Present when session_id is provided in the request."""

    model_config = ConfigDict(extra="allow")


class ChatCompletedForm(BaseModel):
    """
    Form for notifying that a chat completion has been generated.

    This endpoint is called after a chat completion is generated to process
    outlet filters that may modify the response. The form contains the
    completed message and associated metadata.
    """

    model: str
    """The model ID used for generation."""

    messages: list[str]
    """List of message IDs in the conversation."""

    chat_id: str
    """The ID of the chat this completion belongs to."""

    session_id: str
    """The session ID for the chat session."""

    id: Optional[str] = None
    """The ID of the completed message."""

    filter_ids: Optional[list[str]] = None
    """Optional list of filter IDs to apply for outlet processing."""

    model_config = ConfigDict(extra="allow")


class ChatCompletedResponse(BaseModel):
    """
    Response model for chat completed endpoint.

    Returns the modified form data after processing outlet filters.
    The structure matches the request form but may be modified by filters.
    """

    model_config = ConfigDict(extra="allow")


class ChatActionForm(BaseModel):
    """
    Form for executing a chat action.

    This form is used to trigger custom actions (functions) that can process
    chat messages and return results. Actions are user-defined functions that
    can perform arbitrary operations on chat data.
    """

    model: str
    """The model ID to use for the action."""

    messages: list[str]
    """List of message IDs in the conversation."""

    chat_id: str
    """The ID of the chat this action belongs to."""

    id: str
    """The ID of the message being acted upon."""

    session_id: str
    """The session ID for the chat session."""

    model_item: Optional[dict] = None
    """Optional direct model configuration for bypassing model registry.

    Dict Fields:
        - `direct` (bool, required): Must be True to use direct model configuration
        - Model-specific configuration fields (base_url, api_key, etc.)
    """

    model_config = ConfigDict(extra="allow")


class ChatActionResponse(BaseModel):
    """
    Response model for chat action endpoint.

    The response structure varies based on the action function being executed.
    Actions can return any data type, so this model uses extra="allow"
    to accommodate arbitrary response structures.
    """

    model_config = ConfigDict(extra="allow")
