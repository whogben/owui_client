"""
Main client module for the Open WebUI API.

This module provides the `OpenWebUI` class, which serves as the primary entry point
for interacting with the Open WebUI backend. It aggregates various sub-clients
(routers) to provide access to all supported API endpoints.
"""

from owui_client.client_base import OWUIClientBase
from owui_client.routers.auths import AuthsClient
from owui_client.routers.users import UsersClient
from owui_client.routers.configs import ConfigsClient
from owui_client.routers.notes import NotesClient
from owui_client.routers.groups import GroupsClient
from owui_client.routers.prompts import PromptsClient
from owui_client.routers.files import FilesClient
from owui_client.routers.openai import OpenAIClient
from owui_client.routers.ollama import OllamaClient
from owui_client.routers.pipelines import PipelinesClient
from owui_client.routers.tasks import TasksClient
from owui_client.routers.images import ImagesClient
from owui_client.routers.audio import AudioClient
from owui_client.routers.retrieval import RetrievalClient
from owui_client.routers.channels import ChannelsClient
from owui_client.routers.chats import ChatsClient
from owui_client.routers.models import ModelsClient
from owui_client.routers.knowledge import KnowledgeClient
from owui_client.routers.tools import ToolsClient
from owui_client.routers.memories import MemoriesClient
from owui_client.routers.folders import FoldersClient
from owui_client.routers.functions import FunctionsClient
from owui_client.routers.evaluations import EvaluationsClient
from owui_client.routers.utils import UtilsClient
from owui_client.routers.root import RootClient
from owui_client.shortcuts import Shortcuts


class OpenWebUI(OWUIClientBase):
    """
    Main client for the Open WebUI API.

    This class aggregates all the sub-resource clients (routers) to provide a single
    entry point for the API.

    Args:
        api_url: The base URL for the Open WebUI API. Defaults to "http://127.0.0.1:8080/api".
        api_key: The API key to be used for authentication. Defaults to None.
    """

    def __init__(
        self, api_url: str = "http://127.0.0.1:8080/api", api_key: str | None = None
    ):
        super().__init__(api_url=api_url, api_key=api_key)

        self.auths = AuthsClient(self)
        """Client for Authentication endpoints."""

        self.users = UsersClient(self)
        """Client for Users endpoints."""

        self.configs = ConfigsClient(self)
        """Client for Configs endpoints."""

        self.notes = NotesClient(self)
        """Client for Notes endpoints."""

        self.groups = GroupsClient(self)
        """Client for Groups endpoints."""

        self.prompts = PromptsClient(self)
        """Client for Prompts endpoints."""

        self.files = FilesClient(self)
        """Client for Files endpoints."""

        self.openai = OpenAIClient(self)
        """Client for OpenAI-compatible endpoints."""

        self.ollama = OllamaClient(self)
        """Client for Ollama endpoints."""

        self.pipelines = PipelinesClient(self)
        """Client for Pipelines endpoints."""

        self.tasks = TasksClient(self)
        """Client for Tasks endpoints."""

        self.images = ImagesClient(self)
        """Client for Images endpoints."""

        self.audio = AudioClient(self)
        """Client for Audio endpoints."""

        self.retrieval = RetrievalClient(self)
        """Client for Retrieval endpoints."""

        self.channels = ChannelsClient(self)
        """Client for Channels endpoints."""

        self.chats = ChatsClient(self)
        """Client for Chats endpoints."""

        self.models = ModelsClient(self)
        """Client for Models endpoints."""

        self.knowledge = KnowledgeClient(self)
        """Client for Knowledge endpoints."""

        self.tools = ToolsClient(self)
        """Client for Tools endpoints."""

        self.memories = MemoriesClient(self)
        """Client for Memories endpoints."""

        self.folders = FoldersClient(self)
        """Client for Folders endpoints."""

        self.functions = FunctionsClient(self)
        """Client for Functions endpoints."""

        self.evaluations = EvaluationsClient(self)
        """Client for Evaluations endpoints."""

        self.utils = UtilsClient(self)
        """Client for Utils endpoints."""

        self.root = RootClient(self)
        """Client for Root endpoints."""

        self.shortcuts = Shortcuts(self)
        """Helper for shortcut methods."""
