from owui_client.client_base import ResourceBase
from owui_client.models.openai import OpenAIConfigForm, ConnectionVerificationForm
from urllib.parse import urljoin
from typing import Optional


class OpenAIClient(ResourceBase):
    """
    Client for the OpenAI-compatible endpoints.

    This resource handles configuration of OpenAI providers, as well as proxying
    requests for chat completions, embeddings, and speech generation to the configured providers.
    """

    def _get_url(self, path: str) -> str:
        # OpenAI router is mounted at root /openai, not /api/openai
        # We need to construct the URL relative to the root, not base_url (which includes /api)
        base = str(self._client._client.base_url)
        if base.endswith("/api/"):
            base = base[:-5]
        elif base.endswith("/api"):
            base = base[:-4]

        if not base.endswith("/"):
            base += "/"

        if path.startswith("/"):
            path = path[1:]

        return urljoin(base, path)

    async def get_config(self) -> dict:
        """
        Get the current OpenAI API configuration.

        Returns:
            dict: Configuration object containing `ENABLE_OPENAI_API`, `OPENAI_API_BASE_URLS`, `OPENAI_API_KEYS`, and `OPENAI_API_CONFIGS`.
        """
        # Use full URL to bypass base_url path
        return await self._request("GET", self._get_url("openai/config"))

    async def update_config(self, form_data: OpenAIConfigForm) -> dict:
        """
        Update the OpenAI API configuration.

        Args:
            form_data (OpenAIConfigForm): The new configuration.

        Returns:
            dict: The updated configuration object.
        """
        return await self._request(
            "POST", self._get_url("openai/config/update"), json=form_data.model_dump()
        )

    async def get_models(self, url_idx: Optional[int] = None) -> dict:
        """
        Get available OpenAI models.

        Args:
            url_idx (Optional[int]): The index of the specific provider to fetch models from.
                If None, fetches and merges models from all enabled providers.

        Returns:
            dict: A dictionary containing a `data` key with a list of model objects.
        """
        path = "openai/models"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request("GET", self._get_url(path))

    async def verify_connection(self, form_data: ConnectionVerificationForm) -> dict:
        """
        Verify connectivity to a specific OpenAI-compatible provider.

        Args:
            form_data (ConnectionVerificationForm): The connection details to verify.

        Returns:
            dict: The response from the provider (typically the models list) if successful.
        """
        return await self._request(
            "POST", self._get_url("openai/verify"), json=form_data.model_dump()
        )

    async def speech(self, payload: dict) -> bytes:
        """
        Generate speech from text (TTS).

        Args:
            payload (dict): OpenAI-compatible speech payload (e.g. `{"model": "tts-1", "input": "Hello", "voice": "alloy"}`).

        Returns:
            bytes: The audio file content (MP3).
        """
        # Returns MP3 file bytes
        return await self._request(
            "POST", self._get_url("openai/audio/speech"), json=payload, model=bytes
        )

    async def chat_completions(self, payload: dict) -> dict:
        """
        Generate a chat completion.

        Proxies the request to the appropriate OpenAI-compatible provider based on the model ID.

        Args:
            payload (dict): OpenAI-compatible chat completion payload (e.g. `{"model": "gpt-3.5-turbo", "messages": [...]}`).

        Returns:
            dict: The chat completion response object.
        """
        return await self._request(
            "POST", self._get_url("openai/chat/completions"), json=payload
        )

    async def embeddings(self, payload: dict) -> dict:
        """
        Generate embeddings for the input text.

        Args:
            payload (dict): OpenAI-compatible embeddings payload (e.g. `{"model": "text-embedding-3-small", "input": "text"}`).

        Returns:
            dict: The embeddings response object.
        """
        return await self._request(
            "POST", self._get_url("openai/embeddings"), json=payload
        )

    async def proxy(self, method: str, path: str, payload: Optional[dict] = None) -> dict:
        """
        Deprecated: Proxy arbitrary requests to the first OpenAI provider.

        This endpoint is deprecated and may not work as expected with multiple providers.

        Args:
            method (str): HTTP method (e.g. "GET", "POST").
            path (str): The path to append to the base URL (e.g. "models").
            payload (Optional[dict]): JSON payload for the request.

        Returns:
            dict: The JSON response from the provider.
        """
        return await self._request(
            method, self._get_url(f"openai/{path}"), json=payload
        )
