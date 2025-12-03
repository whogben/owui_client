from typing import Optional
from owui_client.client_base import ResourceBase
from owui_client.models.prompts import PromptModel, PromptUserResponse, PromptForm


class PromptsClient(ResourceBase):
    async def get_prompts(self) -> list[PromptModel]:
        return await self._request(
            "GET", "/v1/prompts/", model=list[PromptModel]
        )

    async def get_prompt_list(self) -> list[PromptUserResponse]:
        return await self._request(
            "GET", "/v1/prompts/list", model=list[PromptUserResponse]
        )

    async def create_new_prompt(self, form_data: PromptForm) -> Optional[PromptModel]:
        return await self._request(
            "POST",
            "/v1/prompts/create",
            json=form_data.model_dump(),
            model=Optional[PromptModel],
        )

    async def get_prompt_by_command(self, command: str) -> Optional[PromptModel]:
        clean_command = command.lstrip("/")
        return await self._request(
            "GET",
            f"/v1/prompts/command/{clean_command}",
            model=Optional[PromptModel],
        )

    async def update_prompt_by_command(
        self, command: str, form_data: PromptForm
    ) -> Optional[PromptModel]:
        clean_command = command.lstrip("/")
        return await self._request(
            "POST",
            f"/v1/prompts/command/{clean_command}/update",
            json=form_data.model_dump(),
            model=Optional[PromptModel],
        )

    async def delete_prompt_by_command(self, command: str) -> bool:
        clean_command = command.lstrip("/")
        return await self._request(
            "DELETE",
            f"/v1/prompts/command/{clean_command}/delete",
            model=bool,
        )

