from pydantic import BaseModel

class UrlForm(BaseModel):
    url: str

