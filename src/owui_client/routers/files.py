import json
from typing import Optional, Union
from owui_client.client_base import ResourceBase
from owui_client.models.files import FileModel, FileModelResponse, FileListResponse, ContentForm, FileRenameForm


"""
Client for the Files endpoints.
"""


class FilesClient(ResourceBase):
    """
    Client for managing files, including upload, download, and metadata operations.
    """

    async def upload_file(
        self,
        file: Union[bytes, tuple],
        metadata: Optional[dict | str] = None,
        process: bool = True,
        process_in_background: bool = True,
    ) -> FileModelResponse:
        """
        Upload a file to the system.

        Args:
            file: The file to upload. Can be:
                - bytes: Raw file content. Filename will be auto-generated or missing.
                - tuple: (filename, file_content, [content_type]). e.g., ('report.pdf', b'...', 'application/pdf').
            metadata: Optional metadata dict or JSON string to attach to the file.
            process: If True, the system will attempt to extract text/content from the file immediately.
            process_in_background: If True, processing happens asynchronously. If False, waits for processing (slower).

        Returns:
            `FileModelResponse`: The uploaded file details.
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

    async def list_files(
        self, content: bool = True, page: int = 1
    ) -> list[FileModelResponse]:
        """
        List files accessible to the current user, paginated.

        Args:
            content: If True, includes the 'content' field in the response (if available).
                     If False, the content field is stripped to reduce payload size.
            page: Page number (1-indexed). Defaults to 1.

        Returns:
            list[FileModelResponse]: A list of file objects for the requested page.
        """
        result = await self._request(
            "GET",
            "/v1/files/",
            model=FileListResponse,
            params={"content": content, "page": page},
        )
        return result.items

    async def search_files(
        self, filename: str, content: bool = True
    ) -> list[FileModelResponse]:
        """
        Search for files by filename.

        Args:
            filename: Filename pattern to search for. Supports wildcards such as '*.txt'.
            content: If True, includes the 'content' field in the response.

        Returns:
            list[FileModelResponse]: A list of matching files.
        """
        return await self._request(
            "GET",
            "/v1/files/search",
            model=FileModelResponse,
            params={"filename": filename, "content": content},
        )

    async def delete_all_files(self) -> dict:
        """
        Delete ALL files in the system.

        Requires Admin privileges.

        Returns:
            dict: Success message.
        """
        return await self._request("DELETE", "/v1/files/all")

    async def get_file_by_id(self, id: str) -> Optional[FileModel]:
        """
        Get detailed information about a specific file.

        Args:
            id: The UUID of the file.

        Returns:
            Optional[FileModel]: The file details if found, None otherwise.
        """
        return await self._request("GET", f"/v1/files/{id}", model=Optional[FileModel])

    async def delete_file_by_id(self, id: str) -> dict:
        """
        Delete a specific file.

        Args:
            id: The UUID of the file to delete.

        Returns:
            dict: Success message.
        """
        return await self._request("DELETE", f"/v1/files/{id}")

    async def get_file_process_status(self, id: str, stream: bool = False) -> dict:
        """
        Get the processing status of a file.

        Args:
            id: The UUID of the file.
            stream: If True, returns an SSE stream (not fully supported).
                    Use False for a one-time status check.

        Returns:
            dict: The status object (e.g. {"status": "completed"}).
        """
        return await self._request(
            "GET",
            f"/v1/files/{id}/process/status",
            params={"stream": stream},
        )

    async def get_file_data_content_by_id(self, id: str) -> dict:
        """
        Get the extracted text content of a file.

        Args:
            id: The UUID of the file.

        Returns:
            dict: Wrapper containing the content, e.g. {"content": "Extracted text..."}.
        """
        return await self._request("GET", f"/v1/files/{id}/data/content")

    async def update_file_data_content_by_id(
        self, id: str, content: str
    ) -> dict:
        """
        Update the extracted text content of a file manually.

        Args:
            id: The UUID of the file.
            content: The new text content.

        Returns:
            dict: The updated content wrapper.
        """
        return await self._request(
            "POST",
            f"/v1/files/{id}/data/content/update",
            json={"content": content},
        )

    async def get_file_content_by_id(
        self, id: str, attachment: bool = False
    ) -> bytes:
        """
        Download the raw file content.

        Args:
            id: The UUID of the file.
            attachment: If True, sets Content-Disposition to attachment.

        Returns:
            bytes: The raw file content.
        """
        return await self._request(
            "GET", f"/v1/files/{id}/content", model=bytes, params={"attachment": attachment}
        )

    async def get_html_file_content_by_id(self, id: str) -> bytes:
        """
        Get the file content to be served as HTML.

        Restricted to files owned by an Admin user.

        Args:
            id: The UUID of the file.

        Returns:
            bytes: The file content.
        """
        return await self._request("GET", f"/v1/files/{id}/content/html", model=bytes)

    async def rename_file_by_id(self, id: str, filename: str) -> Optional[FileModel]:
        """
        Rename a file.

        Updates the filename of an existing file. The caller must be the file owner,
        an admin, or have write access to the file's containing knowledge base.

        Args:
            id: The UUID of the file to rename.
            filename: The new filename to assign to the file.

        Returns:
            Optional[FileModel]: The updated file details, or None if the rename failed.
        """
        return await self._request(
            "POST",
            f"/v1/files/{id}/rename",
            model=Optional[FileModel],
            json=FileRenameForm(filename=filename).model_dump(),
        )

