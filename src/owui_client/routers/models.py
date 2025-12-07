from typing import Optional, List
from owui_client.client_base import ResourceBase
from owui_client.models.models import (
    ModelListResponse,
    ModelResponse,
    ModelUserResponse,
    ModelForm,
    ModelModel,
    ModelsImportForm,
    SyncModelsForm,
    ModelIdForm,
)


class ModelsClient(ResourceBase):
    """
    Client for the Models endpoints.
    """

    async def get_models(
        self,
        query: Optional[str] = None,
        view_option: Optional[str] = None,
        tag: Optional[str] = None,
        order_by: Optional[str] = None,
        direction: Optional[str] = None,
        page: Optional[int] = 1,
    ) -> ModelListResponse:
        """
        Get a list of models with optional filtering and pagination.

        Args:
            query: Search query string.
            view_option: View option. Accepted values:
                - `created`: Show models created by the user.
                - `shared`: Show models shared with the user (not created by them).
                - `None` (default): Show all accessible models.
            tag: Filter by tag.
            order_by: Field to order by ('name', 'created_at', 'updated_at').
            direction: Sort direction ('asc', 'desc').
            page: Page number (1-based).

        Returns:
            ModelListResponse: List of models and total count.
        """
        params = {}
        if query:
            params["query"] = query
        if view_option:
            params["view_option"] = view_option
        if tag:
            params["tag"] = tag
        if order_by:
            params["order_by"] = order_by
        if direction:
            params["direction"] = direction
        if page:
            params["page"] = page

        return await self._request(
            "GET", "/v1/models/list", model=ModelListResponse, params=params
        )

    async def get_base_models(self) -> list[ModelResponse]:
        """
        Get all base models.

        Returns:
            list[ModelResponse]: List of base models.
        """
        return await self._request("GET", "/v1/models/base", model=list[ModelResponse])

    async def get_model_tags(self) -> list[str]:
        """
        Get all unique tags used in models.

        Returns:
            list[str]: List of tag names.
        """
        return await self._request("GET", "/v1/models/tags", model=list[str])

    async def create_new_model(self, form_data: ModelForm) -> Optional[ModelModel]:
        """
        Create a new model.

        Requires valid permissions (admin or `workspace.models`).
        The model ID must be unique and <= 256 characters.

        Args:
            form_data: The model data to create.

        Returns:
            Optional[ModelModel]: The created model.
        """
        return await self._request(
            "POST", "/v1/models/create", model=Optional[ModelModel], json=form_data.model_dump()
        )

    async def export_models(self) -> list[ModelModel]:
        """
        Export all models.

        Returns:
            list[ModelModel]: List of all models.
        """
        return await self._request("GET", "/v1/models/export", model=list[ModelModel])

    async def import_models(self, form_data: ModelsImportForm) -> bool:
        """
        Import models.

        Args:
            form_data: The form data containing models to import.

        Returns:
            bool: True if import was successful.
        """
        return await self._request(
            "POST", "/v1/models/import", model=bool, json=form_data.model_dump()
        )

    async def sync_models(self, form_data: SyncModelsForm) -> list[ModelModel]:
        """
        Sync models.

        Args:
            form_data: The models to sync.

        Returns:
            list[ModelModel]: The list of synced models.
        """
        return await self._request(
            "POST", "/v1/models/sync", model=list[ModelModel], json=form_data.model_dump()
        )

    async def get_model_by_id(self, id: str) -> Optional[ModelResponse]:
        """
        Get a model by ID.

        Args:
            id: The model ID.

        Returns:
            Optional[ModelResponse]: The model details.
        """
        return await self._request(
            "GET", "/v1/models/model", model=Optional[ModelResponse], params={"id": id}
        )

    async def get_model_profile_image(self, id: str) -> bytes:
        """
        Get a model's profile image.

        Args:
            id: The model ID.

        Returns:
            bytes: The image data.
        """
        return await self._request(
            "GET", "/v1/models/model/profile/image", model=bytes, params={"id": id}
        )

    async def toggle_model_by_id(self, id: str) -> Optional[ModelResponse]:
        """
        Toggle a model's active state.

        Args:
            id: The model ID.

        Returns:
            Optional[ModelResponse]: The updated model.
        """
        return await self._request(
            "POST", "/v1/models/model/toggle", model=Optional[ModelResponse], params={"id": id}
        )

    async def update_model_by_id(self, form_data: ModelForm) -> Optional[ModelModel]:
        """
        Update a model.

        Args:
            form_data: The updated model data (must include ID).

        Returns:
            Optional[ModelModel]: The updated model.
        """
        return await self._request(
            "POST", "/v1/models/model/update", model=Optional[ModelModel], json=form_data.model_dump()
        )

    async def delete_model_by_id(self, id: str) -> bool:
        """
        Delete a model by ID.

        Args:
            id: The model ID.

        Returns:
            bool: True if deletion was successful.
        """
        return await self._request(
            "POST", "/v1/models/model/delete", model=bool, json={"id": id}
        )

    async def delete_all_models(self) -> bool:
        """
        Delete all models.

        Returns:
            bool: True if successful.
        """
        return await self._request("DELETE", "/v1/models/delete/all", model=bool)
