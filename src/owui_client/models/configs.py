from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any, Union

# Models for Configs router


class ImportConfigForm(BaseModel):
    """
    Form for importing system configuration.
    """

    config: Dict[str, Any]
    """The configuration dictionary to import. This should match the structure returned by the export endpoint.

Dict Fields:
    This dictionary contains the complete Open WebUI configuration that can be exported and imported.
    It includes all settings from the backend config system. For a complete reference of all possible
    keys and their descriptions, see the backend configuration in:
    owui_client/refs/owui_source_main/backend/open_webui/main.py

    The config includes but is not limited to:
    - API integrations (Ollama, OpenAI, etc.)
    - Feature flags (folders, channels, notes, etc.)
    - Authentication settings (OAuth, LDAP, etc.)
    - RAG and retrieval configurations
    - Image generation and editing settings
    - Audio processing configurations
    - Web search and loader configurations
    - Code execution and interpreter settings
    - UI and permission settings
    """


class ConnectionsConfigForm(BaseModel):
    """
    Configuration for system connections.
    """

    ENABLE_DIRECT_CONNECTIONS: bool
    """Whether to allow users to connect to their own OpenAI compatible API endpoints directly."""

    ENABLE_BASE_MODELS_CACHE: bool
    """Whether to cache the base model list. speeeds up access by fetching base models only at startup or on settings save."""


class OAuthClientRegistrationForm(BaseModel):
    """
    Form for registering an OAuth client.
    """

    url: str
    """The URL of the service to register with (e.g. Tool Server URL)."""

    client_id: str
    """Unique identifier for the client."""

    client_name: Optional[str] = None
    """Optional name for the client."""


class ToolServerConnection(BaseModel):
    """
    Configuration for a single tool server connection.
    """

    url: str
    """Base URL of the tool server."""

    path: str
    """Path/Prefix for the tools (e.g. /api/v1)."""

    type: Optional[str] = "openapi"
    """Type of tool server. Supported values: 'openapi', 'mcp'."""

    auth_type: Optional[str] = None
    """Authentication type. Common values: 'bearer', 'session', 'system_oauth', 'oauth_2.1'."""

    headers: Optional[Union[Dict[str, Any], str]] = None
    """Custom headers to send with requests to the tool server.

    Dict Fields:
        - `Authorization` (str, optional): Authorization header for tool server authentication
        - `Content-Type` (str, optional): Content type header for requests
        - `X-OpenWebUI-User-Name` (str, optional): User name header for user context
        - `X-OpenWebUI-Chat-Id` (str, optional): Chat ID header for context tracking
        - `Accept` (str, optional): Accept header for response content type
        - Any other custom headers needed for specific tool server requirements

    The headers dictionary allows customization of HTTP headers sent to tool servers.
    Common use cases include:
    - Adding authentication headers beyond the standard bearer token
    - Setting custom content types for specific API requirements
    - Forwarding user information headers when ENABLE_FORWARD_USER_INFO_HEADERS is enabled
    - Including chat context headers for tracking and logging purposes

    When provided as a string, it should be a JSON-encoded dictionary.
    """

    key: Optional[str] = None
    """API Key or Token for bearer auth."""

    config: Optional[Dict[str, Any]] = None
    """Additional configuration for the connection.

    Dict Fields:
        - `enable` (bool, optional): Whether the tool server connection is enabled. Defaults to True.
        - `function_name_filter_list` (str, optional): Comma-separated list of function names to filter/allow for this tool server. Used to restrict which functions from the tool server are exposed.
        - `access_control` (dict, optional): Access control configuration for the tool server connection. Defines permissions and restrictions for user access.
        - `oauth_server_key` (str, optional): OAuth server key for OAuth 2.1 authentication with MCP tool servers. Used during dynamic client registration.

    The config dictionary provides additional connection-specific settings that control
    behavior, security, and functionality of the tool server integration.
    """

    model_config = ConfigDict(extra="allow")


