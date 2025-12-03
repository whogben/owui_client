from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class ChatModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    title: str
    chat: dict
    
    created_at: int  # timestamp in epoch
    updated_at: int  # timestamp in epoch

    share_id: Optional[str] = None
    archived: bool = False
    pinned: Optional[bool] = False
    
    meta: dict = {}
    folder_id: Optional[str] = None

class ChatForm(BaseModel):
    chat: dict
    folder_id: Optional[str] = None

class ChatImportForm(ChatForm):
    meta: Optional[dict] = {}
    pinned: Optional[bool] = False
    created_at: Optional[int] = None
    updated_at: Optional[int] = None

class ChatsImportForm(BaseModel):
    chats: List[ChatImportForm]

class ChatTitleMessagesForm(BaseModel):
    title: str
    messages: List[dict]

class ChatTitleForm(BaseModel):
    title: str

class ChatResponse(BaseModel):
    id: str
    user_id: str
    title: str
    chat: dict
    updated_at: int  # timestamp in epoch
    created_at: int  # timestamp in epoch
    share_id: Optional[str] = None  # id of the chat to be shared
    archived: bool
    pinned: Optional[bool] = False
    meta: dict = {}
    folder_id: Optional[str] = None

class ChatTitleIdResponse(BaseModel):
    id: str
    title: str
    updated_at: int
    created_at: int

# Models from router
class TagForm(BaseModel):
    name: str

class TagFilterForm(TagForm):
    skip: Optional[int] = 0
    limit: Optional[int] = 50

class MessageForm(BaseModel):
    content: str

class EventForm(BaseModel):
    type: str
    data: dict

class CloneForm(BaseModel):
    title: Optional[str] = None

class ChatFolderIdForm(BaseModel):
    folder_id: Optional[str] = None

