"""
Client for the Ollama endpoints.
"""
from urllib.parse import urljoin

from typing import Optional, Dict, Any, List, Union
from pathlib import Path
from owui_client.client_base import ResourceBase
from owui_client.models.ollama import (
    OllamaConfigForm,
    ModelNameForm,
    PushModelForm,
    CreateModelForm,
    CopyModelForm,
    GenerateEmbedForm,
    GenerateEmbeddingsForm,
    GenerateCompletionForm,
    GenerateChatCompletionForm,
    ConnectionVerificationForm,
    UrlForm,
)


class OllamaClient(ResourceBase):
    """
    Client for the Ollama endpoints.

    This client handles interaction with the Ollama service managed by Open WebUI,
    including model management (pull, push, create, delete), text generation (chat, completion),
    and configuration.
    """

    def _get_url(self, path: str) -> str:
        # Ollama router is mounted at root /ollama, not /api/ollama
        # We need to construct the URL relative to the root, not base_url (which includes /api)
        base = str(self._client._client.base_url)
        if base.endswith("/api/"):
            base = base[:-5]
        elif base.endswith("/api"):
            base = base[:-4]

        if not base.endswith("/"):
            base += "/"

        if path.startswith("/"):
            path = path[1:]

        return urljoin(base, path)

    async def get_status(self) -> Dict[str, bool]:
        """
        Check the status of the Ollama service.
        
        Matches GET /ollama/
        
        Returns:
            Dict containing status (e.g. {"status": True})
        """
        # Matches GET / and HEAD /
        # Using /ollama/ to match drift script heuristic
        return await self._request("GET", self._get_url("/ollama/"))

    async def head_status(self) -> bool:
        """
        Check the status of the Ollama service using HEAD request.
        
        Returns:
            True if service is reachable.
        """
        # Explicitly for HEAD / endpoint
        await self._request("HEAD", self._get_url("/ollama/"))
        return True

    async def verify_connection(self, form: ConnectionVerificationForm) -> Any:
        """
        Verify connection to an external Ollama instance.
        
        Args:
            form: Configuration containing URL and optional key.
            
        Returns:
            Response data from the verification endpoint (usually version info).
        """
        return await self._request(
            "POST", self._get_url("ollama/verify"), json=form.model_dump()
        )

    async def get_config(self) -> Dict[str, Any]:
        """
        Get the current global Ollama configuration.
        
        Returns:
            Dict containing ENABLE_OLLAMA_API, OLLAMA_BASE_URLS, OLLAMA_API_CONFIGS.
        """
        return await self._request("GET", self._get_url("ollama/config"))

    async def update_config(self, form: OllamaConfigForm) -> Dict[str, Any]:
        """
        Update the global Ollama configuration.
        
        Args:
            form: New configuration settings.
            
        Returns:
            Updated configuration dictionary.
        """
        return await self._request(
            "POST", self._get_url("ollama/config/update"), json=form.model_dump()
        )

    async def get_models(self, url_idx: int = None) -> Dict[str, Any]:
        """
        List available models.
        
        Args:
            url_idx: Optional index of the Ollama server to query. If None, queries all.
            
        Returns:
            Dict containing list of models.
        """
        path = "ollama/api/tags"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request("GET", self._get_url(path))

    async def get_loaded_models(self) -> Dict[str, Any]:
        """
        List models currently loaded in memory (ps).
        
        Returns:
            Dict containing list of loaded models and their details.
        """
        return await self._request("GET", self._get_url("ollama/api/ps"))

    async def get_version(self, url_idx: int = None) -> Dict[str, Any]:
        """
        Get the Ollama version.
        
        Args:
            url_idx: Optional index of the Ollama server to query.
            
        Returns:
            Dict containing version string.
        """
        path = "ollama/api/version"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request("GET", self._get_url(path))

    async def unload_model(self, form: ModelNameForm) -> Any:
        """
        Unload a model from memory.
        
        Args:
            form: Form containing the model name.
            
        Returns:
            Status of operation.
        """
        return await self._request(
            "POST",
            self._get_url("ollama/api/unload"),
            json=form.model_dump(exclude_none=True),
        )

    async def pull_model(self, form: ModelNameForm, url_idx: int = 0) -> str:
        """
        Pull a model from the registry.
        
        Note: This endpoint streams responses (NDJSON) by default. The client will wait
        for the operation to complete and return the full NDJSON response as a string.
        
        Args:
            form: Form containing the model name.
            url_idx: Index of the Ollama server to use (default 0).
            
        Returns:
            The full NDJSON response string.
        """
        path = f"ollama/api/pull/{url_idx}"
        # Note: This endpoint streams responses (NDJSON) by default.
        return await self._request(
            "POST", self._get_url(path), json=form.model_dump(exclude_none=True)
        )

    async def push_model(self, form: PushModelForm, url_idx: int = None) -> str:
        """
        Push a model to the registry.
        
        Note: This endpoint streams responses (NDJSON) by default. The client will wait
        for the operation to complete and return the full NDJSON response as a string.
        
        Args:
            form: Form containing model name and options.
            url_idx: Optional index of the Ollama server.
            
        Returns:
            The full NDJSON response string.
        """
        path = "ollama/api/push"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request(
            "DELETE", self._get_url(path), json=form.model_dump(exclude_none=True)
        )

    async def create_model(self, form: CreateModelForm, url_idx: int = 0) -> str:
        """
        Create a model from a Modelfile.
        
        Note: This endpoint streams responses (NDJSON) by default. The client will wait
        for the operation to complete and return the full NDJSON response as a string.
        
        Args:
            form: Form containing model name and creation options.
            url_idx: Index of the Ollama server (default 0).
            
        Returns:
            The full NDJSON response string.
        """
        path = f"ollama/api/create/{url_idx}"
        return await self._request(
            "POST", self._get_url(path), json=form.model_dump(exclude_none=True)
        )

    async def copy_model(self, form: CopyModelForm, url_idx: int = None) -> Any:
        """
        Copy a model.
        
        Args:
            form: Form containing source and destination names.
            url_idx: Optional index of the Ollama server.
            
        Returns:
            True if successful.
        """
        path = "ollama/api/copy"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request(
            "POST", self._get_url(path), json=form.model_dump(exclude_none=True)
        )

    async def delete_model(self, form: ModelNameForm, url_idx: int = None) -> Any:
        """
        Delete a model.
        
        Args:
            form: Form containing the model name.
            url_idx: Optional index of the Ollama server.
            
        Returns:
            True if successful.
        """
        path = "ollama/api/delete"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request(
            "DELETE", self._get_url(path), json=form.model_dump(exclude_none=True)
        )

    async def show_model(self, form: ModelNameForm) -> Dict[str, Any]:
        """
        Show information about a model.
        
        Args:
            form: Form containing the model name.
            
        Returns:
            Dict containing model details (modelfile, parameters, etc.).
        """
        return await self._request(
            "POST",
            self._get_url("ollama/api/show"),
            json=form.model_dump(exclude_none=True),
        )

    async def embed(self, form: GenerateEmbedForm, url_idx: int = None) -> Dict[str, Any]:
        """
        Generate embeddings for the given input (new endpoint).
        
        Args:
            form: Form containing model and input.
            url_idx: Optional index of the Ollama server.
            
        Returns:
            Response containing embeddings.
        """
        path = "ollama/api/embed"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request(
            "POST", self._get_url(path), json=form.model_dump(exclude_none=True)
        )

    async def embeddings(self, form: GenerateEmbeddingsForm, url_idx: int = None) -> Dict[str, Any]:
        """
        Generate embeddings for the given prompt (legacy endpoint).
        
        Args:
            form: Form containing model and prompt.
            url_idx: Optional index of the Ollama server.
            
        Returns:
            Response containing embeddings.
        """
        path = "ollama/api/embeddings"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request(
            "POST", self._get_url(path), json=form.model_dump(exclude_none=True)
        )

    async def generate(self, form: GenerateCompletionForm, url_idx: int = None) -> Union[Dict[str, Any], str]:
        """
        Generate a completion for the given prompt.
        
        If `stream=True` (default), the client waits for the full NDJSON response and returns it as a string.
        If `stream=False`, returns a Dict containing the completion.
        
        Args:
            form: Form containing model, prompt, and options.
            url_idx: Optional index of the Ollama server.
            
        Returns:
            Dict or NDJSON string depending on `stream` parameter.
        """
        path = "ollama/api/generate"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request(
            "POST", self._get_url(path), json=form.model_dump(exclude_none=True)
        )

    async def chat(self, form: GenerateChatCompletionForm, url_idx: int = None) -> Union[Dict[str, Any], str]:
        """
        Generate a chat completion.
        
        If `stream=True` (default), the client waits for the full NDJSON response and returns it as a string.
        If `stream=False`, returns a Dict containing the completion.
        
        Args:
            form: Form containing model, messages, and options.
            url_idx: Optional index of the Ollama server.
            
        Returns:
            Dict or NDJSON string depending on `stream` parameter.
        """
        path = "ollama/api/chat"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request(
            "POST", self._get_url(path), json=form.model_dump(exclude_none=True)
        )

    async def generate_openai_completion(self, payload: Dict, url_idx: int = None) -> Dict[str, Any]:
        """
        Generate completion using OpenAI-compatible endpoint.
        
        Args:
            payload: OpenAI completion request payload.
            url_idx: Optional index of the Ollama server.
            
        Returns:
            OpenAI-compatible completion response.
        """
        path = "ollama/v1/completions"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request(
            "POST", self._get_url(path), json=payload
        )

    async def generate_openai_chat_completion(self, payload: Dict, url_idx: int = None) -> Dict[str, Any]:
        """
        Generate chat completion using OpenAI-compatible endpoint.
        
        Args:
            payload: OpenAI chat completion request payload.
            url_idx: Optional index of the Ollama server.
            
        Returns:
            OpenAI-compatible chat completion response.
        """
        path = "ollama/v1/chat/completions"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request(
            "POST", self._get_url(path), json=payload
        )

    async def get_openai_models(self, url_idx: int = None) -> Dict[str, Any]:
        """
        List models using OpenAI-compatible endpoint.
        
        Args:
            url_idx: Optional index of the Ollama server.
            
        Returns:
            OpenAI-compatible model list.
        """
        path = "ollama/v1/models"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request("GET", self._get_url(path))

    async def download_model(self, form: UrlForm, url_idx: int = None) -> str:
        """
        Download a model from a URL (e.g. Hugging Face).
        
        Note: The backend returns a Server-Sent Events (SSE) stream of progress updates.
        The client waits for completion and returns the full SSE text.
        
        Args:
            form: Form containing the URL.
            url_idx: Optional index of the Ollama server.
            
        Returns:
            The full SSE response string.
        """
        path = "ollama/models/download"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        # This endpoint returns a streaming response
        return await self._request(
            "POST", self._get_url(path), json=form.model_dump()
        )

    async def upload_model(self, file_path: Union[str, Path], url_idx: int = None) -> str:
        """
        Upload a model file to the server.
        
        Note: The backend returns a Server-Sent Events (SSE) stream of progress updates.
        The client waits for completion and returns the full SSE text.
        
        Args:
            file_path: Local path to the file to upload.
            url_idx: Optional index of the Ollama server.
            
        Returns:
            The full SSE response string.
            
        Raises:
            FileNotFoundError: If the file does not exist.
        """
        path = "ollama/models/upload"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "rb") as f:
            content = f.read()
            
        files = {"file": (file_path.name, content)}
        return await self._request("POST", self._get_url(path), files=files)
