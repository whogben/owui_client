from typing import Dict, Any, Optional, List
from owui_client.client_base import ResourceBase
from owui_client.models.configs import (
    ImportConfigForm, 
    ConnectionsConfigForm,
    OAuthClientRegistrationForm,
    ToolServersConfigForm,
    ToolServerConnection,
    CodeInterpreterConfigForm,
    ModelsConfigForm,
    PromptSuggestion,
    SetDefaultSuggestionsForm,
    BannerModel,
    SetBannersForm
)

class ConfigsClient(ResourceBase):
    async def export_config(self) -> Dict[str, Any]:
        """
        Export the current system configuration.

        This returns the full configuration dictionary including all settings,
        models, and other system-wide configurations.

        Returns:
            The configuration dictionary.
        """
        return await self._request(
            "GET",
            "/v1/configs/export",
            model=dict,
        )

    async def import_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Import a system configuration.

        Args:
            config: The configuration dictionary to import.

        Returns:
            The updated configuration dictionary.
        """
        return await self._request(
            "POST",
            "/v1/configs/import",
            model=dict,
            json=ImportConfigForm(config=config).model_dump(),
        )

    async def get_connections_config(self) -> ConnectionsConfigForm:
        """
        Get the current connections configuration.

        Returns:
            ConnectionsConfigForm with current settings for direct connections and model caching.
        """
        return await self._request(
            "GET",
            "/v1/configs/connections",
            model=ConnectionsConfigForm,
        )

    async def set_connections_config(
        self, form_data: ConnectionsConfigForm
    ) -> ConnectionsConfigForm:
        """
        Set the connections configuration.

        Args:
            form_data: ConnectionsConfigForm with new settings.

        Returns:
            Updated ConnectionsConfigForm.
        """
        return await self._request(
            "POST",
            "/v1/configs/connections",
            model=ConnectionsConfigForm,
            json=form_data.model_dump(),
        )

    async def register_oauth_client(
        self, form_data: OAuthClientRegistrationForm, type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Register an OAuth client.

        Used for services like MCP Tool Servers that require OAuth 2.1 authentication/registration.

        Args:
            form_data: Registration details (url, client_id, client_name).
            type: Optional type prefix for the client_id (e.g. 'mcp').

        Returns:
            Dictionary containing status and encrypted oauth_client_info.
        """
        params = {}
        if type:
            params["type"] = type
        
        return await self._request(
            "POST",
            "/v1/configs/oauth/clients/register",
            model=dict,
            json=form_data.model_dump(),
            params=params,
        )

    async def get_tool_servers_config(self) -> ToolServersConfigForm:
        """
        Get the current tool servers configuration.

        Returns:
            ToolServersConfigForm with current settings.
        """
        return await self._request(
            "GET",
            "/v1/configs/tool_servers",
            model=ToolServersConfigForm,
        )

    async def set_tool_servers_config(
        self, form_data: ToolServersConfigForm
    ) -> ToolServersConfigForm:
        """
        Set the tool servers configuration.

        Args:
            form_data: ToolServersConfigForm with new settings.

        Returns:
            Updated ToolServersConfigForm.
        """
        return await self._request(
            "POST",
            "/v1/configs/tool_servers",
            model=ToolServersConfigForm,
            json=form_data.model_dump(),
        )

    async def verify_tool_servers_config(
        self, form_data: ToolServerConnection
    ) -> Dict[str, Any]:
        """
        Verify a tool server connection.

        This endpoint attempts to connect to the tool server using the provided
        configuration and returns the server specifications if successful.

        Args:
            form_data: ToolServerConnection details to verify.

        Returns:
            Response dictionary containing verification status and server specs (if successful).
        """
        return await self._request(
            "POST",
            "/v1/configs/tool_servers/verify",
            model=dict,
            json=form_data.model_dump(),
        )

    async def get_code_execution_config(self) -> CodeInterpreterConfigForm:
        """
        Get the current code execution configuration.

        Returns:
            CodeInterpreterConfigForm with current settings.
        """
        return await self._request(
            "GET",
            "/v1/configs/code_execution",
            model=CodeInterpreterConfigForm,
        )

    async def set_code_execution_config(
        self, form_data: CodeInterpreterConfigForm
    ) -> CodeInterpreterConfigForm:
        """
        Set the code execution configuration.

        Args:
            form_data: CodeInterpreterConfigForm with new settings.

        Returns:
            Updated CodeInterpreterConfigForm.
        """
        return await self._request(
            "POST",
            "/v1/configs/code_execution",
            model=CodeInterpreterConfigForm,
            json=form_data.model_dump(),
        )

    async def get_models_config(self) -> ModelsConfigForm:
        """
        Get the current models configuration.

        Returns:
            ModelsConfigForm with current settings.
        """
        return await self._request(
            "GET",
            "/v1/configs/models",
            model=ModelsConfigForm,
        )

    async def set_models_config(self, form_data: ModelsConfigForm) -> ModelsConfigForm:
        """
        Set the models configuration.

        Args:
            form_data: ModelsConfigForm with new settings.

        Returns:
            Updated ModelsConfigForm.
        """
        return await self._request(
            "POST",
            "/v1/configs/models",
            model=ModelsConfigForm,
            json=form_data.model_dump(),
        )

    async def set_default_suggestions(
        self, form_data: SetDefaultSuggestionsForm
    ) -> List[PromptSuggestion]:
        """
        Set default prompt suggestions.

        Args:
            form_data: SetDefaultSuggestionsForm containing the suggestions list.

        Returns:
            Updated list of PromptSuggestion.
        """
        return await self._request(
            "POST",
            "/v1/configs/suggestions",
            model=List[PromptSuggestion],
            json=form_data.model_dump(),
        )

    async def get_banners(self) -> List[BannerModel]:
        """
        Get the current banners.

        Returns:
            List of BannerModel.
        """
        return await self._request(
            "GET",
            "/v1/configs/banners",
            model=List[BannerModel],
        )

    async def set_banners(self, form_data: SetBannersForm) -> List[BannerModel]:
        """
        Set the banners.

        Args:
            form_data: SetBannersForm containing the banners list.

        Returns:
            Updated list of BannerModel.
        """
        return await self._request(
            "POST",
            "/v1/configs/banners",
            model=List[BannerModel],
            json=form_data.model_dump(),
        )
