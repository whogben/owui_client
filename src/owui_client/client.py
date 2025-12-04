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
    """

    def __init__(
        self, api_url: str = "http://127.0.0.1:8080/api", api_key: str | None = None
    ):
        super().__init__(api_url=api_url, api_key=api_key)

        self.auths = AuthsClient(self)
        self.users = UsersClient(self)
        self.configs = ConfigsClient(self)
        self.notes = NotesClient(self)
        self.groups = GroupsClient(self)
        self.prompts = PromptsClient(self)
        self.files = FilesClient(self)
        self.openai = OpenAIClient(self)
        self.ollama = OllamaClient(self)
        self.pipelines = PipelinesClient(self)
        self.tasks = TasksClient(self)
        self.images = ImagesClient(self)
        self.audio = AudioClient(self)
        self.retrieval = RetrievalClient(self)
        self.channels = ChannelsClient(self)
        self.chats = ChatsClient(self)
        self.models = ModelsClient(self)
        self.knowledge = KnowledgeClient(self)
        self.tools = ToolsClient(self)
        self.memories = MemoriesClient(self)
        self.folders = FoldersClient(self)
        self.functions = FunctionsClient(self)
        self.evaluations = EvaluationsClient(self)
        self.utils = UtilsClient(self)
        self.root = RootClient(self)
        self.shortcuts = Shortcuts(self)
