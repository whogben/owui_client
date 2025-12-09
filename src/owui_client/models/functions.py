from typing import Optional
from pydantic import BaseModel, ConfigDict, HttpUrl
from owui_client.models.users import UserModel


class FunctionMeta(BaseModel):
    """
    Metadata for a function.
    """

    description: Optional[str] = None
    """
    Description of the function.
    """

    manifest: Optional[dict] = {}
    """
    Manifest data extracted from the function's frontmatter.

    Dict Fields:
        - `version` (str, optional): Version of the function
        - `funding_url` (str, optional): URL for funding/support
        - `required_open_webui_version` (str, optional): Minimum required Open WebUI version
        - `icon_url` (str, optional): URL for function icon
    """

    model_config = ConfigDict(extra="allow")


class FunctionModel(BaseModel):
    """
    Model representing a function.
    """

    id: str
    """
    Unique identifier for the function.
    """

    user_id: str
    """
    ID of the user who owns the function.
    """

    name: str
    """
    Name of the function.
    """

    type: str
    """
    Type of the function (e.g., 'filter', 'action').
    """

    content: str
    """
    The Python source code content of the function.
    """

    meta: FunctionMeta
    """
    Metadata associated with the function.
    """

    is_active: bool = False
    """
    Whether the function is currently active.
    """

    is_global: bool = False
    """
    Whether the function is globally available.
    """

    updated_at: int
    """
    Timestamp of the last update (epoch time).
    """

    created_at: int
    """
    Timestamp of creation (epoch time).
    """

    model_config = ConfigDict(from_attributes=True)


class FunctionWithValvesModel(BaseModel):
    """
    Model representing a function including its valves configuration.
    """

    id: str
    """
    Unique identifier for the function.
    """

    user_id: str
    """
    ID of the user who owns the function.
    """

    name: str
    """
    Name of the function.
    """

    type: str
    """
    Type of the function.
    """

    content: str
    """
    The Python source code content of the function.
    """

    meta: FunctionMeta
    """
    Metadata associated with the function.
    """

    valves: Optional[dict] = None
    """
    Configuration values (valves) for the function.

    Dict Fields:
        - `priority` (int, optional): Priority level for filter operations
        - `max_turns` (int, optional): Maximum allowable conversation turns
        - `OPENAI_API_BASE_URL` (str, optional): Base URL for OpenAI API endpoints
        - `OPENAI_API_KEY` (str, optional): API key for OpenAI API access
        - Additional keys may exist depending on the specific function implementation
    """

    is_active: bool = False
    """
    Whether the function is currently active.
    """

    is_global: bool = False
    """
    Whether the function is globally available.
    """

    updated_at: int
    """
    Timestamp of the last update (epoch time).
    """

    created_at: int
    """
    Timestamp of creation (epoch time).
    """

    model_config = ConfigDict(from_attributes=True)


class FunctionUserResponse(FunctionModel):
    """
    Response model for a function including user details.
    """

    user: Optional[UserModel] = None
    """
    Details of the user who owns the function.
    """


class FunctionResponse(BaseModel):
    """
    Response model for function details.
    """

    id: str
    """
    Unique identifier for the function.
    """

    user_id: str
    """
    ID of the user who owns the function.
    """

    type: str
    """
    Type of the function.
    """

    name: str
    """
    Name of the function.
    """

    meta: FunctionMeta
    """
    Metadata associated with the function.
    """

    is_active: bool
    """
    Whether the function is currently active.
    """

    is_global: bool
    """
    Whether the function is globally available.
    """

    updated_at: int
    """
    Timestamp of the last update (epoch time).
    """

    created_at: int
    """
    Timestamp of creation (epoch time).
    """


class FunctionForm(BaseModel):
    """
    Form for creating or updating a function.
    """

    id: str
    """
    Unique identifier for the function.
    """

    name: str
    """
    Name of the function.
    """

    content: str
    """
    The Python source code content of the function.
    """

    meta: FunctionMeta
    """
    Metadata associated with the function.
    """


class FunctionValves(BaseModel):
    """
    Model for function valves.
    """

    valves: Optional[dict] = None
    """
    Dictionary of valve configuration values.

    Dict Fields:
        - `priority` (int, optional): Priority level for filter operations
        - `max_turns` (int, optional): Maximum allowable conversation turns
        - `OPENAI_API_BASE_URL` (str, optional): Base URL for OpenAI API endpoints
        - `OPENAI_API_KEY` (str, optional): API key for OpenAI API access
        - Additional keys may exist depending on the specific function implementation
    """


class SyncFunctionsForm(BaseModel):
    """
    Form for syncing multiple functions.
    """

    functions: list[FunctionWithValvesModel] = []
    """
    List of functions to sync.
    """


class LoadUrlForm(BaseModel):
    """
    Form for loading a function from a URL.
    """

    url: HttpUrl
    """
    URL to load the function from (e.g., GitHub URL).
    """
