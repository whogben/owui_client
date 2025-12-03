from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from owui_client.models.users import UserNameResponse

class MessageModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    channel_id: Optional[str] = None

    reply_to_id: Optional[str] = None
    parent_id: Optional[str] = None

    # Pins
    is_pinned: bool = False
    pinned_by: Optional[str] = None
    pinned_at: Optional[int] = None  # timestamp in epoch (time_ns)

    content: str
    data: Optional[dict] = None
    meta: Optional[dict] = None

    created_at: int  # timestamp in epoch (time_ns)
    updated_at: int  # timestamp in epoch (time_ns)


class MessageForm(BaseModel):
    temp_id: Optional[str] = None
    content: str
    reply_to_id: Optional[str] = None
    parent_id: Optional[str] = None
    data: Optional[dict] = None
    meta: Optional[dict] = None


class ReactionForm(BaseModel):
    name: str


class Reactions(BaseModel):
    name: str
    users: List[dict]
    count: int


class MessageUserResponse(MessageModel):
    user: Optional[UserNameResponse] = None


class MessageReplyToResponse(MessageUserResponse):
    reply_to_message: Optional[MessageUserResponse] = None


class MessageWithReactionsResponse(MessageUserResponse):
    reactions: List[Reactions]


class MessageResponse(MessageReplyToResponse):
    latest_reply_at: Optional[int] = None
    reply_count: int = 0
    reactions: List[Reactions]

