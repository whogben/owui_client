"""Client for the Terminals endpoints.

This module provides access to the terminal server reverse proxy endpoints,
including listing available terminal servers and proxying requests to them.
"""

from typing import Any, Dict, List, Optional

from owui_client.client_base import ResourceBase
from owui_client.models.terminals import TerminalServer


class TerminalsClient(ResourceBase):
    """Client for the Terminals endpoints."""

    async def list_terminals(self) -> List[TerminalServer]:
        """Return terminal servers the authenticated user has access to.

        Returns:
            List of `TerminalServer` objects containing `id`, `url`, and `name`
            for each enabled terminal server the user is authorized to use.
        """
        return await self._request(
            "GET",
            "/v1/terminals/",
            model=List[TerminalServer],
        )

    async def proxy(
        self,
        server_id: str,
        path: str,
        method: str = "GET",
        data: Any = None,
        json: Any = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Proxy a request to the admin terminal server identified by *server_id*.

        This method forwards an arbitrary HTTP request to a configured terminal
        server through the Open WebUI reverse proxy. The caller is responsible
        for providing a valid *path* relative to the terminal server's base URL.

        Args:
            server_id: The unique identifier of the target terminal server.
            path: The path to proxy (e.g. ``"api/terminals/session-id"``).
                Leading slashes are stripped automatically.
            method: HTTP method to use (default: ``"GET"``).
            data: Raw request body data.
            json: JSON-serializable request body.
            params: Query parameters to append to the proxied URL.
            headers: Additional headers to forward with the request.

        Returns:
            The upstream response body. JSON responses are parsed automatically;
            non-JSON responses are returned as text.

        Raises:
            HTTPStatusError: If the terminal server is not found (404),
                access is denied (403), or the upstream returns an error.
        """
        safe_path = path.lstrip("/")
        return await self._request(
            method,
            f"/v1/terminals/{server_id}/{safe_path}",
            data=data,
            json=json,
            params=params,
            headers=headers,
        )
