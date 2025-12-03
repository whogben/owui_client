from owui_client.client_base import ResourceBase
from owui_client.models.openai import OpenAIConfigForm, ConnectionVerificationForm
from urllib.parse import urljoin
from typing import Optional


class OpenAIClient(ResourceBase):
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
        # Use full URL to bypass base_url path
        return await self._request("GET", self._get_url("openai/config"))

    async def update_config(self, form_data: OpenAIConfigForm) -> dict:
        return await self._request(
            "POST", self._get_url("openai/config/update"), json=form_data.model_dump()
        )

    async def get_models(self, url_idx: Optional[int] = None) -> dict:
        path = "openai/models"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request("GET", self._get_url(path))

    async def verify_connection(self, form_data: ConnectionVerificationForm) -> dict:
        return await self._request(
            "POST", self._get_url("openai/verify"), json=form_data.model_dump()
        )

    async def speech(self, payload: dict) -> bytes:
        # Returns MP3 file bytes
        return await self._request(
            "POST", self._get_url("openai/audio/speech"), json=payload, model=bytes
        )

    async def chat_completions(self, payload: dict) -> dict:
        return await self._request(
            "POST", self._get_url("openai/chat/completions"), json=payload
        )

    async def embeddings(self, payload: dict) -> dict:
        return await self._request(
            "POST", self._get_url("openai/embeddings"), json=payload
        )

    async def proxy(self, method: str, path: str, payload: Optional[dict] = None) -> dict:
        """
        Deprecated: proxy all requests to OpenAI API.
        """
        return await self._request(
            method, self._get_url(f"openai/{path}"), json=payload
        )