class ToolServersConfigForm(BaseModel):
    """
    Configuration for tool servers.
    """

    TOOL_SERVER_CONNECTIONS: List[ToolServerConnection]
    """List of configured tool server connections."""


class CodeInterpreterConfigForm(BaseModel):
    """
    Configuration for code execution and interpreter.
    """

    ENABLE_CODE_EXECUTION: bool
    """Enable general code execution (e.g. for tools)."""

    CODE_EXECUTION_ENGINE: str
    """Engine for code execution. Supported: 'pyodide', 'jupyter'."""

    CODE_EXECUTION_JUPYTER_URL: Optional[str] = None
    """URL for Jupyter server (if engine is jupyter)."""

    CODE_EXECUTION_JUPYTER_AUTH: Optional[str] = None
    """Auth method for Jupyter. Supported: 'token', 'password', or empty/None."""

    CODE_EXECUTION_JUPYTER_AUTH_TOKEN: Optional[str] = None
    """Token for Jupyter auth."""

    CODE_EXECUTION_JUPYTER_AUTH_PASSWORD: Optional[str] = None
    """Password for Jupyter auth."""

    CODE_EXECUTION_JUPYTER_TIMEOUT: Optional[int] = None
    """Timeout for code execution in seconds."""

    ENABLE_CODE_INTERPRETER: bool
    """Enable code interpreter feature (e.g. for chat)."""

    CODE_INTERPRETER_ENGINE: str
    """Engine for code interpreter. Supported: 'pyodide', 'jupyter'."""

    CODE_INTERPRETER_PROMPT_TEMPLATE: Optional[str] = None
    """Custom prompt template for the code interpreter."""

    CODE_INTERPRETER_JUPYTER_URL: Optional[str] = None
    """URL for Jupyter server (if interpreter engine is jupyter)."""

    CODE_INTERPRETER_JUPYTER_AUTH: Optional[str] = None
    """Auth method for Jupyter interpreter. Supported: 'token', 'password', or empty/None."""

    CODE_INTERPRETER_JUPYTER_AUTH_TOKEN: Optional[str] = None
    """Token for Jupyter interpreter auth."""

    CODE_INTERPRETER_JUPYTER_AUTH_PASSWORD: Optional[str] = None
    """Password for Jupyter interpreter auth."""

    CODE_INTERPRETER_JUPYTER_TIMEOUT: Optional[int] = None
    """Timeout for interpreter execution in seconds."""


class ModelsConfigForm(BaseModel):
    """
    Configuration for model defaults and ordering.
    """

    DEFAULT_MODELS: Optional[str] = None
    """Comma-separated list of default model IDs (e.g. for new chats)."""

    DEFAULT_PINNED_MODELS: Optional[str] = None
    """Comma-separated list of pinned model IDs."""

    MODEL_ORDER_LIST: Optional[List[str]] = None
    """List of model IDs specifying the display order."""


class PromptSuggestion(BaseModel):
    """
    A prompt suggestion for the chat interface.
    """

    title: List[str]
    """List containing [title, subtitle]. E.g. ["Tell me a fun fact", "about the Roman Empire"]."""

    content: str
    """The actual prompt content to be sent when selected."""


class SetDefaultSuggestionsForm(BaseModel):
    """
    Form for setting default prompt suggestions.
    """

    suggestions: List[PromptSuggestion]
    """List of prompt suggestions to set as default."""


class BannerModel(BaseModel):
    """
    Model representing a banner notification.
    """

    id: str
    """Unique ID of the banner."""

    type: str
    """Type of banner. Supported: 'info', 'warning', 'error', 'success'."""

    title: Optional[str] = None
    """Title of the banner (optional)."""

    content: str
    """Content of the banner. Supports Markdown."""

    dismissible: bool = True
    """Whether the banner can be dismissed by the user."""

    timestamp: int
    """Timestamp of creation/update."""


class SetBannersForm(BaseModel):
    """
    Form for setting banners.
    """

    banners: List[BannerModel]
    """List of banners to display."""
