from typing import Optional, Union
from owui_client.client_base import ResourceBase
from owui_client.models.functions import (
    FunctionResponse,
    FunctionUserResponse,
    FunctionModel,
    FunctionWithValvesModel,
    FunctionForm,
    SyncFunctionsForm,
    LoadUrlForm,
)


class FunctionsClient(ResourceBase):
    async def get_functions(self) -> list[FunctionResponse]:
        """
        Get all functions.
        """
        return await self._request(
            "GET",
            "/v1/functions/",
            model=list[FunctionResponse],
        )

    async def get_function_list(self) -> list[FunctionUserResponse]:
        """
        Get list of functions with user info.
        """
        return await self._request(
            "GET",
            "/v1/functions/list",
            model=list[FunctionUserResponse],
        )

    async def export_functions(
        self, include_valves: bool = False
    ) -> list[Union[FunctionModel, FunctionWithValvesModel]]:
        """
        Export functions.
        """
        return await self._request(
            "GET",
            "/v1/functions/export",
            params={"include_valves": include_valves},
            model=list[Union[FunctionModel, FunctionWithValvesModel]],
        )

    async def load_function_from_url(self, url: str) -> Optional[dict]:
        """
        Load a function from a URL.
        """
        return await self._request(
            "POST",
            "/v1/functions/load/url",
            json={"url": url},
            model=Optional[dict],
        )

    async def sync_functions(
        self, functions: list[FunctionWithValvesModel]
    ) -> list[FunctionWithValvesModel]:
        """
        Sync functions.
        """
        form = SyncFunctionsForm(functions=functions)
        return await self._request(
            "POST",
            "/v1/functions/sync",
            json=form.model_dump(),
            model=list[FunctionWithValvesModel],
        )

    async def create_function(
        self, form_data: FunctionForm
    ) -> Optional[FunctionResponse]:
        """
        Create a new function.
        """
        return await self._request(
            "POST",
            "/v1/functions/create",
            json=form_data.model_dump(),
            model=Optional[FunctionResponse],
        )

    async def get_function_by_id(self, id: str) -> Optional[FunctionModel]:
        """
        Get a function by ID.
        """
        return await self._request(
            "GET",
            f"/v1/functions/id/{id}",
            model=Optional[FunctionModel],
        )

    async def toggle_function_by_id(self, id: str) -> Optional[FunctionModel]:
        """
        Toggle a function's active state by ID.
        """
        return await self._request(
            "POST",
            f"/v1/functions/id/{id}/toggle",
            model=Optional[FunctionModel],
        )

    async def toggle_global_by_id(self, id: str) -> Optional[FunctionModel]:
        """
        Toggle a function's global state by ID.
        """
        return await self._request(
            "POST",
            f"/v1/functions/id/{id}/toggle/global",
            model=Optional[FunctionModel],
        )

    async def update_function_by_id(
        self, id: str, form_data: FunctionForm
    ) -> Optional[FunctionModel]:
        """
        Update a function by ID.
        """
        return await self._request(
            "POST",
            f"/v1/functions/id/{id}/update",
            json=form_data.model_dump(),
            model=Optional[FunctionModel],
        )

    async def delete_function_by_id(self, id: str) -> bool:
        """
        Delete a function by ID.
        """
        return await self._request(
            "DELETE",
            f"/v1/functions/id/{id}/delete",
            model=bool,
        )

    async def get_function_valves_by_id(self, id: str) -> Optional[dict]:
        """
        Get function valves by ID.
        """
        return await self._request(
            "GET",
            f"/v1/functions/id/{id}/valves",
            model=Optional[dict],
        )

    async def get_function_valves_spec_by_id(self, id: str) -> Optional[dict]:
        """
        Get function valves specification by ID.
        """
        return await self._request(
            "GET",
            f"/v1/functions/id/{id}/valves/spec",
            model=Optional[dict],
        )

    async def update_function_valves_by_id(
        self, id: str, valves: dict
    ) -> Optional[dict]:
        """
        Update function valves by ID.
        """
        return await self._request(
            "POST",
            f"/v1/functions/id/{id}/valves/update",
            json=valves,
            model=Optional[dict],
        )

    async def get_function_user_valves_by_id(self, id: str) -> Optional[dict]:
        """
        Get function user valves by ID.
        """
        return await self._request(
            "GET",
            f"/v1/functions/id/{id}/valves/user",
            model=Optional[dict],
        )

    async def get_function_user_valves_spec_by_id(self, id: str) -> Optional[dict]:
        """
        Get function user valves specification by ID.
        """
        return await self._request(
            "GET",
            f"/v1/functions/id/{id}/valves/user/spec",
            model=Optional[dict],
        )

    async def update_function_user_valves_by_id(
        self, id: str, valves: dict
    ) -> Optional[dict]:
        """
        Update function user valves by ID.
        """
        return await self._request(
            "POST",
            f"/v1/functions/id/{id}/valves/user/update",
            json=valves,
            model=Optional[dict],
        )

