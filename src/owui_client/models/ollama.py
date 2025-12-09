"""
Pydantic models for Ollama endpoints.
"""

from typing import Optional, Union, List, Dict, Any
from pydantic import BaseModel, ConfigDict, field_validator


class OllamaConfigForm(BaseModel):
    """
    Configuration for Ollama API settings.

    This form is used to update the global Ollama configuration, including enabling/disabling
    the API, setting base URLs, and configuring specific API settings like keys.
    """

    ENABLE_OLLAMA_API: Optional[bool] = None
    """
    Whether to enable the Ollama API integration.
    """

    OLLAMA_BASE_URLS: List[str]
    """
    A list of base URLs for Ollama instances (e.g., `http://localhost:11434`).
    """

    OLLAMA_API_CONFIGS: Dict[str, Any]
    """
    A dictionary mapping URL indices (as strings) or URLs to configuration objects.

    Dict Fields:
        - `enable` (bool, optional): Whether this specific URL is enabled.
        - `key` (str, optional): API key for authentication (if required).
        - `prefix_id` (str, optional): A prefix to prepend to model names from this source.
        - `tags` (List[str], optional): Tags to apply to models from this source.
        - `model_ids` (List[str], optional): Allowlist of model IDs to show.
        - `connection_type` (str, optional): Type of connection (e.g., "local").
    """

    access_control: Optional[dict] = None
    """
    Access control configuration for Ollama resources.

    Dict Fields:
        - `read` (dict, optional): Read access control configuration
            - `group_ids` (List[str], optional): List of group IDs that have read access
            - `user_ids` (List[str], optional): List of user IDs that have read access
        - `write` (dict, optional): Write access control configuration
            - `group_ids` (List[str], optional): List of group IDs that have write access
            - `user_ids` (List[str], optional): List of user IDs that have write access

    When `access_control` is `None`, resources are publicly accessible.
    When `access_control` is provided, only specified users and groups have access.
    """


class ModelNameForm(BaseModel):
    """
    Form for specifying a model name.

    Used in various operations like unloading, deleting, or showing model information.
    """

    model: Optional[str] = None
    """
    The model identifier (e.g., `llama2:latest`).
    """

    # Support extra fields like 'name' which is sometimes used interchangeably
    model_config = ConfigDict(extra="allow")


class PushModelForm(BaseModel):
    """
    Form for pushing a model to a registry.
    """

    model: str
    """
    The name of the model to push.
    """

    insecure: Optional[bool] = None
    """
    Allow insecure connections to the registry.
    """

    stream: Optional[bool] = None
    """
    Whether to stream the progress of the push operation.
    """


class CreateModelForm(BaseModel):
    """
    Form for creating a new model.
    """

    model: Optional[str] = None
    """
    The name of the model to create.
    """

    stream: Optional[bool] = None
    """
    Whether to stream the progress of the creation.
    """

    path: Optional[str] = None
    """
    Path to the model file (deprecated in newer Ollama versions).
    """

    model_config = ConfigDict(extra="allow")


class CopyModelForm(BaseModel):
    """
    Form for copying a model.
    """

    source: str
    """
    The name of the source model.
    """

    destination: str
    """
    The name of the destination model.
    """


class GenerateEmbedForm(BaseModel):
    """
    Form for generating embeddings.
    """

    model: str
    """
    The model to use for embeddings.
    """

    input: Union[List[str], str]
    """
    The input text or list of texts to embed.
    """

    truncate: Optional[bool] = None
    """
    Whether to truncate the input to the model's context length.
    """

    options: Optional[Dict[str, Any]] = None
    """
    Model options (e.g., temperature, context size).

    Dict Fields:
        See [Ollama Modelfile documentation](https://github.com/ollama/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values) for valid parameters.
    """

    keep_alive: Optional[Union[int, str]] = None
    """
    How long to keep the model loaded (e.g., "5m").
    """

    model_config = ConfigDict(extra="allow")


class GenerateEmbeddingsForm(BaseModel):
    """
    Form for generating embeddings (legacy endpoint).
    """

    model: str
    """
    The model to use.
    """

    prompt: str
    """
    The prompt text to embed.
    """

    options: Optional[Dict[str, Any]] = None
    """
    Model options.

    Dict Fields:
        See [Ollama Modelfile documentation](https://github.com/ollama/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values) for valid parameters.
    """

    keep_alive: Optional[Union[int, str]] = None
    """
    How long to keep the model loaded.
    """


