from typing import Optional, List
from owui_client.client_base import ResourceBase
from owui_client.models.prompts import PromptModel, PromptUserResponse, PromptForm


class PromptsClient(ResourceBase):
    """
    Client for the Prompts endpoints.
    """

    async def get_prompts(self) -> List[PromptModel]:
        """
        Get all prompts (read access).

        Returns:
            List[PromptModel]: List of prompts.
        """
        return await self._request(
            "GET", "/v1/prompts/", model=List[PromptModel]
        )

    async def get_prompt_list(self) -> List[PromptUserResponse]:
        """
        Get all prompts with user info (write access).

        Returns:
            List[PromptUserResponse]: List of prompts with user details.
        """
        return await self._request(
            "GET", "/v1/prompts/list", model=List[PromptUserResponse]
        )

    async def create_new_prompt(self, form_data: PromptForm) -> Optional[PromptModel]:
        """
        Create a new prompt.

        Args:
            form_data: The prompt data. The `command` field must start with a slash (e.g., '/help').

        Returns:
            Optional[PromptModel]: The created prompt.
        """
        return await self._request(
            "POST",
            "/v1/prompts/create",
            json=form_data.model_dump(),
            model=Optional[PromptModel],
        )

    async def get_prompt_by_command(self, command: str) -> Optional[PromptModel]:
        """
        Get a prompt by command.

        Args:
            command: The command trigger (e.g., 'help' or '/help'). Leading slash is automatically handled.

        Returns:
            Optional[PromptModel]: The prompt details.
        """
        clean_command = command.lstrip("/")
        return await self._request(
            "GET",
            f"/v1/prompts/command/{clean_command}",
            model=Optional[PromptModel],
        )

    async def update_prompt_by_command(
        self, command: str, form_data: PromptForm
    ) -> Optional[PromptModel]:
        """
        Update a prompt by command.

        Args:
            command: The command trigger (e.g., 'help' or '/help'). Leading slash is automatically handled.
            form_data: The updated prompt data.

        Returns:
            Optional[PromptModel]: The updated prompt.
        """
        clean_command = command.lstrip("/")
        return await self._request(
            "POST",
            f"/v1/prompts/command/{clean_command}/update",
            json=form_data.model_dump(),
            model=Optional[PromptModel],
        )

    async def delete_prompt_by_command(self, command: str) -> bool:
        """
        Delete a prompt by command.

        Args:
            command: The command trigger (e.g., 'help' or '/help'). Leading slash is automatically handled.

        Returns:
            bool: True if successful.
        """
        clean_command = command.lstrip("/")
        return await self._request(
            "DELETE",
            f"/v1/prompts/command/{clean_command}/delete",
            model=bool,
        )
