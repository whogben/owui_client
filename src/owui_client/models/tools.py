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
    """
    meta: ToolMeta
    """
    Metadata associated with the tool.
    """
    access_control: Optional[dict] = None
    """
    Access control settings for the tool.
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
    """

class ToolValves(BaseModel):
    """
    Model representing tool valves (configuration settings).
    """
    valves: Optional[dict] = None
    """
    Dictionary of valve values.
    """

class LoadUrlForm(BaseModel):
    """
    Form for loading a tool from a URL.
    """
    url: HttpUrl
    """
    The URL to load the tool from (e.g., a GitHub raw URL).
    """

