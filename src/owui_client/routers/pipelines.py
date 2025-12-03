import os
from typing import Optional
from owui_client.client_base import ResourceBase
from owui_client.models.pipelines import AddPipelineForm, DeletePipelineForm

class PipelinesClient(ResourceBase):
    async def list(self) -> dict:
        """
        Get list of pipelines.
        """
        return await self._request("GET", "/v1/pipelines/list")

    async def upload(self, file_path: str, url_idx: int) -> dict:
        """
        Upload a pipeline file.
        """
        filename = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            files = {"file": (filename, f)}
            data = {"urlIdx": str(url_idx)}
            return await self._request("POST", "/v1/pipelines/upload", data=data, files=files)

    async def add(self, form: AddPipelineForm) -> dict:
        """
        Add a pipeline via URL.
        """
        return await self._request("POST", "/v1/pipelines/add", json=form.model_dump())

    async def delete(self, form: DeletePipelineForm) -> dict:
        """
        Delete a pipeline.
        """
        return await self._request("DELETE", "/v1/pipelines/delete", json=form.model_dump())

    async def get(self, url_idx: Optional[int] = None) -> dict:
        """
        Get pipelines from a specific URL index.
        """
        params = {}
        if url_idx is not None:
            params["urlIdx"] = url_idx
        return await self._request("GET", "/v1/pipelines/", params=params)

    async def get_valves(self, pipeline_id: str, url_idx: Optional[int] = None) -> dict:
        """
        Get valves for a pipeline.
        """
        params = {}
        if url_idx is not None:
            params["urlIdx"] = url_idx
        return await self._request("GET", f"/v1/pipelines/{pipeline_id}/valves", params=params)

    async def get_valves_spec(self, pipeline_id: str, url_idx: Optional[int] = None) -> dict:
        """
        Get valves spec for a pipeline.
        """
        params = {}
        if url_idx is not None:
            params["urlIdx"] = url_idx
        return await self._request("GET", f"/v1/pipelines/{pipeline_id}/valves/spec", params=params)

    async def update_valves(self, pipeline_id: str, form_data: dict, url_idx: Optional[int] = None) -> dict:
        """
        Update valves for a pipeline.
        """
        params = {}
        if url_idx is not None:
            params["urlIdx"] = url_idx
        return await self._request("POST", f"/v1/pipelines/{pipeline_id}/valves/update", params=params, json=form_data)

