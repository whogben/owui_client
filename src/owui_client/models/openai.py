from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, ConfigDict


class ResponsesForm(BaseModel):
    """
    Request form for the OpenAI Responses API.

    The Responses API is an alternative to Chat Completions that uses a simpler input format
    and supports multi-turn conversations with stored response IDs. This model uses
    `extra="allow"` to pass through any additional OpenAI API parameters.
    """

    model: str
    """The model ID to use (e.g., "gpt-4o", "o1")."""

    input: Optional[Union[list, str]] = None
    """Input for the response generation.

    Can be a string (treated as a single user message) or a list of input items.
    Each input item can be a message object with `type: "message"`, `role`, and `content` fields,
    or output items from previous responses for multi-turn conversations.
    """

    instructions: Optional[str] = None
    """System instructions for the model, similar to the system message in Chat Completions."""

    stream: Optional[bool] = None
    """Whether to stream the response as SSE events."""

    temperature: Optional[float] = None
    """Sampling temperature between 0.0 and 2.0."""

    max_output_tokens: Optional[int] = None
    """Maximum number of tokens to generate in the output."""

    top_p: Optional[float] = None
    """Nucleus sampling parameter between 0.0 and 1.0."""

    tools: Optional[list] = None
    """List of tools available to the model.

    Uses Responses API format: `{"type": "function", "name": "...", "parameters": {...}}`.
    """

    tool_choice: Optional[Union[str, dict]] = None
    """Controls which tool is called. Can be "auto", "none", "required", or a dict.

    Dict Fields:
        - `type` (str, required): Must be "function"
        - `function` (dict, required): Function specification
            - `name` (str, required): Name of the function to call

    String Values:
        - "auto": Model decides whether to call a tool
        - "none": Model will not call any tool
        - "required": Model must call at least one tool
    """

    text: Optional[dict] = None
    """Text response format configuration.

    Dict Fields:
        - `format` (dict, optional): Response format settings, e.g., `{"type": "json_object"}`.
    """

    truncation: Optional[str] = None
    """Truncation strategy for the response. Valid values: "auto", "disabled"."""

    metadata: Optional[dict] = None
    """Metadata to attach to the response.

    Dict Fields:
        Arbitrary key-value pairs for tracking. Keys must be strings, values
        can be strings, numbers, or nested objects. Maximum 16 key-value pairs.
        Commonly used for storing user IDs, session IDs, or other identifiers.
    """

    store: Optional[bool] = None
    """Whether to store the response for later retrieval."""

    reasoning: Optional[dict] = None
    """Reasoning effort configuration for o-series models.

    Dict Fields:
        - `effort` (str, optional): Reasoning effort level. Valid values: "low", "medium", "high".
    """

    previous_response_id: Optional[str] = None
    """ID of a previous response to continue the conversation."""

    model_config = ConfigDict(extra="allow")


class OpenAIConfigForm(BaseModel):
    """
    Configuration form for OpenAI API settings.

    Used to update the global OpenAI configuration, including enabling the API, setting base URLs and keys, and configuring specific provider settings.
    """

    ENABLE_OPENAI_API: Optional[bool] = None
    """
    Whether to enable the OpenAI API integration.
    """

    OPENAI_API_BASE_URLS: List[str]
    """
    List of base URLs for OpenAI-compatible providers (e.g. `https://api.openai.com/v1`, `http://localhost:11434/v1`).
    """

    OPENAI_API_KEYS: List[str]
    """
    List of API keys corresponding to the base URLs.
    
    The order must match `OPENAI_API_BASE_URLS`. If the length does not match, the backend may pad or truncate this list.
    """

    OPENAI_API_CONFIGS: Dict[str, Any]
    """
    Configuration dictionary for each provider.

    Keys are string indices (e.g. "0", "1") corresponding to the index in `OPENAI_API_BASE_URLS`.
    Values are dictionaries containing provider-specific configuration.

    Dict Fields:
        - `enable` (bool, optional): Whether this specific provider is enabled. Defaults to True.
        - `model_ids` (List[str], optional): List of specific model IDs to expose. If empty, all models are fetched from the provider.
        - `prefix_id` (str, optional): Prefix to add to model IDs from this provider to avoid naming conflicts.
        - `connection_type` (str, optional): Type of connection, typically "external" or "local".
        - `azure` (bool, optional): Whether this is an Azure OpenAI endpoint.
        - `api_version` (str, optional): API version for Azure OpenAI endpoints (e.g., "2023-03-15-preview").
        - `auth_type` (str, optional): Authentication type. Valid values: "bearer", "session", "system_oauth", "azure_ad", "microsoft_entra_id", "none".
        - `headers` (dict, optional): Additional HTTP headers as JSON object for custom authentication or request modifications.
        - `tags` (List[str], optional): Tags for categorization and filtering of models.
    """


class ConnectionVerificationForm(BaseModel):
    """
    Form for verifying connectivity to an OpenAI-compatible provider.
    """

    url: str
    """
    The base URL of the provider to verify (e.g. `https://api.openai.com/v1`).
    """

    key: str
    """
    The API key to use for verification.
    """

    config: Optional[dict] = None
    """
    Optional configuration overrides for the verification request.

    Dict Fields:
        - `azure` (bool, optional): Whether this is an Azure OpenAI endpoint.
        - `auth_type` (str, optional): Authentication type. Valid values: "bearer", "session", "system_oauth", "azure_ad", "microsoft_entra_id", "none".
        - `api_version` (str, optional): API version for Azure OpenAI endpoints (e.g., "2023-03-15-preview").
        - `headers` (dict, optional): Additional HTTP headers as JSON object for custom authentication or request modifications.
    """
