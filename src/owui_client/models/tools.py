from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict, HttpUrl
from owui_client.models.users import UserResponse

class ToolMeta(BaseModel):
    description: Optional[str] = None
    manifest: Optional[dict] = {}

class ToolModel(BaseModel):
    id: str
    user_id: str
    name: str
    content: str
    specs: List[Dict[str, Any]]
    meta: ToolMeta
    access_control: Optional[dict] = None

    updated_at: int  # timestamp in epoch
    created_at: int  # timestamp in epoch

    model_config = ConfigDict(from_attributes=True)

class ToolUserModel(ToolModel):
    user: Optional[UserResponse] = None

class ToolResponse(BaseModel):
    id: str
    user_id: str
    name: str
    meta: ToolMeta
    access_control: Optional[dict] = None
    updated_at: int  # timestamp in epoch
    created_at: int  # timestamp in epoch

class ToolUserResponse(ToolResponse):
    user: Optional[UserResponse] = None

    model_config = ConfigDict(extra="allow")

class ToolForm(BaseModel):
    id: str
    name: str
    content: str
    meta: ToolMeta
    access_control: Optional[dict] = None

class ToolValves(BaseModel):
    valves: Optional[dict] = None

class LoadUrlForm(BaseModel):
    url: HttpUrl

