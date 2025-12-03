from typing import Optional
from pydantic import BaseModel, ConfigDict, HttpUrl
from owui_client.models.users import UserModel


class FunctionMeta(BaseModel):
    description: Optional[str] = None
    manifest: Optional[dict] = {}
    model_config = ConfigDict(extra="allow")


class FunctionModel(BaseModel):
    id: str
    user_id: str
    name: str
    type: str
    content: str
    meta: FunctionMeta
    is_active: bool = False
    is_global: bool = False
    updated_at: int  # timestamp in epoch
    created_at: int  # timestamp in epoch

    model_config = ConfigDict(from_attributes=True)


class FunctionWithValvesModel(BaseModel):
    id: str
    user_id: str
    name: str
    type: str
    content: str
    meta: FunctionMeta
    valves: Optional[dict] = None
    is_active: bool = False
    is_global: bool = False
    updated_at: int  # timestamp in epoch
    created_at: int  # timestamp in epoch

    model_config = ConfigDict(from_attributes=True)


class FunctionUserResponse(FunctionModel):
    user: Optional[UserModel] = None


class FunctionResponse(BaseModel):
    id: str
    user_id: str
    type: str
    name: str
    meta: FunctionMeta
    is_active: bool
    is_global: bool
    updated_at: int  # timestamp in epoch
    created_at: int  # timestamp in epoch


class FunctionForm(BaseModel):
    id: str
    name: str
    content: str
    meta: FunctionMeta


class FunctionValves(BaseModel):
    valves: Optional[dict] = None


class SyncFunctionsForm(BaseModel):
    functions: list[FunctionWithValvesModel] = []


class LoadUrlForm(BaseModel):
    url: HttpUrl

