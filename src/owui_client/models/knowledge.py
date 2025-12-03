from typing import Optional, Union
from pydantic import BaseModel, ConfigDict

from owui_client.models.users import UserResponse
from owui_client.models.files import FileMetadataResponse


class KnowledgeModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str

    name: str
    description: str

    meta: Optional[dict] = None

    access_control: Optional[dict] = None

    created_at: int  # timestamp in epoch
    updated_at: int  # timestamp in epoch


class KnowledgeUserModel(KnowledgeModel):
    user: Optional[UserResponse] = None


class KnowledgeResponse(KnowledgeModel):
    files: Optional[list[Union[FileMetadataResponse, dict]]] = None


class KnowledgeUserResponse(KnowledgeUserModel):
    files: Optional[list[Union[FileMetadataResponse, dict]]] = None


class KnowledgeForm(BaseModel):
    name: str
    description: str
    access_control: Optional[dict] = None


class KnowledgeFilesResponse(KnowledgeResponse):
    files: list[FileMetadataResponse]


class KnowledgeFileIdForm(BaseModel):
    file_id: str

