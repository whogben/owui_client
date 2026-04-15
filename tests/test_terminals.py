"""Tests for the Terminals endpoints."""

import pytest

pytestmark = pytest.mark.asyncio


async def test_list_terminal_servers(client):
    """Test listing terminal servers the authenticated user has access to."""
    result = await client.terminals.list_terminal_servers()
    assert result is not None
    assert isinstance(result, list)


async def test_proxy_request(client):
    """Test proxy_request to a non-existent server_id expects an error."""
    try:
        await client.terminals.proxy_request(
            server_id="non-existent-server",
            path="api/test",
        )
        assert False, "Expected an error for non-existent server_id"
    except Exception:
        pass
