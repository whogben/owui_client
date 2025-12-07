"""
Client for the Utils endpoints.
"""
from typing import Dict
from owui_client.client_base import ResourceBase
from owui_client.models.utils import CodeForm, MarkdownForm
from owui_client.models.chats import ChatTitleMessagesForm

class UtilsClient(ResourceBase):
    """
    Client for utility operations such as Gravatar, code formatting/execution, markdown conversion, and database downloads.
    """
    async def get_gravatar(self, email: str) -> str:
        """
        Get the Gravatar URL for a given email address.

        Args:
            email: The email address to retrieve the Gravatar URL for.

        Returns:
            The URL of the Gravatar image.
        """
        return await self._request("GET", "/v1/utils/gravatar", params={"email": email})

    async def format_code(self, form_data: CodeForm) -> Dict[str, str]:
        """
        Format the provided code using Black (Python formatter).

        Args:
            form_data: The `CodeForm` containing the code to format.

        Returns:
            A dictionary containing the formatted code under the "code" key.
        """
        return await self._request("POST", "/v1/utils/code/format", json=form_data.model_dump())

    async def execute_code(self, form_data: CodeForm) -> Dict:
        """
        Execute the provided code using a Jupyter kernel.

        Note: Code execution must be enabled and configured (e.g., Jupyter URL) on the server.

        Args:
            form_data: The `CodeForm` containing the code to execute.

        Returns:
            The output of the code execution from Jupyter.

        Raises:
            HTTPException: If the code execution engine is not supported or configured.
        """
        return await self._request("POST", "/v1/utils/code/execute", json=form_data.model_dump())

    async def get_html_from_markdown(self, form_data: MarkdownForm) -> Dict[str, str]:
        """
        Convert Markdown content to HTML.

        Args:
            form_data: The `MarkdownForm` containing the markdown content.

        Returns:
            A dictionary containing the generated HTML under the "html" key.
        """
        return await self._request("POST", "/v1/utils/markdown", json=form_data.model_dump())

    async def download_chat_as_pdf(self, form_data: ChatTitleMessagesForm) -> bytes:
        """
        Generate and download a PDF version of a chat.

        Args:
            form_data: The `ChatTitleMessagesForm` containing chat title and messages.

        Returns:
            The PDF file content as bytes.
        """
        return await self._request("POST", "/v1/utils/pdf", model=bytes, json=form_data.model_dump())

    async def download_db(self) -> bytes:
        """
        Download the database file.

        Note: Requires admin privileges and `ENABLE_ADMIN_EXPORT` must be True.
        Only supported for SQLite databases.

        Returns:
            The database file content as bytes.

        Raises:
            HTTPException: If access is prohibited or the database is not SQLite.
        """
        return await self._request("GET", "/v1/utils/db/download", model=bytes)

