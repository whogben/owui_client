from typing import Dict, Any
from owui_client.client_base import ResourceBase
from owui_client.models.root import UrlForm


class RootClient(ResourceBase):
    async def get_version(self) -> Dict[str, Any]:
        """
        Get the application version.
        """
        return await self._request("GET", "/version", model=dict)

    async def get_changelog(self) -> Dict[str, Any]:
        """
        Get the application changelog.
        """
        return await self._request("GET", "/changelog", model=dict)

    async def health(self) -> Dict[str, bool]:
        """
        Check the health of the application.
        """
        # /health is at the root, not under /api
        # Use relative path "../health" to go up from /api base
        return await self._request("GET", "../health", model=dict)

    async def get_config(self) -> Dict[str, Any]:
        """
        Get the application configuration.
        """
        return await self._request("GET", "/config", model=dict)

    async def get_webhook_url(self) -> Dict[str, str]:
        """
        Get the configured webhook URL.
        """
        return await self._request("GET", "/webhook", model=dict)

    async def update_webhook_url(self, url: str) -> Dict[str, str]:
        """
        Update the webhook URL.
        """
        return await self._request(
            "POST",
            "/webhook",
            model=dict,
            json=UrlForm(url=url).model_dump(),
        )

    async def get_models(self) -> Dict[str, Any]:
        """
        Get available models (unified list).
        """
        return await self._request("GET", "/models", model=dict)

    async def chat_completions(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate chat completions (unified endpoint).
        """
        return await self._request(
            "POST", "/chat/completions", model=dict, json=form_data
        )

    async def embeddings(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate embeddings (unified endpoint).
        """
        return await self._request("POST", "/embeddings", model=dict, json=form_data)
