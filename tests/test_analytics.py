import pytest
from owui_client.client import OpenWebUI


@pytest.mark.asyncio
async def test_get_model_analytics(client: OpenWebUI):
    result = await client.analytics.get_model_analytics()
    assert result is not None
    assert hasattr(result, "models")
    assert isinstance(result.models, list)


@pytest.mark.asyncio
async def test_get_model_analytics_with_date_range(client: OpenWebUI):
    result = await client.analytics.get_model_analytics(
        start_date=1700000000, end_date=1800000000
    )
    assert result is not None
    assert isinstance(result.models, list)


@pytest.mark.asyncio
async def test_get_user_analytics(client: OpenWebUI):
    result = await client.analytics.get_user_analytics()
    assert result is not None
    assert hasattr(result, "users")
    assert isinstance(result.users, list)


@pytest.mark.asyncio
async def test_get_user_analytics_with_limit(client: OpenWebUI):
    result = await client.analytics.get_user_analytics(limit=10)
    assert result is not None
    assert isinstance(result.users, list)


@pytest.mark.asyncio
async def test_get_messages_empty(client: OpenWebUI):
    result = await client.analytics.get_messages()
    assert result is not None
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_get_messages_with_model_filter(client: OpenWebUI):
    result = await client.analytics.get_messages(model_id="gpt-4o")
    assert result is not None
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_get_summary(client: OpenWebUI):
    result = await client.analytics.get_summary()
    assert result is not None
    assert hasattr(result, "total_messages")
    assert hasattr(result, "total_chats")
    assert hasattr(result, "total_models")
    assert hasattr(result, "total_users")
    assert isinstance(result.total_messages, int)
    assert isinstance(result.total_chats, int)
    assert isinstance(result.total_models, int)
    assert isinstance(result.total_users, int)


@pytest.mark.asyncio
async def test_get_daily_stats(client: OpenWebUI):
    result = await client.analytics.get_daily_stats()
    assert result is not None
    assert hasattr(result, "data")
    assert isinstance(result.data, list)


@pytest.mark.asyncio
async def test_get_daily_stats_hourly(client: OpenWebUI):
    result = await client.analytics.get_daily_stats(granularity="hourly")
    assert result is not None
    assert isinstance(result.data, list)


@pytest.mark.asyncio
async def test_get_token_usage(client: OpenWebUI):
    result = await client.analytics.get_token_usage()
    assert result is not None
    assert hasattr(result, "models")
    assert hasattr(result, "total_input_tokens")
    assert hasattr(result, "total_output_tokens")
    assert hasattr(result, "total_tokens")
    assert isinstance(result.models, list)
    assert isinstance(result.total_tokens, int)


@pytest.mark.asyncio
async def test_get_model_chats(client: OpenWebUI):
    result = await client.analytics.get_model_chats(model_id="gpt-4o")
    assert result is not None
    assert hasattr(result, "chats")
    assert hasattr(result, "total")
    assert isinstance(result.chats, list)
    assert isinstance(result.total, int)


@pytest.mark.asyncio
async def test_get_model_chats_with_pagination(client: OpenWebUI):
    result = await client.analytics.get_model_chats(
        model_id="gpt-4o", skip=0, limit=10
    )
    assert result is not None
    assert isinstance(result.chats, list)


@pytest.mark.asyncio
async def test_get_model_overview(client: OpenWebUI):
    result = await client.analytics.get_model_overview(model_id="gpt-4o")
    assert result is not None
    assert hasattr(result, "history")
    assert hasattr(result, "tags")
    assert isinstance(result.history, list)
    assert isinstance(result.tags, list)


@pytest.mark.asyncio
async def test_get_model_overview_all_time(client: OpenWebUI):
    result = await client.analytics.get_model_overview(model_id="gpt-4o", days=0)
    assert result is not None
    assert isinstance(result.history, list)
    assert isinstance(result.tags, list)
