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
    ModelAccessGrantsForm,
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
            `ModelListResponse`: List of models and total count.
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

    async def get_base_model_tags(self) -> list[str]:
        """
        Get the distinct set of tags used across base models.

        Base models are models with no `base_model_id` (i.e. the underlying
        connected models, as opposed to workspace/derived models). Tags are
        collected from each base model's `meta.tags` entries. Requires admin
        privileges.

        Returns:
            list[str]: Sorted, de-duplicated list of base-model tag names.
        """
        return await self._request(
            "GET", "/v1/models/base/tags", model=list[str]
        )

    async def get_base_models(self) -> list[ModelResponse]:
        """
        Get all base models.

        Returns:
            list[ModelResponse]: List of base models.
        """
        return await self._request("GET", "/v1/models/base", model=list[ModelResponse])

    async def get_base_models_direct(self) -> list[ModelResponse]:
        """
        Get all base models (direct endpoint).

        This is the legacy endpoint from main.py that provides base models.

        Returns:
            list[ModelResponse]: List of base models.
        """
        return await self._request("GET", "/api/models/base", model=list[ModelResponse])

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
            "POST",
            "/v1/models/create",
            model=Optional[ModelModel],
            json=form_data.model_dump(exclude_none=True),
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
            "POST", "/v1/models/import", model=bool, json=form_data.model_dump(exclude_none=True)
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
            "POST",
            "/v1/models/sync",
            model=list[ModelModel],
            json=form_data.model_dump(exclude_none=True),
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
            "POST",
            "/v1/models/model/toggle",
            model=Optional[ModelResponse],
            params={"id": id},
        )

    async def update_model_by_id(self, form_data: ModelForm) -> Optional[ModelModel]:
        """
        Update a model.

        Args:
            form_data: The updated model data (must include ID).

        Returns:
            Optional[ModelModel]: The updated model.

        Note:
            How `access_grants` is handled depends on whether the caller specifies it:

            - **Caller omits `access_grants` (or passes `None`):** the model's existing grants
              are preserved by fetching them via `get_model_by_id` and re-sending them. This
              mirrors the frontend, which always re-sends the current grant list on update.
            - **Caller passes a populated list:** the grants are replaced with that list.
            - **Caller passes `[]`:** the grants are cleared (intentional).

            A list must always be sent (never `None` or omitted from the JSON body): the
            backend handler re-validates the body as `ModelForm(**form_data.model_dump())`,
            and `ModelForm.access_grants` is typed `list[dict | None] = None` (a pydantic v2
            gotcha that rejects an explicit `None`), so sending `None` raises an unhandled
            ValidationError -> HTTP 500 (present in Open WebUI 0.9.6-0.10.1). On the DB side,
            a non-`None` list is passed to `AccessGrants.set_access_grants`, which deletes all
            existing grants and re-inserts the provided ones — so an unconditional `[]` would
            silently wipe any sharing grants. Preserving the current list avoids both pitfalls.
            If the current model cannot be fetched, `[]` is used as a last-resort fallback.
            Note: when grants are omitted they are fetched then re-sent in a separate GET
            followed by the POST, so a concurrent writer could change grants between the
            two calls; this matches the frontend's behavior.
        """
        payload = form_data.model_dump(exclude_none=True)
        if "access_grants" not in payload:
            # Caller did not specify access_grants (it was omitted or None). Preserve the
            # model's existing grants rather than wiping them: fetch the current list and
            # re-send it. We must still send a list (not None) to dodge the backend 500.
            current = await self.get_model_by_id(form_data.id)
            payload["access_grants"] = (
                [g.model_dump() for g in current.access_grants]
                if current is not None
                else []
            )
        return await self._request(
            "POST",
            "/v1/models/model/update",
            model=Optional[ModelModel],
            json=payload,
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

    async def update_model_access(
        self, form_data: ModelAccessGrantsForm
    ) -> Optional[ModelModel]:
        """
        Update a model's access grants.

        Args:
            form_data: The form containing the model ID and access grants.

        Returns:
            Optional[ModelModel]: The updated model.
        """
        return await self._request(
            "POST",
            "/v1/models/model/access/update",
            model=Optional[ModelModel],
            json=form_data.model_dump(),
        )

    async def unload_model(self, model: str) -> dict:
        """
        Unload a model from its provider.

        Resolves the provider that owns the model and calls its native unload
        mechanism. Supports Ollama (keep_alive=0) and llama.cpp (/models/unload).
        Requires admin privileges.

        Args:
            model: The model ID to unload.

        Returns:
            dict: Provider-specific response. Ollama returns `{"status": True}`.

        Raises:
            HTTPException: 400 if provider doesn't support unloading, 404 if
                model not found, 500 on provider errors.
        """
        return await self._request(
            "POST",
            "/api/models/unload",
            model=dict,
            json={"model": model},
        )
