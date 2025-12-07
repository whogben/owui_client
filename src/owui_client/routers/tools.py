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
    """
    Client for the Tools endpoints.
    """

    async def get_tools(self) -> List[ToolUserResponse]:
        """
        Get all available tools.

        This includes local tools and tools from configured servers (OpenAPI, MCP).

        Returns:
            List[ToolUserResponse]: List of tools with user information.
        """
        return await self._request(
            "GET",
            "/v1/tools/",
            model=List[ToolUserResponse],
        )

    async def get_tool_list(self) -> List[ToolUserResponse]:
        """
        Get list of tools the user has write access to.

        Returns:
            List[ToolUserResponse]: List of tools.
        """
        return await self._request(
            "GET",
            "/v1/tools/list",
            model=List[ToolUserResponse],
        )

    async def load_tool_from_url(self, form_data: LoadUrlForm) -> Optional[Dict[str, Any]]:
        """
        Load a tool's code and metadata from a URL.

        Args:
            form_data: The URL information.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing 'name' and 'content' of the tool, or None if failed.
        """
        return await self._request(
            "POST",
            "/v1/tools/load/url",
            json=form_data.model_dump(mode="json"),
            model=Optional[Dict[str, Any]],
        )

    async def export_tools(self) -> List[ToolModel]:
        """
        Export all tools the user has read access to.

        Returns:
            List[ToolModel]: List of tools with full content.
        """
        return await self._request(
            "GET",
            "/v1/tools/export",
            model=List[ToolModel],
        )

    async def create_new_tool(self, form_data: ToolForm) -> Optional[ToolResponse]:
        """
        Create a new tool.

        Args:
            form_data: The tool data, including ID, name, and Python content.

        Returns:
            Optional[ToolResponse]: The created tool metadata.
        """
        return await self._request(
            "POST",
            "/v1/tools/create",
            json=form_data.model_dump(mode="json"),
            model=Optional[ToolResponse],
        )

    async def get_tool_by_id(self, id: str) -> Optional[ToolModel]:
        """
        Get a tool by its unique ID.

        Args:
            id: The tool ID.

        Returns:
            Optional[ToolModel]: The tool details.
        """
        return await self._request(
            "GET",
            f"/v1/tools/id/{id}",
            model=Optional[ToolModel],
        )

    async def update_tool_by_id(self, id: str, form_data: ToolForm) -> Optional[ToolModel]:
        """
        Update a tool by ID.

        Args:
            id: The tool ID.
            form_data: The updated tool data.

        Returns:
            Optional[ToolModel]: The updated tool details.
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

        Args:
            id: The tool ID.

        Returns:
            bool: True if successful, False otherwise.
        """
        return await self._request(
            "DELETE",
            f"/v1/tools/id/{id}/delete",
            model=bool,
        )

    async def get_tool_valves_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Get the current valve settings for a tool.

        Args:
            id: The tool ID.

        Returns:
            Optional[Dict[str, Any]]: The valve settings.
        """
        return await self._request(
            "GET",
            f"/v1/tools/id/{id}/valves",
            model=Optional[Dict[str, Any]],
        )

    async def get_tool_valves_spec_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Get the specification (schema) for the tool's valves.

        Args:
            id: The tool ID.

        Returns:
            Optional[Dict[str, Any]]: The JSON schema for the valves.
        """
        return await self._request(
            "GET",
            f"/v1/tools/id/{id}/valves/spec",
            model=Optional[Dict[str, Any]],
        )

    async def update_tool_valves_by_id(self, id: str, valves: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update the valve settings for a tool.

        Args:
            id: The tool ID.
            valves: The new valve settings.

        Returns:
            Optional[Dict[str, Any]]: The updated valve settings.
        """
        return await self._request(
            "POST",
            f"/v1/tools/id/{id}/valves/update",
            json=valves,
            model=Optional[Dict[str, Any]],
        )

    async def get_tool_user_valves_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Get user-specific valve settings for a tool.

        Args:
            id: The tool ID.

        Returns:
            Optional[Dict[str, Any]]: The user's valve settings.
        """
        return await self._request(
            "GET",
            f"/v1/tools/id/{id}/valves/user",
            model=Optional[Dict[str, Any]],
        )

    async def get_tool_user_valves_spec_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Get the specification (schema) for the tool's user valves.

        Args:
            id: The tool ID.

        Returns:
            Optional[Dict[str, Any]]: The JSON schema for the user valves.
        """
        return await self._request(
            "GET",
            f"/v1/tools/id/{id}/valves/user/spec",
            model=Optional[Dict[str, Any]],
        )

    async def update_tool_user_valves_by_id(self, id: str, valves: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update user-specific valve settings for a tool.

        Args:
            id: The tool ID.
            valves: The new valve settings.

        Returns:
            Optional[Dict[str, Any]]: The updated valve settings.
        """
        return await self._request(
            "POST",
            f"/v1/tools/id/{id}/valves/user/update",
            json=valves,
            model=Optional[Dict[str, Any]],
        )

