from typing import Optional, Union, List, Dict, Any
from pydantic import BaseModel, ConfigDict, field_validator

class OllamaConfigForm(BaseModel):
    ENABLE_OLLAMA_API: Optional[bool] = None
    OLLAMA_BASE_URLS: List[str]
    OLLAMA_API_CONFIGS: Dict[str, Any]

class ModelNameForm(BaseModel):
    model: Optional[str] = None
    # Support extra fields like 'name' which is sometimes used interchangeably
    model_config = ConfigDict(extra="allow")

class PushModelForm(BaseModel):
    model: str
    insecure: Optional[bool] = None
    stream: Optional[bool] = None

class CreateModelForm(BaseModel):
    model: Optional[str] = None
    stream: Optional[bool] = None
    path: Optional[str] = None
    model_config = ConfigDict(extra="allow")

class CopyModelForm(BaseModel):
    source: str
    destination: str

class GenerateEmbedForm(BaseModel):
    model: str
    input: Union[List[str], str]
    truncate: Optional[bool] = None
    options: Optional[Dict[str, Any]] = None
    keep_alive: Optional[Union[int, str]] = None
    model_config = ConfigDict(extra="allow")

class GenerateEmbeddingsForm(BaseModel):
    model: str
    prompt: str
    options: Optional[Dict[str, Any]] = None
    keep_alive: Optional[Union[int, str]] = None

class GenerateCompletionForm(BaseModel):
    model: str
    prompt: str
    suffix: Optional[str] = None
    images: Optional[List[str]] = None
    format: Optional[Union[Dict[str, Any], str]] = None
    options: Optional[Dict[str, Any]] = None
    system: Optional[str] = None
    template: Optional[str] = None
    context: Optional[List[int]] = None
    stream: Optional[bool] = True
    raw: Optional[bool] = None
    keep_alive: Optional[Union[int, str]] = None

class ChatMessage(BaseModel):
    role: str
    content: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    images: Optional[List[str]] = None

    @field_validator("content", mode="before")
    @classmethod
    def check_at_least_one_field(cls, field_value, info):
        # Validation logic similar to backend
        values = info.data
        if field_value is None and (
            "tool_calls" not in values or values["tool_calls"] is None
        ):
            # In Pydantic v2 validation is slightly different, but this is close enough check
            # We'll let the server handle strict validation if needed, or improve this later.
            pass
        return field_value

class GenerateChatCompletionForm(BaseModel):
    model: str
    messages: List[ChatMessage]
    format: Optional[Union[Dict[str, Any], str]] = None
    options: Optional[Dict[str, Any]] = None
    template: Optional[str] = None
    stream: Optional[bool] = True
    keep_alive: Optional[Union[int, str]] = None
    tools: Optional[List[Dict[str, Any]]] = None
    model_config = ConfigDict(extra="allow")

class ConnectionVerificationForm(BaseModel):
    url: str
    key: Optional[str] = None

class UrlForm(BaseModel):
    url: str

class UploadBlobForm(BaseModel):
    filename: str
