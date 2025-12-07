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
    
    Keys are string string indices (e.g. "0", "1") corresponding to the index in `OPENAI_API_BASE_URLS`.
    Values are dictionaries containing settings like:
    - `enable` (bool): Whether this specific provider is enabled.
    - `model_ids` (List[str]): List of specific model IDs to expose (if empty, all are fetched).
    - `prefix_id` (str): Prefix to add to model IDs from this provider.
    - `connection_type` (str): e.g. "external".
    - `azure` (bool): Whether this is an Azure OpenAI endpoint.
    - `api_version` (str): API version for Azure.
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
    
    Can include keys like `azure` (bool), `auth_type` (str), `api_version` (str), etc.
    """
