import pytest
from httpx import HTTPStatusError
from owui_client.client import OpenWebUI


@pytest.mark.asyncio
async def test_list_servers(client: OpenWebUI):
    """list_servers returns a list (empty when no servers configured)."""
    result = await client.terminals.list_servers()
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_proxy_server_not_found(client: OpenWebUI):
    """proxy raises 404 when the server_id does not exist."""
    with pytest.raises(HTTPStatusError) as exc_info:
        await client.terminals.proxy("nonexistent-server", "some/path")
    assert exc_info.value.response.status_code == 404
