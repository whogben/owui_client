"""Client for the Terminals endpoints.

Reverse proxy for admin-configured terminal servers. Provides access to
terminal server listings and HTTP proxy forwarding.

The WebSocket proxy endpoint (``/{server_id}/api/terminals/{session_id}``)
is not supported by this HTTP client — WebSocket connections cannot be
wrapped by httpx.
"""

from typing import Any, Optional

from owui_client.client_base import ResourceBase


class TerminalsClient(ResourceBase):
    """
    Client for the Terminals endpoints.

    Terminals is a reverse-proxy feature that forwards HTTP requests to
    admin-configured terminal servers. Only the HTTP endpoints are
    implemented; the interactive WebSocket proxy is not supported.
    """

    async def list_servers(self) -> list[dict[str, Any]]:
        """List terminal servers the authenticated user has access to.

        Returns only servers that are enabled and for which the user's
        group membership grants access. Each entry contains ``id``,
        ``url``, and ``name``.

        Returns:
            List of terminal server dicts, each with keys ``id``, ``url``,
            ``name``.
        """
        return await self._request("GET", "/v1/terminals/")

    async def proxy(
        self,
        server_id: str,
        path: str,
        method: str = "GET",
        json: Optional[Any] = None,
        data: Optional[Any] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> Any:
        """Proxy a request to a terminal server.

        Forwards an HTTP request through the Open WebUI backend to the
        terminal server identified by *server_id*. The backend handles
        authentication, path sanitization, and access control.

        Args:
            server_id: ID of the terminal server to proxy to.
            path: URL path to append after the server base URL.
            method: HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD,
                OPTIONS). Defaults to ``"GET"``.
            json: JSON body to forward with the request.
            data: Form or raw body to forward with the request.
            params: Query parameters to forward with the request.

        Returns:
            The proxied response from the terminal server. May be a dict,
            list, bytes, or other type depending on the upstream response.

        Raises:
            HTTPStatusError: If the backend returns 403 (access denied),
                404 (server not found), 400 (invalid path), 502 (proxy
                error), or 503 (server URL not configured).
        """
        kwargs: dict[str, Any] = {}
        if json is not None:
            kwargs["json"] = json
        if data is not None:
            kwargs["data"] = data
        if params is not None:
            kwargs["params"] = params

        return await self._request(
            method,
            f"/v1/terminals/{server_id}/{path}",
            **kwargs,
        )
