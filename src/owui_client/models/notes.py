from typing import Optional
from pydantic import BaseModel, ConfigDict
from owui_client.models.users import UserResponse

class NoteModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str

    title: str
    data: Optional[dict] = None
    meta: Optional[dict] = None

    access_control: Optional[dict] = None

    created_at: int  # timestamp in epoch
    updated_at: int  # timestamp in epoch

class NoteForm(BaseModel):
    title: str
    data: Optional[dict] = None
    meta: Optional[dict] = None
    access_control: Optional[dict] = None

class NoteUpdateForm(BaseModel):
    title: Optional[str] = None
    data: Optional[dict] = None
    meta: Optional[dict] = None
    access_control: Optional[dict] = None

class NoteUserResponse(NoteModel):
    user: Optional[UserResponse] = None

class NoteTitleIdResponse(BaseModel):
    id: str
    title: str
    updated_at: int
    created_at: int

