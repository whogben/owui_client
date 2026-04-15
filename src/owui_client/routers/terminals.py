"""Client for the Terminals endpoints.

Provides access to admin-configured terminal servers and acts as a reverse proxy.

Note: The WebSocket endpoint (`/{server_id}/api/terminals/{session_id}`) is not
available through this HTTP client. Use a WebSocket-capable library directly.
"""

from typing import Any
from owui_client.client_base import ResourceBase


class TerminalsClient(ResourceBase):
    """Client for the Terminals endpoints."""

    async def list_terminal_servers(self) -> list[dict[str, str]]:
        """List terminal servers the authenticated user has access to.

        Returns:
            list[dict]: Each dict contains 'id', 'url', and 'name' keys.
        """
        return await self._request("GET", "/v1/terminals/")

    async def proxy_request(
        self,
        server_id: str,
        path: str,
        method: str = "GET",
        **kwargs: Any,
    ) -> Any:
        """Proxy a request to the specified terminal server.

        This forwards the request to the admin-configured terminal server
        identified by server_id, appending the given path.

        Args:
            server_id: The terminal server ID.
            path: The path to forward to the terminal server.
            method: HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS).
            **kwargs: Additional keyword arguments passed to the underlying HTTP request.
        """
        return await self._request(
            method, f"/v1/terminals/{server_id}/{path}", **kwargs
        )
