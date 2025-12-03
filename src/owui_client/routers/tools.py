from typing import List, Optional, Dict, Any
from owui_client.client_base import ResourceBase
from owui_client.models.tools import (
    ToolUserResponse,
    ToolModel,
    ToolResponse,
    ToolForm,
    LoadUrlForm,
)

class ToolsClient(ResourceBase):
    async def get_tools(self) -> List[ToolUserResponse]:
        """
        Get all tools.
        """
        return await self._request(
            "GET",
            "/v1/tools/",
            model=List[ToolUserResponse],
        )

    async def get_tool_list(self) -> List[ToolUserResponse]:
        """
        Get list of tools.
        """
        return await self._request(
            "GET",
            "/v1/tools/list",
            model=List[ToolUserResponse],
        )

    async def load_tool_from_url(self, form_data: LoadUrlForm) -> Optional[Dict[str, Any]]:
        """
        Load a tool from a URL.
        """
        return await self._request(
            "POST",
            "/v1/tools/load/url",
            json=form_data.model_dump(mode="json"),
            model=Optional[Dict[str, Any]],
        )

    async def export_tools(self) -> List[ToolModel]:
        """
        Export tools.
        """
        return await self._request(
            "GET",
            "/v1/tools/export",
            model=List[ToolModel],
        )

    async def create_new_tool(self, form_data: ToolForm) -> Optional[ToolResponse]:
        """
        Create a new tool.
        """
        return await self._request(
            "POST",
            "/v1/tools/create",
            json=form_data.model_dump(mode="json"),
            model=Optional[ToolResponse],
        )

    async def get_tool_by_id(self, id: str) -> Optional[ToolModel]:
        """
        Get a tool by ID.
        """
        return await self._request(
            "GET",
            f"/v1/tools/id/{id}",
            model=Optional[ToolModel],
        )

    async def update_tool_by_id(self, id: str, form_data: ToolForm) -> Optional[ToolModel]:
        """
        Update a tool by ID.
        """
        return await self._request(
            "POST",
            f"/v1/tools/id/{id}/update",
            json=form_data.model_dump(mode="json"),
            model=Optional[ToolModel],
        )

    async def delete_tool_by_id(self, id: str) -> bool:
        """
        Delete a tool by ID.
        """
        return await self._request(
            "DELETE",
            f"/v1/tools/id/{id}/delete",
            model=bool,
        )

    async def get_tool_valves_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Get tool valves by ID.
        """
        return await self._request(
            "GET",
            f"/v1/tools/id/{id}/valves",
            model=Optional[Dict[str, Any]],
        )

    async def get_tool_valves_spec_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Get tool valves spec by ID.
        """
        return await self._request(
            "GET",
            f"/v1/tools/id/{id}/valves/spec",
            model=Optional[Dict[str, Any]],
        )

    async def update_tool_valves_by_id(self, id: str, valves: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update tool valves by ID.
        """
        return await self._request(
            "POST",
            f"/v1/tools/id/{id}/valves/update",
            json=valves,
            model=Optional[Dict[str, Any]],
        )

    async def get_tool_user_valves_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Get tool user valves by ID.
        """
        return await self._request(
            "GET",
            f"/v1/tools/id/{id}/valves/user",
            model=Optional[Dict[str, Any]],
        )

    async def get_tool_user_valves_spec_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Get tool user valves spec by ID.
        """
        return await self._request(
            "GET",
            f"/v1/tools/id/{id}/valves/user/spec",
            model=Optional[Dict[str, Any]],
        )

    async def update_tool_user_valves_by_id(self, id: str, valves: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update tool user valves by ID.
        """
        return await self._request(
            "POST",
            f"/v1/tools/id/{id}/valves/user/update",
            json=valves,
            model=Optional[Dict[str, Any]],
        )

