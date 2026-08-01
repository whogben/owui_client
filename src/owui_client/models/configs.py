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

    client_secret: Optional[str] = None
    """Static OAuth client secret. When provided, skips dynamic registration and uses static credentials."""

    oauth_server_url: Optional[str] = None
    """Override for the OAuth server URL. Defaults to the url field if not provided."""

    oauth_scope: Optional[str] = None
    """OAuth scope(s) to request during client registration.

    A single string of whitespace- and/or comma-separated scope tokens
    (e.g. ``"openid email profile"`` or ``"openid,email,profile"``); the
    backend normalizes both separators. When omitted/None the backend falls
    back to the scopes advertised by the resource's Protected Resource
    Metadata (RFC 9728) during dynamic client registration.
    """


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

    info: Optional[Dict[str, Any]] = None
    """Server metadata and identification info.

    Dict Fields:
        - `id` (str, optional): Server identifier used for OAuth client management
        - `oauth_server_url` (str, optional): Override URL for the OAuth authorization server
        - Additional keys may be present depending on server type and configuration
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

    DEFAULT_MODEL_METADATA: Optional[dict] = None
    """Default metadata for models.

    Dict Fields:
        Additional key-value pairs defining default model metadata. The specific keys
        depend on the model provider and configuration.
    """

    DEFAULT_MODEL_PARAMS: Optional[dict] = None
    """Default parameters for models.

    Dict Fields:
        Additional key-value pairs defining default model parameters. The specific keys
        depend on the model provider and configuration (e.g., temperature, max_tokens).
    """


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


class TerminalServerConnection(BaseModel):
    """
    Configuration for a single terminal server connection.
    """

    id: Optional[str] = ""
    """Unique identifier for the terminal server connection."""

    name: Optional[str] = ""
    """Display name for the terminal server."""

    enabled: Optional[bool] = True
    """Whether the terminal server connection is enabled."""

    url: str
    """Base URL of the terminal server."""

    path: Optional[str] = "/openapi.json"
    """Path to the OpenAPI spec (default: /openapi.json)."""

    key: Optional[str] = ""
    """API Key or Token for authentication."""

    auth_type: Optional[str] = "bearer"
    """Authentication type. Common values: 'bearer', 'none'."""

    config: Optional[Dict[str, Any]] = None
    """Additional configuration for the connection.

    Dict Fields:
        - `enable` (bool, optional): Whether the terminal server connection is enabled
        - Additional keys may be used for provider-specific settings
    """

    server_type: Optional[str] = None
    """Type of terminal server. 'orchestrator' manages multiple terminals, 'terminal' is a plain terminal server."""

    policy_id: Optional[str] = None
    """ID of the policy assigned to this terminal server from an orchestrator."""

    policy: Optional[Dict[str, Any]] = None
    """Cached policy data fetched from the orchestrator.

    Dict Fields:
        Policy structure is defined by the orchestrator terminal server's API.
        See the orchestrator's /api/v1/policies endpoint for details.
    """

    model_config = ConfigDict(extra="allow")


class TerminalServersConfigForm(BaseModel):
    """
    Configuration for terminal servers.
    """

    TERMINAL_SERVER_CONNECTIONS: List[TerminalServerConnection]
    """List of configured terminal server connections."""


class TerminalServerPolicyForm(BaseModel):
    """
    Form for pushing a policy to an orchestrator terminal server.
    """

    url: str
    """Base URL of the orchestrator terminal server."""

    key: Optional[str] = ""
    """API key or bearer token for authentication."""

    auth_type: Optional[str] = "bearer"
    """Authentication type. Common values: 'bearer', 'none'."""

    policy_id: str
    """ID of the policy to create or update."""

    policy_data: Dict[str, Any]
    """Policy data to send to the orchestrator.

    Dict Fields:
        Policy structure is defined by the orchestrator terminal server's API.
        See the orchestrator's /api/v1/policies endpoint for details.
    """


class TerminalServerLifecycleForm(BaseModel):
    """Form for pushing a session-lifecycle policy to an orchestrator terminal server.

    Open WebUI proxies this verbatim to the orchestrator; only ``bearer`` auth
    is wired into the proxy (any other ``auth_type`` sends no Authorization
    header).
    """

    url: str
    """Base URL of the orchestrator terminal server. Trailing slash is stripped by the backend."""

    key: Optional[str] = ""
    """Bearer token for orchestrator auth. Only applied when auth_type is 'bearer'."""

    auth_type: Optional[str] = "bearer"
    """Auth scheme. Only 'bearer' is honored by the proxy; other values send no auth header."""

    policy_id: str
    """ID of the policy whose lifecycle should be updated on the orchestrator."""

    lifecycle_data: Dict[str, Any]
    """Opaque lifecycle policy body forwarded verbatim to the orchestrator.

    Dict Fields:
        Structure is defined entirely by the orchestrator terminal server's
        ``/api/v1/policies/{policy_id}/lifecycle`` endpoint. The frontend sends
        an arbitrary JSON object (default ``{}``) entered by an admin; Open WebUI
        does not interpret or validate its contents.
    """


class TerminalServerRefreshForm(BaseModel):
    """Form for refreshing or resetting running terminal sessions on an orchestrator.

    Proxied to the orchestrator's ``/api/v1/terminals/refresh`` endpoint.
    ``only_idle`` and ``reset`` are always forwarded; ``user_id`` and
    ``policy_id`` are forwarded only when set, narrowing the targeted sessions.
    Only ``bearer`` auth is wired into the proxy.
    """

    url: str
    """Base URL of the orchestrator terminal server. Trailing slash is stripped by the backend."""

    key: Optional[str] = ""
    """Bearer token for orchestrator auth. Only applied when auth_type is 'bearer'."""

    auth_type: Optional[str] = "bearer"
    """Auth scheme. Only 'bearer' is honored by the proxy; other values send no auth header."""

    user_id: Optional[str] = None
    """Optional user ID. When set, restrict the operation to terminals owned by this user."""

    policy_id: Optional[str] = None
    """Optional policy ID. When set, restrict the operation to terminals under this policy."""

    only_idle: bool = True
    """When True (default), only refresh/reset idle terminal sessions."""

    reset: bool = False
    """When True, reset sessions (tear down and recreate) instead of just refreshing them."""


class SubagentsConfigForm(BaseModel):
    """
    Configuration for the Open WebUI 0.11.0 subagents feature.

    Subagents are auxiliary models spawned to assist with a task. Stored under the
    `subagents.*` config namespace. All fields are required by the backend
    (`POST /v1/configs/subagents` validates the full form).
    """

    ENABLE_SUBAGENTS: bool
    """Master switch for the subagents feature."""

    SUBAGENTS_BACKGROUND_ENABLED: bool
    """Whether subagents run in the background (non-blocking) rather than foreground."""

    SUBAGENTS_MAX_CONCURRENT: int
    """Maximum number of subagents that may run concurrently."""

    SUBAGENTS_MAX_ASYNC: int
    """Maximum number of asynchronous subagent tasks permitted."""

    SUBAGENTS_MAX_ITERATIONS: int
    """Maximum iterations a subagent may perform before stopping."""

    SUBAGENTS_MAX_OUTPUT: int
    """Maximum output (tokens) a subagent may produce."""

    SUBAGENTS_SYSTEM_PROMPT: str
    """System prompt applied to subagents."""
