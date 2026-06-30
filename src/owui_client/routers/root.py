"""
Client for root/main endpoints.
"""

from typing import Dict, Any
from owui_client.client_base import ResourceBase


class RootClient(ResourceBase):
    """
    Client for root/main endpoints (version, config, models, chat, etc.).

    Note: the legacy per-instance `/api/webhook` URL endpoints were removed in
    Open WebUI 0.10.0 in favor of the full event webhooks system; see
    `OpenWebUI.events` (`EventsClient`).
    """
    async def get_version(self) -> Dict[str, Any]:
        """
        Get the application version and deployment ID.

        Returns:
            A dictionary containing:
            - `version`: The current application version.
            - `deployment_id`: The deployment ID.
        """
        return await self._request("GET", "/version", model=dict)

    async def get_changelog(self) -> Dict[str, Any]:
        """
        Get the application changelog.

        Returns:
            A dictionary containing the latest 5 changelog entries.
        """
        return await self._request("GET", "/changelog", model=dict)

    async def health(self) -> Dict[str, bool]:
        """
        Check the health of the application.

        Returns:
            A dictionary with the health status: `{"status": True}`.
        """
        # /health is at the root, not under /api
        # Use relative path "../health" to go up from /api base
        return await self._request("GET", "../health", model=dict)

    async def get_config(self) -> Dict[str, Any]:
        """
        Get the application configuration.

        Returns:
            A dictionary containing configuration details such as:
            - `status`: Application status.
            - `name`: WebUI name.
            - `version`: Application version.
            - `oauth`: OAuth providers configuration.
            - `features`: Enabled features (auth, signup, etc.).
            - `default_models`: Default models configuration (if authenticated).
        """
        return await self._request("GET", "/config", model=dict)

    async def get_models(self) -> Dict[str, Any]:
        """
        Get available models (unified list).

        Returns:
            A dictionary with a `data` key containing a list of available models.
        """
        return await self._request("GET", "/models", model=dict)

    async def chat_completions(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate chat completions (unified endpoint).

        Args:
            form_data: A dictionary containing the chat completion parameters.
                       This typically includes `model`, `messages`, and optional fields
                       like `chat_id`, `stream`, `files`, `features`, etc.

        Returns:
            A dictionary containing the chat completion response.
        """
        return await self._request(
            "POST", "/chat/completions", model=dict, json=form_data
        )

    async def embeddings(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate embeddings (unified endpoint).

        Args:
            form_data: A dictionary containing the embeddings parameters.
                       This typically includes `model` and `input`.

        Returns:
            A dictionary containing the embeddings response.
        """
        return await self._request("POST", "/embeddings", model=dict, json=form_data)
