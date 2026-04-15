"""Tests for the Terminals endpoints."""

import pytest

pytestmark = pytest.mark.asyncio


async def test_list_terminal_servers(client):
    """Test listing terminal servers the authenticated user has access to."""
    result = await client.terminals.list_terminal_servers()
    assert result is not None
    assert isinstance(result, list)
