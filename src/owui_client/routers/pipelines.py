import os
from typing import Optional
from owui_client.client_base import ResourceBase
from owui_client.models.pipelines import AddPipelineForm, DeletePipelineForm

class PipelinesClient(ResourceBase):
    """
    Client for the Pipelines endpoints.

    Pipelines allow extending Open WebUI's functionality using Python scripts
    that can intercept and modify requests/responses (filters) or add new capabilities (pipes).
    """
    async def list(self) -> dict:
        """
        Get the list of configured pipeline servers.

        This returns the available OpenAI API base URLs that are configured and capable of hosting pipelines.

        Returns:
            dict: A dictionary containing a list of pipeline server configurations.
            Example:
            ```json
            {
                "data": [
                    {
                        "url": "http://localhost:9099",
                        "idx": 0
                    }
                ]
            }
            ```
        """
        return await self._request("GET", "/v1/pipelines/list")

    async def upload(self, file_path: str, url_idx: int) -> dict:
        """
        Upload a pipeline file (.py) to a specific pipeline server.

        Args:
            file_path: The local path to the Python file to upload.
            url_idx: The index of the pipeline server to upload to (from `list()`).

        Returns:
            dict: The response from the pipeline server, typically containing details of the uploaded pipeline.
        """
        filename = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            files = {"file": (filename, f)}
            data = {"urlIdx": str(url_idx)}
            return await self._request("POST", "/v1/pipelines/upload", data=data, files=files)

    async def add(self, form: AddPipelineForm) -> dict:
        """
        Add a pipeline by instructing the server to download it from a URL.

        Args:
            form: The form data containing the pipeline URL and server index.

        Returns:
            dict: The response from the pipeline server, typically containing details of the added pipeline.
        """
        return await self._request("POST", "/v1/pipelines/add", json=form.model_dump())

    async def delete(self, form: DeletePipelineForm) -> dict:
        """
        Delete a pipeline from a pipeline server.

        Args:
            form: The form data containing the pipeline ID and server index.

        Returns:
            dict: The response from the pipeline server confirming deletion.
        """
        return await self._request("DELETE", "/v1/pipelines/delete", json=form.model_dump())

    async def get(self, url_idx: Optional[int] = None) -> dict:
        """
        Get the list of installed pipelines from a specific pipeline server.

        Args:
            url_idx: The index of the pipeline server to query.

        Returns:
            dict: A dictionary containing the list of installed pipelines on that server.
        """
        params = {}
        if url_idx is not None:
            params["urlIdx"] = url_idx
        return await self._request("GET", "/v1/pipelines/", params=params)

    async def get_valves(self, pipeline_id: str, url_idx: Optional[int] = None) -> dict:
        """
        Get the current valve values (configuration) for a specific pipeline.

        Valves allow users to configure pipeline behavior (e.g., API keys, toggles).

        Args:
            pipeline_id: The ID of the pipeline.
            url_idx: The index of the pipeline server where the pipeline resides.

        Returns:
            dict: A dictionary of valve keys and their current values.
        """
        params = {}
        if url_idx is not None:
            params["urlIdx"] = url_idx
        return await self._request("GET", f"/v1/pipelines/{pipeline_id}/valves", params=params)

    async def get_valves_spec(self, pipeline_id: str, url_idx: Optional[int] = None) -> dict:
        """
        Get the specification of valves for a specific pipeline.

        This includes details like variable names, types, and descriptions, which can be used to generate a configuration UI.

        Args:
            pipeline_id: The ID of the pipeline.
            url_idx: The index of the pipeline server where the pipeline resides.

        Returns:
            dict: The JSON schema or specification of the pipeline's valves.
        """
        params = {}
        if url_idx is not None:
            params["urlIdx"] = url_idx
        return await self._request("GET", f"/v1/pipelines/{pipeline_id}/valves/spec", params=params)

    async def update_valves(self, pipeline_id: str, form_data: dict, url_idx: Optional[int] = None) -> dict:
        """
        Update the valve values for a specific pipeline.

        Args:
            pipeline_id: The ID of the pipeline.
            form_data: A dictionary containing the new values for the valves.
            url_idx: The index of the pipeline server where the pipeline resides.

        Returns:
            dict: The updated valve configuration or confirmation from the server.
        """
        params = {}
        if url_idx is not None:
            params["urlIdx"] = url_idx
        return await self._request("POST", f"/v1/pipelines/{pipeline_id}/valves/update", params=params, json=form_data)

