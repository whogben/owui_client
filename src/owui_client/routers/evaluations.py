from typing import Optional, List, Dict, Any
from owui_client.client_base import ResourceBase
from owui_client.models.evaluations import UpdateConfigForm
from owui_client.models.feedbacks import (
    FeedbackModel,
    FeedbackResponse,
    FeedbackForm,
    FeedbackUserResponse,
    FeedbackListResponse,
)


class EvaluationsClient(ResourceBase):
    """
    Client for the Evaluations endpoints.
    Handles configuration of evaluation arena models and management of feedback.
    """
    async def get_config(self) -> Dict[str, Any]:
        """
        Get the current evaluation configuration.

        Returns:
            Dict[str, Any]: A dictionary containing evaluation settings, including:
            - ENABLE_EVALUATION_ARENA_MODELS (bool): Whether evaluation arena models are enabled.
            - EVALUATION_ARENA_MODELS (list[dict]): List of configured arena models.
        """
        return await self._request(
            "GET",
            "/v1/evaluations/config",
        )

    async def update_config(self, form_data: UpdateConfigForm) -> Dict[str, Any]:
        """
        Update the evaluation configuration.

        Args:
            form_data: The configuration update form containing fields to update.

        Returns:
            Dict[str, Any]: The updated evaluation configuration.
        """
        return await self._request(
            "POST",
            "/v1/evaluations/config",
            json=form_data.model_dump(),
        )

    async def get_all_feedbacks(self) -> List[FeedbackResponse]:
        """
        Get all feedbacks (admin only).

        Returns:
            List[FeedbackResponse]: A list of all feedback entries in the system.
        """
        return await self._request(
            "GET",
            "/v1/evaluations/feedbacks/all",
            model=FeedbackResponse,
        )

    async def delete_all_feedbacks(self) -> bool:
        """
        Delete all feedbacks (admin only).

        Returns:
            bool: True if the operation was successful.
        """
        return await self._request(
            "DELETE",
            "/v1/evaluations/feedbacks/all",
            model=bool,
        )

    async def export_all_feedbacks(self) -> List[FeedbackModel]:
        """
        Export all feedbacks with full data details (admin only).

        Returns:
            List[FeedbackModel]: A list of all feedback models with complete data for export.
        """
        return await self._request(
            "GET",
            "/v1/evaluations/feedbacks/all/export",
            model=FeedbackModel,
        )

    async def get_feedbacks_by_user(self) -> List[FeedbackUserResponse]:
        """
        Get feedbacks submitted by the current user.

        Returns:
            List[FeedbackUserResponse]: A list of feedbacks submitted by the user.
        """
        return await self._request(
            "GET",
            "/v1/evaluations/feedbacks/user",
            model=FeedbackUserResponse,
        )

    async def delete_feedbacks_by_user(self) -> bool:
        """
        Delete all feedbacks submitted by the current user.

        Returns:
            bool: True if the operation was successful.
        """
        return await self._request(
            "DELETE",
            "/v1/evaluations/feedbacks",
            model=bool,
        )

    async def get_feedbacks_list(
        self,
        order_by: Optional[str] = None,
        direction: Optional[str] = None,
        page: Optional[int] = 1,
    ) -> FeedbackListResponse:
        """
        Get a paginated and sorted list of feedbacks (admin only).

        Args:
            order_by: The field name to order the results by (e.g., 'created_at').
            direction: The sort direction, either 'asc' (ascending) or 'desc' (descending).
            page: The page number to retrieve (default is 1).

        Returns:
            FeedbackListResponse: A response object containing the list of feedbacks and pagination details.
        """
        params = {}
        if order_by:
            params["order_by"] = order_by
        if direction:
            params["direction"] = direction
        if page:
            params["page"] = page

        return await self._request(
            "GET",
            "/v1/evaluations/feedbacks/list",
            model=FeedbackListResponse,
            params=params,
        )

    async def create_feedback(self, form_data: FeedbackForm) -> FeedbackModel:
        """
        Create a new feedback entry.

        Args:
            form_data: The data for the new feedback (e.g., type, content, data).

        Returns:
            FeedbackModel: The created feedback object.
        """
        return await self._request(
            "POST",
            "/v1/evaluations/feedback",
            model=FeedbackModel,
            json=form_data.model_dump(),
        )

    async def get_feedback(self, id: str) -> FeedbackModel:
        """
        Get a specific feedback entry by its ID.

        Args:
            id: The unique identifier of the feedback to retrieve.

        Returns:
            FeedbackModel: The requested feedback object.
        """
        return await self._request(
            "GET",
            f"/v1/evaluations/feedback/{id}",
            model=FeedbackModel,
        )

    async def update_feedback(self, id: str, form_data: FeedbackForm) -> FeedbackModel:
        """
        Update a specific feedback entry by its ID.

        Args:
            id: The unique identifier of the feedback to update.
            form_data: The updated data for the feedback.

        Returns:
            FeedbackModel: The updated feedback object.
        """
        return await self._request(
            "POST",
            f"/v1/evaluations/feedback/{id}",
            model=FeedbackModel,
            json=form_data.model_dump(),
        )

    async def delete_feedback(self, id: str) -> bool:
        """
        Delete a specific feedback entry by its ID.

        Args:
            id: The unique identifier of the feedback to delete.

        Returns:
            bool: True if the operation was successful.
        """
        return await self._request(
            "DELETE",
            f"/v1/evaluations/feedback/{id}",
            model=bool,
        )

