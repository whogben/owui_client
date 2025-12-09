from typing import Optional, List, Dict, Any
from pydantic import BaseModel


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
