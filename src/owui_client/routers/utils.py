from typing import Dict
from owui_client.client_base import ResourceBase
from owui_client.models.utils import CodeForm, MarkdownForm
from owui_client.models.chats import ChatTitleMessagesForm

class UtilsClient(ResourceBase):
    async def get_gravatar(self, email: str) -> str:
        return await self._request("GET", "/v1/utils/gravatar", params={"email": email})

    async def format_code(self, form_data: CodeForm) -> Dict[str, str]:
        return await self._request("POST", "/v1/utils/code/format", json=form_data.model_dump())

    async def execute_code(self, form_data: CodeForm) -> Dict:
        return await self._request("POST", "/v1/utils/code/execute", json=form_data.model_dump())

    async def get_html_from_markdown(self, form_data: MarkdownForm) -> Dict[str, str]:
        return await self._request("POST", "/v1/utils/markdown", json=form_data.model_dump())

    async def download_chat_as_pdf(self, form_data: ChatTitleMessagesForm) -> bytes:
        return await self._request("POST", "/v1/utils/pdf", model=bytes, json=form_data.model_dump())

    async def download_db(self) -> bytes:
        return await self._request("GET", "/v1/utils/db/download", model=bytes)

