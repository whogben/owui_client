from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict, HttpUrl
from owui_client.models.users import UserResponse


class ToolMeta(BaseModel):
    """
    Metadata for a tool.
    """

    description: Optional[str] = None
    """
    Description of the tool.
    """
    manifest: Optional[dict] = {}
    """
    Manifest of the tool, usually parsed from the tool's file frontmatter.

    Dict Fields:
        - `version` (str, optional): Version of the tool
        - `funding_url` (str, optional): URL for funding/supporting the tool
        - `icon_url` (str, optional): URL for the tool's icon
        - `required_open_webui_version` (str, optional): Minimum required Open WebUI version for this tool
    """


class ToolModel(BaseModel):
    """
    Model representing a tool in the database.
    """

    id: str
    """
    Unique identifier for the tool.
    """
    user_id: str
    """
    ID of the user who created the tool.
    """
    name: str
    """
    Name of the tool.
    """
    content: str
    """
    The Python code content of the tool.
    """
    specs: List[Dict[str, Any]]
    """
    List of function specifications (JSON schema) for the tool's functions.

    Dict Fields:
        - `name` (str, required): Name of the function
        - `description` (str, optional): Description of what the function does
        - `parameters` (dict, required): Parameters schema for the function
            - `type` (str, required): Should be "object"
            - `properties` (dict, required): Dictionary of parameter definitions
                - Each property key is the parameter name
                - Each property value is a parameter specification with:
                    - `type` (str, required): Parameter type (e.g., "string", "number", "boolean", "array", "object")
                    - `description` (str, optional): Description of the parameter
                    - `required` (list[str], optional): List of required parameter names
                    - Additional OpenAPI-style parameter constraints
            - `required` (list[str], optional): List of required parameter names
        - Additional OpenAI function specification fields as needed
    """
    meta: ToolMeta
    """
    Metadata associated with the tool.
    """
    access_control: Optional[dict] = None
    """
    Access control settings for the tool.

    Dict Fields:
        - `read` (dict, optional): Read access permissions
            - `group_ids` (list[str], optional): List of group IDs that have read access
            - `user_ids` (list[str], optional): List of user IDs that have read access
        - `write` (dict, optional): Write access permissions
            - `group_ids` (list[str], optional): List of group IDs that have write access
            - `user_ids` (list[str], optional): List of user IDs that have write access

    Special values:
        - `None`: Public access, available to all users with the "user" role
        - `{}`: Private access, restricted exclusively to the owner
    """

    updated_at: int
    """
    Timestamp of the last update (epoch).
    """
    created_at: int
    """
    Timestamp of creation (epoch).
    """

    model_config = ConfigDict(from_attributes=True)


class ToolUserModel(ToolModel):
    """
    Tool model with associated user information.
    """

    user: Optional[UserResponse] = None
    """
    Details of the user who owns the tool.
    """


class ToolResponse(BaseModel):
    """
    Response model for tool operations, excluding heavy content/specs.
    """

    id: str
    """
    Unique identifier for the tool.
    """
    user_id: str
    """
    ID of the user who created the tool.
    """
    name: str
    """
    Name of the tool.
    """
    meta: ToolMeta
    """
    Metadata associated with the tool.
    """
    access_control: Optional[dict] = None
    """
    Access control settings for the tool.

    Dict Fields:
        - `read` (dict, optional): Read access permissions
            - `group_ids` (list[str], optional): List of group IDs that have read access
            - `user_ids` (list[str], optional): List of user IDs that have read access
        - `write` (dict, optional): Write access permissions
            - `group_ids` (list[str], optional): List of group IDs that have write access
            - `user_ids` (list[str], optional): List of user IDs that have write access

    Special values:
        - `None`: Public access, available to all users with the "user" role
        - `{}`: Private access, restricted exclusively to the owner
    """
    updated_at: int
    """
    Timestamp of the last update (epoch).
    """
    created_at: int
    """
    Timestamp of creation (epoch).
    """


class ToolUserResponse(ToolResponse):
    """
    Tool response including user details.
    """

    user: Optional[UserResponse] = None
    """
    Details of the user who owns the tool.
    """
    has_user_valves: Optional[bool] = None
    """
    Indicates if the tool has user-specific valves (settings).
    """

    model_config = ConfigDict(extra="allow")
    """
    Allows extra fields like `has_user_valves` which are dynamically added.
    """


class ToolForm(BaseModel):
    """
    Form for creating or updating a tool.
    """

    id: str
    """
    Unique identifier for the tool.
    """
    name: str
    """
    Name of the tool.
    """
    content: str
    """
    The Python code content of the tool.
    """
    meta: ToolMeta
    """
    Metadata associated with the tool.
    """
    access_control: Optional[dict] = None
    """
    Access control settings for the tool.

    Dict Fields:
        - `read` (dict, optional): Read access permissions
            - `group_ids` (list[str], optional): List of group IDs that have read access
            - `user_ids` (list[str], optional): List of user IDs that have read access
        - `write` (dict, optional): Write access permissions
            - `group_ids` (list[str], optional): List of group IDs that have write access
            - `user_ids` (list[str], optional): List of user IDs that have write access

    Special values:
        - `None`: Public access, available to all users with the "user" role
        - `{}`: Private access, restricted exclusively to the owner
    """


class ToolValves(BaseModel):
    """
    Model representing tool valves (configuration settings).
    """

    valves: Optional[dict] = None
    """
    Dictionary of valve values representing tool-specific configuration settings.

    Dict Fields:
        - Arbitrary key-value pairs defined by each tool's `Valves` class
        - Common examples from tool implementations:
            - `priority` (int, optional): Priority level for tool operations
            - `max_turns` (int, optional): Maximum allowable conversation turns
            - `OPENAI_API_BASE_URL` (str, optional): Base URL for OpenAI API calls
            - `OPENAI_API_KEY` (str, optional): API key for OpenAI services
            - Other tool-specific configuration parameters

    Valves are tool-specific configuration settings that control the behavior of tools.
    Each tool can define its own Valves class with custom parameters.
    The valves dictionary contains the current configuration values for the tool.

    Special behavior:
        - `None`: No valves configured for this tool
        - `{}`: Empty valves configuration (tool uses default settings)
        - When present: Contains the active configuration for the tool

    Valves can be managed via the following endpoints:
        - GET `/tools/id/{id}/valves` - Get current valves for a tool
        - POST `/tools/id/{id}/valves/update` - Update valves for a tool
        - GET `/tools/id/{id}/valves/spec` - Get the Valves schema definition for a tool
    """


class LoadUrlForm(BaseModel):
    """
    Form for loading a tool from a URL.
    """

    url: HttpUrl
    """
    The URL to load the tool from (e.g., a GitHub raw URL).
    """
