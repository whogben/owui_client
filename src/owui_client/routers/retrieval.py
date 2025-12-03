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
    async def get_status(self) -> Dict:
        return await self._request("GET", "/v1/retrieval/")

    async def get_embedding_config(self) -> Dict:
        return await self._request("GET", "/v1/retrieval/embedding")

    async def update_embedding_config(self, form_data: EmbeddingModelUpdateForm) -> Dict:
        return await self._request("POST", "/v1/retrieval/embedding/update", json=form_data.model_dump())

    async def update_config(self, form_data: ConfigForm) -> Dict:
        return await self._request("POST", "/v1/retrieval/config/update", json=form_data.model_dump())

    async def process_file(self, form_data: ProcessFileForm) -> Dict:
        return await self._request("POST", "/v1/retrieval/process/file", json=form_data.model_dump())

    async def process_text(self, form_data: ProcessTextForm) -> Dict:
        return await self._request("POST", "/v1/retrieval/process/text", json=form_data.model_dump())

    async def process_web(self, form_data: ProcessUrlForm) -> Dict:
        return await self._request("POST", "/v1/retrieval/process/web", json=form_data.model_dump())
    
    async def process_youtube(self, form_data: ProcessUrlForm) -> Dict:
        return await self._request("POST", "/v1/retrieval/process/youtube", json=form_data.model_dump())

    async def process_web_search(self, form_data: SearchForm) -> Dict:
        return await self._request("POST", "/v1/retrieval/process/web/search", json=form_data.model_dump())

    async def query_doc(self, form_data: QueryDocForm) -> Dict:
        return await self._request("POST", "/v1/retrieval/query/doc", json=form_data.model_dump())

    async def query_collection(self, form_data: QueryCollectionsForm) -> Dict:
        return await self._request("POST", "/v1/retrieval/query/collection", json=form_data.model_dump())

    async def delete(self, form_data: DeleteForm) -> Dict:
        return await self._request("POST", "/v1/retrieval/delete", json=form_data.model_dump())

    async def reset_db(self) -> None:
        await self._request("POST", "/v1/retrieval/reset/db")

    async def reset_uploads(self) -> bool:
        return await self._request("POST", "/v1/retrieval/reset/uploads")

    async def process_files_batch(self, form_data: BatchProcessFilesForm) -> BatchProcessFilesResponse:
        response = await self._request("POST", "/v1/retrieval/process/files/batch", json=form_data.model_dump())
        return BatchProcessFilesResponse(**response)

    async def get_embeddings(self, text: str = "Hello World!") -> Dict:
        return await self._request("GET", f"/v1/retrieval/ef/{text}")
