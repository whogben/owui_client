from pydantic import BaseModel

class AddPipelineForm(BaseModel):
    url: str
    urlIdx: int

class DeletePipelineForm(BaseModel):
    id: str
    urlIdx: int

