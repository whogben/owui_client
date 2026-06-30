"""Direct unit tests for low-level response handling in `client_base`.

These do not require the Open WebUI server (they mock the httpx client and
exercise the pure transform logic in `_request`).
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from owui_client.client_base import OWUIClientBase


def _base_with_mock_response(payload):
    """Build an OWUIClientBase whose httpx client returns `payload` as JSON."""
    base = OWUIClientBase()
    fake_response = MagicMock()
    fake_response.json.return_value = payload
    fake_response.raise_for_status = MagicMock()
    http = MagicMock()
    http.request = AsyncMock(return_value=fake_response)
    # Inject into the name-mangled lazy-client slot the `_client` property reads.
    base._OWUIClientBase__client = http
    return base


@pytest.mark.asyncio
async def test_request_list_of_dicts_is_preserved():
    """Regression guard for `get_pending_knowledge_files` (and any `list[dict]` endpoint).

    `model=list[dict]` must round-trip a list of dicts unchanged. The earlier
    `model=list` (bare) form corrupted list-of-dicts payloads into lists of
    dict keys, because `_request` only special-cases parameterized list types
    (`get_origin(list[dict]) is list`) and otherwise delegates the whole list to
    `_process_model_item`, which does `[list(item) for item in data]`.
    """
    payload = [{"id": "a", "content": "x"}, {"id": "b", "content": "y"}]
    base = _base_with_mock_response(payload)

    result = await base._request("GET", "/anything", model=list[dict])

    assert result == payload
    assert all(isinstance(item, dict) for item in result)


@pytest.mark.asyncio
async def test_request_list_of_dicts_empty():
    """An empty result list stays an empty list (no corruption / no error)."""
    base = _base_with_mock_response([])
    assert await base._request("GET", "/anything", model=list[dict]) == []
