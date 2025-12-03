from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any, Union

# Models for Configs router

class ImportConfigForm(BaseModel):
    config: Dict[str, Any]

class ConnectionsConfigForm(BaseModel):
    ENABLE_DIRECT_CONNECTIONS: bool
    ENABLE_BASE_MODELS_CACHE: bool

class OAuthClientRegistrationForm(BaseModel):
    url: str
    client_id: str
    client_name: Optional[str] = None

class ToolServerConnection(BaseModel):
    url: str
    path: str
    type: Optional[str] = "openapi"  # openapi, mcp
    auth_type: Optional[str] = None
    headers: Optional[Union[Dict[str, Any], str]] = None
    key: Optional[str] = None
    config: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(extra="allow")

class ToolServersConfigForm(BaseModel):
    TOOL_SERVER_CONNECTIONS: List[ToolServerConnection]

class CodeInterpreterConfigForm(BaseModel):
    ENABLE_CODE_EXECUTION: bool
    CODE_EXECUTION_ENGINE: str
    CODE_EXECUTION_JUPYTER_URL: Optional[str] = None
    CODE_EXECUTION_JUPYTER_AUTH: Optional[str] = None
    CODE_EXECUTION_JUPYTER_AUTH_TOKEN: Optional[str] = None
    CODE_EXECUTION_JUPYTER_AUTH_PASSWORD: Optional[str] = None
    CODE_EXECUTION_JUPYTER_TIMEOUT: Optional[int] = None
    ENABLE_CODE_INTERPRETER: bool
    CODE_INTERPRETER_ENGINE: str
    CODE_INTERPRETER_PROMPT_TEMPLATE: Optional[str] = None
    CODE_INTERPRETER_JUPYTER_URL: Optional[str] = None
    CODE_INTERPRETER_JUPYTER_AUTH: Optional[str] = None
    CODE_INTERPRETER_JUPYTER_AUTH_TOKEN: Optional[str] = None
    CODE_INTERPRETER_JUPYTER_AUTH_PASSWORD: Optional[str] = None
    CODE_INTERPRETER_JUPYTER_TIMEOUT: Optional[int] = None

class ModelsConfigForm(BaseModel):
    DEFAULT_MODELS: Optional[str] = None
    DEFAULT_PINNED_MODELS: Optional[str] = None
    MODEL_ORDER_LIST: Optional[List[str]] = None

class PromptSuggestion(BaseModel):
    title: List[str]
    content: str

class SetDefaultSuggestionsForm(BaseModel):
    suggestions: List[PromptSuggestion]

class BannerModel(BaseModel):
    id: str
    type: str
    title: Optional[str] = None
    content: str
    dismissible: bool = True
    timestamp: int

class SetBannersForm(BaseModel):
    banners: List[BannerModel]
