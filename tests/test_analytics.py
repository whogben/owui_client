import pytest

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio


async def test_get_summary(client):
    """
    Test getting analytics summary as admin.

    Verifies that the summary endpoint returns valid statistics.
    With a fresh test server, counts may be zero.
    """
    summary = await client.analytics.get_summary()

    assert summary is not None
    assert isinstance(summary.total_messages, int)
    assert isinstance(summary.total_chats, int)
    assert isinstance(summary.total_models, int)
    assert isinstance(summary.total_users, int)


async def test_get_model_analytics(client):
    """
    Test getting model analytics as admin.

    Verifies that the model analytics endpoint returns a valid response.
    """
    analytics = await client.analytics.get_model_analytics()

    assert analytics is not None
    assert isinstance(analytics.models, list)


async def test_get_user_analytics(client):
    """
    Test getting user analytics as admin.

    Verifies that the user analytics endpoint returns a valid response.
    """
    analytics = await client.analytics.get_user_analytics()

    assert analytics is not None
    assert isinstance(analytics.users, list)


async def test_get_messages_no_filter(client):
    """
    Test querying messages without filters returns an empty list.

    The backend returns an empty list when no filter is specified.
    """
    messages = await client.analytics.get_messages()

    assert messages is not None
    assert messages == []


async def test_get_daily_stats(client):
    """
    Test getting daily stats as admin.

    Verifies that the daily stats endpoint returns a valid response.
    """
    stats = await client.analytics.get_daily_stats()

    assert stats is not None
    assert isinstance(stats.data, list)


async def test_get_token_usage(client):
    """
    Test getting token usage as admin.

    Verifies that the token usage endpoint returns a valid response.
    """
    usage = await client.analytics.get_token_usage()

    assert usage is not None
    assert isinstance(usage.models, list)
    assert isinstance(usage.total_input_tokens, int)
    assert isinstance(usage.total_output_tokens, int)
    assert isinstance(usage.total_tokens, int)


async def test_get_model_chats_not_found(client):
    """
    Test getting chats for a non-existent model.

    Should return an empty chats list with total=0.
    """
    result = await client.analytics.get_model_chats("nonexistent-model")

    assert result is not None
    assert result.chats == []
    assert result.total == 0


async def test_get_model_overview_not_found(client):
    """
    Test getting overview for a non-existent model.

    Should return empty history and tags.
    """
    overview = await client.analytics.get_model_overview("nonexistent-model")

    assert overview is not None
    assert isinstance(overview.history, list)
    assert isinstance(overview.tags, list)