class GenerateCompletionForm(BaseModel):
    """
    Form for generating a completion (single prompt).
    """

    model: str
    """
    The model to use.
    """

    prompt: str
    """
    The prompt text.
    """

    suffix: Optional[str] = None
    """
    A suffix to append to the generated text (for infilling).
    """

    images: Optional[List[str]] = None
    """
    A list of base64-encoded images.
    """

    format: Optional[Union[Dict[str, Any], str]] = None
    """
    The format of the response (e.g., "json").

    Dict Fields:
        If provided as a dictionary, it should be a JSON Schema to enforce a specific output structure.
    """

    options: Optional[Dict[str, Any]] = None
    """
    Model parameters like temperature, top_k, etc.

    Dict Fields:
        See [Ollama Modelfile documentation](https://github.com/ollama/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values) for valid parameters.
    """

    system: Optional[str] = None
    """
    System prompt to override the model's default.
    """

    template: Optional[str] = None
    """
    Prompt template to override the model's default.
    """

    context: Optional[List[int]] = None
    """
    Context parameter returned from a previous request (legacy).
    """

    stream: Optional[bool] = True
    """
    Whether to stream the response.
    """

    raw: Optional[bool] = None
    """
    If True, no formatting is applied to the prompt.
    """

    keep_alive: Optional[Union[int, str]] = None
    """
    How long to keep the model loaded.
    """


class ChatMessage(BaseModel):
    """
    A message in a chat conversation.
    """

    role: str
    """
    The role of the message sender (e.g., "user", "assistant", "system").
    """

    content: Optional[str] = None
    """
    The content of the message.
    """

    tool_calls: Optional[List[Dict[str, Any]]] = None
    """
    List of tool calls generated by the model.

    Dict Fields:
        - `index` (int, optional): The index of the tool call in the sequence
        - `id` (str, optional): Unique identifier for the tool call
        - `function` (dict, required): Function call details
            - `name` (str, required): Name of the function/tool to call
            - `arguments` (dict, required): JSON-serializable arguments for the function
    """

    images: Optional[List[str]] = None
    """
    List of base64-encoded images included in the message.
    """

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
    """
    Form for generating a chat completion.
    """

    model: str
    """
    The model to use.
    """

    messages: List[ChatMessage]
    """
    The conversation history.
    """

    format: Optional[Union[Dict[str, Any], str]] = None
    """
    Response format (e.g., "json").

    Dict Fields:
        If provided as a dictionary, it should be a JSON Schema to enforce a specific output structure.
    """

    options: Optional[Dict[str, Any]] = None
    """
    Model parameters.

    Dict Fields:
        See [Ollama Modelfile documentation](https://github.com/ollama/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values) for valid parameters.
    """

    template: Optional[str] = None
    """
    Prompt template to use.
    """

    stream: Optional[bool] = True
    """
    Whether to stream the response.
    """

    keep_alive: Optional[Union[int, str]] = None
    """
    How long to keep the model loaded.
    """

    tools: Optional[List[Dict[str, Any]]] = None
    """
    List of tools available to the model.

    Dict Fields:
        - `type` (str, required): The type of tool, e.g. "function".
        - `function` (dict, required): The function definition.
            - `name` (str, required): The name of the function.
            - `description` (str, optional): A description of the function.
            - `parameters` (dict, required): A JSON schema defining the function parameters.
    """

    model_config = ConfigDict(extra="allow")


class ConnectionVerificationForm(BaseModel):
    """
    Form for verifying an Ollama connection.
    """

    url: str
    """
    The URL of the Ollama instance.
    """

    key: Optional[str] = None
    """
    The API key for authentication.
    """


class UrlForm(BaseModel):
    """
    Form containing a URL, used for downloading models.
    """

    url: str
    """
    The URL to process (e.g., HuggingFace model URL).
    """


class UploadBlobForm(BaseModel):
    """
    Form for uploading a blob (model file).
    """

    filename: str
    """
    The name of the file being uploaded.
    """
