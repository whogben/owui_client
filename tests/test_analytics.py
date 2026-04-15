"""Tests for the Analytics endpoints."""

import pytest
import time

pytestmark = pytest.mark.asyncio


async def test_get_model_analytics(client):
    """Test retrieving message counts per model."""
    result = await client.analytics.get_model_analytics()
    assert result is not None


async def test_get_user_analytics(client):
    """Test retrieving message counts and token usage per user."""
    result = await client.analytics.get_user_analytics()
    assert result is not None


async def test_get_messages(client):
    """Test querying messages with filters."""
    result = await client.analytics.get_messages()
    assert result is not None
    assert isinstance(result, list)


async def test_get_summary(client):
    """Test retrieving dashboard summary statistics."""
    result = await client.analytics.get_summary()
    assert result is not None


async def test_get_daily_stats(client):
    """Test retrieving daily message counts for time-series charts."""
    result = await client.analytics.get_daily_stats()
    assert result is not None


async def test_get_token_usage(client):
    """Test retrieving token usage aggregated by model."""
    result = await client.analytics.get_token_usage()
    assert result is not None


async def test_get_model_chats(client):
    """Test retrieving chats that used a specific model."""
    result = await client.analytics.get_model_chats(model_id="test-model")
    assert result is not None


async def test_get_model_overview(client):
    """Test retrieving model overview with feedback history and chat tags."""
    result = await client.analytics.get_model_overview(model_id="test-model")
    assert result is not None
