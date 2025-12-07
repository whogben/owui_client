from typing import Dict, List, Optional
from owui_client.client_base import ResourceBase
from owui_client.models.retrieval import (
    EmbeddingModelUpdateForm,
    ConfigForm,
    ProcessFileForm,
    ProcessTextForm,
    ProcessUrlForm,
    QueryDocForm,
    QueryCollectionsForm,
    DeleteForm,
    BatchProcessFilesForm,
    BatchProcessFilesResponse,
    SearchForm,
)

class RetrievalClient(ResourceBase):
    """
    Client for the Retrieval endpoints.
    """

    async def get_status(self) -> Dict:
        """
        Get the status of the retrieval system.

        Returns:
            Dict containing the status and configuration details.
        """
        return await self._request("GET", "/v1/retrieval/")

    async def get_embedding_config(self) -> Dict:
        """
        Get the current embedding configuration.

        Returns:
            Dict containing the embedding configuration.
        """
        return await self._request("GET", "/v1/retrieval/embedding")

    async def update_embedding_config(self, form_data: EmbeddingModelUpdateForm) -> Dict:
        """
        Update the embedding model configuration.

        Args:
            form_data: The configuration updates.

        Returns:
            Dict containing the updated configuration.
        """
        return await self._request("POST", "/v1/retrieval/embedding/update", json=form_data.model_dump())

    async def update_config(self, form_data: ConfigForm) -> Dict:
        """
        Update the retrieval configuration.

        Args:
            form_data: The configuration updates.

        Returns:
            Dict containing the updated configuration.
        """
        return await self._request("POST", "/v1/retrieval/config/update", json=form_data.model_dump())

    async def process_file(self, form_data: ProcessFileForm) -> Dict:
        """
        Process a file for retrieval.

        Args:
            form_data: The file processing data.

        Returns:
            Dict containing the processing result.
        """
        return await self._request("POST", "/v1/retrieval/process/file", json=form_data.model_dump())

    async def process_text(self, form_data: ProcessTextForm) -> Dict:
        """
        Process text for retrieval.

        Args:
            form_data: The text processing data.

        Returns:
            Dict containing the processing result.
        """
        return await self._request("POST", "/v1/retrieval/process/text", json=form_data.model_dump())

    async def process_web(self, form_data: ProcessUrlForm) -> Dict:
        """
        Process a web URL for retrieval.

        Args:
            form_data: The URL processing data.

        Returns:
            Dict containing the processing result.
        """
        return await self._request("POST", "/v1/retrieval/process/web", json=form_data.model_dump())
    
    async def process_youtube(self, form_data: ProcessUrlForm) -> Dict:
        """
        Process a YouTube URL for retrieval.

        Args:
            form_data: The YouTube URL processing data.

        Returns:
            Dict containing the processing result.
        """
        return await self._request("POST", "/v1/retrieval/process/youtube", json=form_data.model_dump())

    async def process_web_search(self, form_data: SearchForm) -> Dict:
        """
        Process a web search for retrieval.

        Args:
            form_data: The search query data.

        Returns:
            Dict containing the search results.
        """
        return await self._request("POST", "/v1/retrieval/process/web/search", json=form_data.model_dump())

    async def query_doc(self, form_data: QueryDocForm) -> Dict:
        """
        Query a document in a collection.

        Args:
            form_data: The query data.

        Returns:
            Dict containing the query results.
        """
        return await self._request("POST", "/v1/retrieval/query/doc", json=form_data.model_dump())

    async def query_collection(self, form_data: QueryCollectionsForm) -> Dict:
        """
        Query multiple collections.

        Args:
            form_data: The query data.

        Returns:
            Dict containing the query results.
        """
        return await self._request("POST", "/v1/retrieval/query/collection", json=form_data.model_dump())

    async def delete(self, form_data: DeleteForm) -> bool:
        """
        Delete a file from a collection.

        Args:
            form_data: The delete request data.

        Returns:
            bool: True if successful.
        """
        return await self._request("POST", "/v1/retrieval/delete", json=form_data.model_dump())

    async def reset_db(self) -> bool:
        """
        Reset the retrieval database.

        Returns:
            bool: True if successful.
        """
        return await self._request("POST", "/v1/retrieval/reset/db")

    async def reset_uploads(self) -> bool:
        """
        Reset the uploaded files.

        Returns:
            bool: True if successful.
        """
        return await self._request("POST", "/v1/retrieval/reset/uploads")

    async def process_files_batch(self, form_data: BatchProcessFilesForm) -> BatchProcessFilesResponse:
        """
        Process a batch of files for retrieval.

        Args:
            form_data: The batch processing data.

        Returns:
            BatchProcessFilesResponse containing the results.
        """
        response = await self._request("POST", "/v1/retrieval/process/files/batch", json=form_data.model_dump())
        return BatchProcessFilesResponse(**response)

    async def get_embeddings(self, text: str = "Hello World!") -> Dict:
        """
        Get embeddings for a given text.

        Args:
            text: The text to get embeddings for.

        Returns:
            Dict containing the embeddings.
        """
        return await self._request("GET", f"/v1/retrieval/ef/{text}")
