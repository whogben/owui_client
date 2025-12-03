from typing import Optional
from pydantic import BaseModel, ConfigDict


class MemoryModel(BaseModel):
    id: str
    user_id: str
    content: str
    updated_at: int  # timestamp in epoch
    created_at: int  # timestamp in epoch

    model_config = ConfigDict(from_attributes=True)


class AddMemoryForm(BaseModel):
    content: str


class MemoryUpdateModel(BaseModel):
    content: Optional[str] = None


class QueryMemoryForm(BaseModel):
    content: str
    k: Optional[int] = 1

