from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class OpenAIConfigForm(BaseModel):
    ENABLE_OPENAI_API: Optional[bool] = None
    OPENAI_API_BASE_URLS: List[str]
    OPENAI_API_KEYS: List[str]
    OPENAI_API_CONFIGS: Dict[str, Any]


class ConnectionVerificationForm(BaseModel):
    url: str
    key: str
    config: Optional[dict] = None
