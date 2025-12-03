import json
from typing import Optional, Union
from owui_client.client_base import ResourceBase
from owui_client.models.files import FileModel, FileModelResponse, ContentForm


class FilesClient(ResourceBase):
    async def upload_file(
        self,
        file: Union[bytes, tuple],
        metadata: Optional[dict | str] = None,
        process: bool = True,
        process_in_background: bool = True,
    ) -> FileModelResponse:
        """
        Upload a file.

        Args:
            file: The file to upload. Can be bytes or a tuple (filename, file_content, content_type).
            metadata: Optional metadata for the file.
            process: Whether to process the file (e.g. extract text).
            process_in_background: Whether to process in background.
        """
        files = {"file": file}
        data = {}
        if metadata:
            if isinstance(metadata, dict):
                data["metadata"] = json.dumps(metadata)
            else:
                data["metadata"] = metadata

        params = {
            "process": process,
            "process_in_background": process_in_background,
        }

        return await self._request(
            "POST",
            "/v1/files/",
            model=FileModelResponse,
            files=files,
            data=data,
            params=params,
        )

    async def list_files(self, content: bool = True) -> list[FileModelResponse]:
        return await self._request(
            "GET", "/v1/files/", model=FileModelResponse, params={"content": content}
        )

    async def search_files(
        self, filename: str, content: bool = True
    ) -> list[FileModelResponse]:
        return await self._request(
            "GET",
            "/v1/files/search",
            model=FileModelResponse,
            params={"filename": filename, "content": content},
        )

    async def delete_all_files(self) -> dict:
        return await self._request("DELETE", "/v1/files/all")

    async def get_file_by_id(self, id: str) -> Optional[FileModel]:
        return await self._request("GET", f"/v1/files/{id}", model=Optional[FileModel])

    async def delete_file_by_id(self, id: str) -> dict:
        return await self._request("DELETE", f"/v1/files/{id}")

    async def get_file_process_status(self, id: str, stream: bool = False) -> dict:
        """
        Get file process status.
        Note: stream=True is not fully supported by the client helper yet (no SSE parsing).
        """
        return await self._request(
            "GET",
            f"/v1/files/{id}/process/status",
            params={"stream": stream},
        )

    async def get_file_data_content_by_id(self, id: str) -> dict:
        return await self._request("GET", f"/v1/files/{id}/data/content")

    async def update_file_data_content_by_id(
        self, id: str, content: str
    ) -> dict:
        return await self._request(
            "POST",
            f"/v1/files/{id}/data/content/update",
            json={"content": content},
        )

    async def get_file_content_by_id(
        self, id: str, attachment: bool = False
    ) -> bytes:
        return await self._request(
            "GET", f"/v1/files/{id}/content", model=bytes, params={"attachment": attachment}
        )

    async def get_html_file_content_by_id(self, id: str) -> bytes:
        return await self._request("GET", f"/v1/files/{id}/content/html", model=bytes)

