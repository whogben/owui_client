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
        # Matches GET / and HEAD /
        # Using /ollama/ to match drift script heuristic
        return await self._request("GET", self._get_url("/ollama/"))

    async def head_status(self) -> bool:
        # Explicitly for HEAD / endpoint
        await self._request("HEAD", self._get_url("/ollama/"))
        return True

    async def verify_connection(self, form: ConnectionVerificationForm) -> Any:
        return await self._request(
            "POST", self._get_url("ollama/verify"), json=form.model_dump()
        )

    async def get_config(self):
        return await self._request("GET", self._get_url("ollama/config"))

    async def update_config(self, form: OllamaConfigForm):
        return await self._request(
            "POST", self._get_url("ollama/config/update"), json=form.model_dump()
        )

    async def get_models(self, url_idx: int = None):
        path = "ollama/api/tags"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request("GET", self._get_url(path))

    async def get_loaded_models(self):
        return await self._request("GET", self._get_url("ollama/api/ps"))

    async def get_version(self, url_idx: int = None):
        path = "ollama/api/version"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request("GET", self._get_url(path))

    async def unload_model(self, form: ModelNameForm):
        return await self._request(
            "POST",
            self._get_url("ollama/api/unload"),
            json=form.model_dump(exclude_none=True),
        )

    async def pull_model(self, form: ModelNameForm, url_idx: int = 0):
        path = f"ollama/api/pull/{url_idx}"
        # Note: This endpoint streams responses (NDJSON) by default.
        return await self._request(
            "POST", self._get_url(path), json=form.model_dump(exclude_none=True)
        )

    async def push_model(self, form: PushModelForm, url_idx: int = None):
        path = "ollama/api/push"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request(
            "DELETE", self._get_url(path), json=form.model_dump(exclude_none=True)
        )

    async def create_model(self, form: CreateModelForm, url_idx: int = 0):
        path = f"ollama/api/create/{url_idx}"
        return await self._request(
            "POST", self._get_url(path), json=form.model_dump(exclude_none=True)
        )

    async def copy_model(self, form: CopyModelForm, url_idx: int = None):
        path = "ollama/api/copy"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request(
            "POST", self._get_url(path), json=form.model_dump(exclude_none=True)
        )

    async def delete_model(self, form: ModelNameForm, url_idx: int = None):
        path = "ollama/api/delete"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request(
            "DELETE", self._get_url(path), json=form.model_dump(exclude_none=True)
        )

    async def show_model(self, form: ModelNameForm):
        return await self._request(
            "POST",
            self._get_url("ollama/api/show"),
            json=form.model_dump(exclude_none=True),
        )

    async def embed(self, form: GenerateEmbedForm, url_idx: int = None):
        path = "ollama/api/embed"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request(
            "POST", self._get_url(path), json=form.model_dump(exclude_none=True)
        )

    async def embeddings(self, form: GenerateEmbeddingsForm, url_idx: int = None):
        path = "ollama/api/embeddings"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request(
            "POST", self._get_url(path), json=form.model_dump(exclude_none=True)
        )

    async def generate(self, form: GenerateCompletionForm, url_idx: int = None):
        path = "ollama/api/generate"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request(
            "POST", self._get_url(path), json=form.model_dump(exclude_none=True)
        )

    async def chat(self, form: GenerateChatCompletionForm, url_idx: int = None):
        path = "ollama/api/chat"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request(
            "POST", self._get_url(path), json=form.model_dump(exclude_none=True)
        )

    async def generate_openai_completion(self, payload: Dict, url_idx: int = None):
        path = "ollama/v1/completions"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request(
            "POST", self._get_url(path), json=payload
        )

    async def generate_openai_chat_completion(self, payload: Dict, url_idx: int = None):
        path = "ollama/v1/chat/completions"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request(
            "POST", self._get_url(path), json=payload
        )

    async def get_openai_models(self, url_idx: int = None):
        path = "ollama/v1/models"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        return await self._request("GET", self._get_url(path))

    async def download_model(self, form: UrlForm, url_idx: int = None):
        path = "ollama/models/download"
        if url_idx is not None:
            path = f"{path}/{url_idx}"
        # This endpoint returns a streaming response
        return await self._request(
            "POST", self._get_url(path), json=form.model_dump()
        )

    async def upload_model(self, file_path: Union[str, Path], url_idx: int = None):
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
