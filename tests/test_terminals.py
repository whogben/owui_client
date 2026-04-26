import pytest
from httpx import HTTPStatusError

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio


async def test_list_terminals_empty(client):
    """
    Test listing terminal servers when none are configured.

    In a fresh test environment, no terminal servers are configured,
    so the endpoint should return an empty list.
    """
    terminals = await client.terminals.list_terminals()
    assert terminals == []


async def test_proxy_terminal_server_not_found(client):
    """
    Test proxying to a non-existent terminal server returns 404.

    When no terminal server with the given ID exists, the endpoint
    should raise an HTTPStatusError with status code 404.
    """
    with pytest.raises(HTTPStatusError) as excinfo:
        await client.terminals.proxy(
            server_id="nonexistent-server",
            path="api/terminals/test-session",
            method="GET",
        )
    assert excinfo.value.response.status_code == 404
