"""Client for the Analytics endpoints."""

from typing import Any, Optional
from owui_client.client_base import ResourceBase
from owui_client.models.analytics import (
    ModelAnalyticsResponse,
    UserAnalyticsResponse,
    SummaryResponse,
    DailyStatsResponse,
    TokenUsageResponse,
    ModelChatsResponse,
    ModelOverviewResponse,
)


class AnalyticsClient(ResourceBase):
    """
    Client for the Analytics endpoints.

    All endpoints require admin privileges. Analytics provides read-only
    dashboards for message counts, token usage, user activity, and model
    performance.
    """

    async def get_model_analytics(
        self,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        group_id: Optional[str] = None,
    ) -> ModelAnalyticsResponse:
        """Get message counts per model, sorted by count descending.

        Args:
            start_date: Start timestamp (epoch seconds) to filter messages.
            end_date: End timestamp (epoch seconds) to filter messages.
            group_id: Filter to users in this group.

        Returns:
            `ModelAnalyticsResponse` with models list sorted by count descending.
        """
        params: dict[str, Any] = {}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if group_id is not None:
            params["group_id"] = group_id
        return await self._request(
            "GET",
            "/v1/analytics/models",
            model=ModelAnalyticsResponse,
            params=params,
        )

    async def get_user_analytics(
        self,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        group_id: Optional[str] = None,
        limit: int = 50,
    ) -> UserAnalyticsResponse:
        """Get message counts and token usage per user, sorted by count descending.

        Args:
            start_date: Start timestamp (epoch seconds) to filter messages.
            end_date: End timestamp (epoch seconds) to filter messages.
            group_id: Filter to users in this group.
            limit: Maximum number of users to return. Defaults to 50.

        Returns:
            `UserAnalyticsResponse` with users list sorted by message count descending.
        """
        params: dict[str, Any] = {"limit": limit}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if group_id is not None:
            params["group_id"] = group_id
        return await self._request(
            "GET",
            "/v1/analytics/users",
            model=UserAnalyticsResponse,
            params=params,
        )

    async def get_messages(
        self,
        model_id: Optional[str] = None,
        user_id: Optional[str] = None,
        chat_id: Optional[str] = None,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> Any:
        """Query chat messages with filters.

        Only one filter (chat_id, model_id, or user_id) should be provided.
        If chat_id is given, start_date/end_date/skip/limit are ignored.
        If none are provided, returns an empty list.

        Args:
            model_id: Filter messages by model ID.
            user_id: Filter messages by user ID.
            chat_id: Filter messages by chat ID (takes priority).
            start_date: Start timestamp (epoch seconds).
            end_date: End timestamp (epoch seconds).
            skip: Number of results to skip. Defaults to 0.
            limit: Maximum results to return (max 100). Defaults to 50.

        Returns:
            List of chat message objects (raw dicts). Each message has fields
            like id, chat_id, user_id, role, content, model_id, created_at, etc.
        """
        params: dict[str, Any] = {"skip": skip, "limit": limit}
        if model_id is not None:
            params["model_id"] = model_id
        if user_id is not None:
            params["user_id"] = user_id
        if chat_id is not None:
            params["chat_id"] = chat_id
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        return await self._request(
            "GET",
            "/v1/analytics/messages",
            params=params,
        )

    async def get_summary(
        self,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        group_id: Optional[str] = None,
    ) -> SummaryResponse:
        """Get dashboard summary statistics.

        Returns total counts of messages, chats, models, and users for the
        given time range.

        Args:
            start_date: Start timestamp (epoch seconds) to filter.
            end_date: End timestamp (epoch seconds) to filter.
            group_id: Filter to users in this group.

        Returns:
            `SummaryResponse` with total_messages, total_chats, total_models, total_users.
        """
        params: dict[str, Any] = {}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if group_id is not None:
            params["group_id"] = group_id
        return await self._request(
            "GET",
            "/v1/analytics/summary",
            model=SummaryResponse,
            params=params,
        )

    async def get_daily_stats(
        self,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        group_id: Optional[str] = None,
        granularity: str = "daily",
    ) -> DailyStatsResponse:
        """Get message counts grouped by model for time-series charts.

        Args:
            start_date: Start timestamp (epoch seconds).
            end_date: End timestamp (epoch seconds).
            group_id: Filter to users in this group.
            granularity: Either 'daily' or 'hourly'. Defaults to 'daily'.

        Returns:
            `DailyStatsResponse` with data entries sorted chronologically.
        """
        params: dict[str, Any] = {"granularity": granularity}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if group_id is not None:
            params["group_id"] = group_id
        return await self._request(
            "GET",
            "/v1/analytics/daily",
            model=DailyStatsResponse,
            params=params,
        )

    async def get_token_usage(
        self,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        group_id: Optional[str] = None,
    ) -> TokenUsageResponse:
        """Get token usage aggregated by model, sorted by total tokens descending.

        Args:
            start_date: Start timestamp (epoch seconds).
            end_date: End timestamp (epoch seconds).
            group_id: Filter to users in this group.

        Returns:
            `TokenUsageResponse` with per-model token breakdowns and aggregates.
        """
        params: dict[str, Any] = {}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if group_id is not None:
            params["group_id"] = group_id
        return await self._request(
            "GET",
            "/v1/analytics/tokens",
            model=TokenUsageResponse,
            params=params,
        )

    async def get_model_chats(
        self,
        model_id: str,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> ModelChatsResponse:
        """Get chats that used a specific model, with preview info.

        Args:
            model_id: The model identifier (may contain slashes, e.g. 'openai/gpt-4o').
            start_date: Start timestamp (epoch seconds).
            end_date: End timestamp (epoch seconds).
            skip: Number of results to skip. Defaults to 0.
            limit: Maximum results to return (max 100). Defaults to 50.

        Returns:
            `ModelChatsResponse` with chat previews and total count.
        """
        params: dict[str, Any] = {"skip": skip, "limit": limit}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        return await self._request(
            "GET",
            f"/v1/analytics/models/{model_id}/chats",
            model=ModelChatsResponse,
            params=params,
        )

    async def get_model_overview(
        self,
        model_id: str,
        days: int = 30,
    ) -> ModelOverviewResponse:
        """Get model overview with feedback history and top chat tags.

        Args:
            model_id: The model identifier (may contain slashes, e.g. 'openai/gpt-4o').
            days: Number of days of feedback history. Use 0 for all time. Defaults to 30.

        Returns:
            `ModelOverviewResponse` with daily feedback history (won/lost) and top 10 tags.
        """
        params: dict[str, Any] = {"days": days}
        return await self._request(
            "GET",
            f"/v1/analytics/models/{model_id}/overview",
            model=ModelOverviewResponse,
            params=params,
        )
