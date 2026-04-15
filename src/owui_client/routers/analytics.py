"""Client for the Analytics endpoints."""

from typing import Optional
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
from owui_client.models.chat_messages import ChatMessageModel


class AnalyticsClient(ResourceBase):
    """Client for the Analytics endpoints."""

    async def get_model_analytics(
        self,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        group_id: Optional[str] = None,
    ) -> ModelAnalyticsResponse:
        """Get message counts per model.

        Args:
            start_date: Start timestamp (epoch).
            end_date: End timestamp (epoch).
            group_id: Filter by user group ID.
        """
        params = {}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if group_id:
            params["group_id"] = group_id
        return await self._request(
            "GET", "/v1/analytics/models", model=ModelAnalyticsResponse, params=params
        )

    async def get_user_analytics(
        self,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        group_id: Optional[str] = None,
        limit: int = 50,
    ) -> UserAnalyticsResponse:
        """Get message counts and token usage per user.

        Args:
            start_date: Start timestamp (epoch).
            end_date: End timestamp (epoch).
            group_id: Filter by user group ID.
            limit: Max users to return.
        """
        params = {}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if group_id:
            params["group_id"] = group_id
        if limit != 50:
            params["limit"] = limit
        return await self._request(
            "GET", "/v1/analytics/users", model=UserAnalyticsResponse, params=params
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
    ) -> list[ChatMessageModel]:
        """Query messages with filters.

        At least one of model_id, user_id, or chat_id should be provided.
        Returns an empty list if no filter is specified.

        Args:
            model_id: Filter by model ID.
            user_id: Filter by user ID.
            chat_id: Filter by chat ID.
            start_date: Start timestamp (epoch).
            end_date: End timestamp (epoch).
            skip: Number of results to skip.
            limit: Max results (max 100).
        """
        params = {}
        if model_id:
            params["model_id"] = model_id
        if user_id:
            params["user_id"] = user_id
        if chat_id:
            params["chat_id"] = chat_id
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if skip != 0:
            params["skip"] = skip
        if limit != 50:
            params["limit"] = limit
        return await self._request(
            "GET", "/v1/analytics/messages", model=list[ChatMessageModel], params=params
        )

    async def get_summary(
        self,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        group_id: Optional[str] = None,
    ) -> SummaryResponse:
        """Get dashboard summary statistics.

        Args:
            start_date: Start timestamp (epoch).
            end_date: End timestamp (epoch).
            group_id: Filter by user group ID.
        """
        params = {}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if group_id:
            params["group_id"] = group_id
        return await self._request(
            "GET", "/v1/analytics/summary", model=SummaryResponse, params=params
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
            start_date: Start timestamp (epoch).
            end_date: End timestamp (epoch).
            group_id: Filter by user group ID.
            granularity: 'daily' or 'hourly'.
        """
        params = {}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if group_id:
            params["group_id"] = group_id
        if granularity != "daily":
            params["granularity"] = granularity
        return await self._request(
            "GET", "/v1/analytics/daily", model=DailyStatsResponse, params=params
        )

    async def get_token_usage(
        self,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        group_id: Optional[str] = None,
    ) -> TokenUsageResponse:
        """Get token usage aggregated by model.

        Args:
            start_date: Start timestamp (epoch).
            end_date: End timestamp (epoch).
            group_id: Filter by user group ID.
        """
        params = {}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if group_id:
            params["group_id"] = group_id
        return await self._request(
            "GET", "/v1/analytics/tokens", model=TokenUsageResponse, params=params
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
            model_id: The model ID to filter by.
            start_date: Start timestamp (epoch).
            end_date: End timestamp (epoch).
            skip: Number of results to skip.
            limit: Max results (max 100).
        """
        params = {}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if skip != 0:
            params["skip"] = skip
        if limit != 50:
            params["limit"] = limit
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
        """Get model overview with feedback history and chat tags.

        Args:
            model_id: The model ID.
            days: Number of days of history (0 for all).
        """
        params = {}
        if days != 30:
            params["days"] = days
        return await self._request(
            "GET",
            f"/v1/analytics/models/{model_id}/overview",
            model=ModelOverviewResponse,
            params=params,
        )
