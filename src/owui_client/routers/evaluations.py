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
    async def get_config(self) -> Dict[str, Any]:
        """
        Get the evaluation configuration.

        :return: Dictionary with evaluation configuration
        """
        return await self._request(
            "GET",
            "/v1/evaluations/config",
        )

    async def update_config(self, form_data: UpdateConfigForm) -> Dict[str, Any]:
        """
        Update the evaluation configuration.

        :param form_data: The configuration update form
        :return: Dictionary with updated evaluation configuration
        """
        return await self._request(
            "POST",
            "/v1/evaluations/config",
            json=form_data.model_dump(),
        )

    async def get_all_feedbacks(self) -> List[FeedbackResponse]:
        """
        Get all feedbacks (admin only).

        :return: List of all feedbacks
        """
        return await self._request(
            "GET",
            "/v1/evaluations/feedbacks/all",
            model=FeedbackResponse,
        )

    async def delete_all_feedbacks(self) -> bool:
        """
        Delete all feedbacks (admin only).

        :return: True if successful
        """
        return await self._request(
            "DELETE",
            "/v1/evaluations/feedbacks/all",
            model=bool,
        )

    async def export_all_feedbacks(self) -> List[FeedbackModel]:
        """
        Export all feedbacks (admin only).

        :return: List of all feedbacks with full data
        """
        return await self._request(
            "GET",
            "/v1/evaluations/feedbacks/all/export",
            model=FeedbackModel,
        )

    async def get_feedbacks_by_user(self) -> List[FeedbackUserResponse]:
        """
        Get feedbacks for the current user.

        :return: List of feedbacks
        """
        return await self._request(
            "GET",
            "/v1/evaluations/feedbacks/user",
            model=FeedbackUserResponse,
        )

    async def delete_feedbacks_by_user(self) -> bool:
        """
        Delete all feedbacks for the current user.

        :return: True if successful
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
        Get feedbacks list with pagination and sorting.

        :param order_by: Field to order by
        :param direction: Sort direction ('asc' or 'desc')
        :param page: Page number
        :return: Feedback list response
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
        Create a new feedback.

        :param form_data: The feedback form data
        :return: The created feedback model
        """
        return await self._request(
            "POST",
            "/v1/evaluations/feedback",
            model=FeedbackModel,
            json=form_data.model_dump(),
        )

    async def get_feedback(self, id: str) -> FeedbackModel:
        """
        Get a feedback by ID.

        :param id: The ID of the feedback
        :return: The feedback model
        """
        return await self._request(
            "GET",
            f"/v1/evaluations/feedback/{id}",
            model=FeedbackModel,
        )

    async def update_feedback(self, id: str, form_data: FeedbackForm) -> FeedbackModel:
        """
        Update a feedback by ID.

        :param id: The ID of the feedback
        :param form_data: The update form data
        :return: The updated feedback model
        """
        return await self._request(
            "POST",
            f"/v1/evaluations/feedback/{id}",
            model=FeedbackModel,
            json=form_data.model_dump(),
        )

    async def delete_feedback(self, id: str) -> bool:
        """
        Delete a feedback by ID.

        :param id: The ID of the feedback
        :return: True if successful
        """
        return await self._request(
            "DELETE",
            f"/v1/evaluations/feedback/{id}",
            model=bool,
        )

