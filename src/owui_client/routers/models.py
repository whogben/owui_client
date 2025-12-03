from typing import Optional
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
    async def get_models(
        self,
        query: Optional[str] = None,
        view_option: Optional[str] = None,
        tag: Optional[str] = None,
        order_by: Optional[str] = None,
        direction: Optional[str] = None,
        page: Optional[int] = 1,
    ) -> ModelListResponse:
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
        return await self._request("GET", "/v1/models/base", model=ModelResponse)

    async def get_model_tags(self) -> list[str]:
        return await self._request("GET", "/v1/models/tags", model=str)

    async def create_new_model(self, form_data: ModelForm) -> Optional[ModelModel]:
        return await self._request(
            "POST", "/v1/models/create", model=ModelModel, json=form_data.model_dump()
        )

    async def export_models(self) -> list[ModelModel]:
        return await self._request("GET", "/v1/models/export", model=ModelModel)

    async def import_models(self, form_data: ModelsImportForm) -> bool:
        return await self._request(
            "POST", "/v1/models/import", model=bool, json=form_data.model_dump()
        )

    async def sync_models(self, form_data: SyncModelsForm) -> list[ModelModel]:
        return await self._request(
            "POST", "/v1/models/sync", model=ModelModel, json=form_data.model_dump()
        )

    async def get_model_by_id(self, id: str) -> Optional[ModelResponse]:
        return await self._request(
            "GET", "/v1/models/model", model=ModelResponse, params={"id": id}
        )

    async def get_model_profile_image(self, id: str) -> bytes:
        return await self._request(
            "GET", "/v1/models/model/profile/image", model=bytes, params={"id": id}
        )

    async def toggle_model_by_id(self, id: str) -> Optional[ModelResponse]:
        return await self._request(
            "POST", "/v1/models/model/toggle", model=ModelResponse, params={"id": id}
        )

    async def update_model_by_id(self, form_data: ModelForm) -> Optional[ModelModel]:
        return await self._request(
            "POST", "/v1/models/model/update", model=ModelModel, json=form_data.model_dump()
        )

    async def delete_model_by_id(self, id: str) -> bool:
        return await self._request(
            "POST", "/v1/models/model/delete", model=bool, json={"id": id}
        )

    async def delete_all_models(self) -> bool:
        return await self._request("DELETE", "/v1/models/delete/all", model=bool)

