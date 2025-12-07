from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any, Union

# Models for Configs router

class ImportConfigForm(BaseModel):
    """
    Form for importing system configuration.
    """
    config: Dict[str, Any]
    """The configuration dictionary to import. This should match the structure returned by the export endpoint."""

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
    """Custom headers to send with requests."""
    
    key: Optional[str] = None
    """API Key or Token for bearer auth."""
    
    config: Optional[Dict[str, Any]] = None
    """Additional configuration for the connection."""
    
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
