from typing import Optional
from pydantic import BaseModel, ConfigDict


class FolderMetadataResponse(BaseModel):
    icon: Optional[str] = None


class FolderModel(BaseModel):
    id: str
    parent_id: Optional[str] = None
    user_id: str
    name: str
    items: Optional[dict] = None
    meta: Optional[dict] = None
    data: Optional[dict] = None
    is_expanded: bool = False
    created_at: int
    updated_at: int

    model_config = ConfigDict(from_attributes=True)


class FolderNameIdResponse(BaseModel):
    id: str
    name: str
    meta: Optional[FolderMetadataResponse] = None
    parent_id: Optional[str] = None
    is_expanded: bool = False
    created_at: int
    updated_at: int


class FolderForm(BaseModel):
    name: str
    data: Optional[dict] = None
    meta: Optional[dict] = None
    model_config = ConfigDict(extra="allow")


class FolderUpdateForm(BaseModel):
    name: Optional[str] = None
    data: Optional[dict] = None
    meta: Optional[dict] = None
    model_config = ConfigDict(extra="allow")


class FolderParentIdForm(BaseModel):
    parent_id: Optional[str] = None


class FolderIsExpandedForm(BaseModel):
    is_expanded: bool

