from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from owui_client.models.users import UserIdNameStatusResponse, UserListResponse

class ChannelModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str

    type: Optional[str] = None

    name: str
    description: Optional[str] = None

    is_private: Optional[bool] = None

    data: Optional[dict] = None
    meta: Optional[dict] = None
    access_control: Optional[dict] = None

    created_at: int  # timestamp in epoch (time_ns)

    updated_at: int  # timestamp in epoch (time_ns)
    updated_by: Optional[str] = None

    archived_at: Optional[int] = None  # timestamp in epoch (time_ns)
    archived_by: Optional[str] = None

    deleted_at: Optional[int] = None  # timestamp in epoch (time_ns)
    deleted_by: Optional[str] = None


class ChannelMemberModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    channel_id: str
    user_id: str

    role: Optional[str] = None
    status: Optional[str] = None

    is_active: bool = True

    is_channel_muted: bool = False
    is_channel_pinned: bool = False

    data: Optional[dict] = None
    meta: Optional[dict] = None

    invited_at: Optional[int] = None  # timestamp in epoch (time_ns)
    invited_by: Optional[str] = None

    joined_at: Optional[int] = None  # timestamp in epoch (time_ns)
    left_at: Optional[int] = None  # timestamp in epoch (time_ns)

    last_read_at: Optional[int] = None  # timestamp in epoch (time_ns)

    created_at: Optional[int] = None  # timestamp in epoch (time_ns)
    updated_at: Optional[int] = None  # timestamp in epoch (time_ns)


class ChannelWebhookModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    channel_id: str
    user_id: str

    name: str
    profile_image_url: Optional[str] = None

    token: str
    last_used_at: Optional[int] = None  # timestamp in epoch (time_ns)

    created_at: int  # timestamp in epoch (time_ns)
    updated_at: int  # timestamp in epoch (time_ns)


class ChannelForm(BaseModel):
    name: str = ""
    description: Optional[str] = None
    is_private: Optional[bool] = None
    data: Optional[dict] = None
    meta: Optional[dict] = None
    access_control: Optional[dict] = None
    group_ids: Optional[list[str]] = None
    user_ids: Optional[list[str]] = None


class CreateChannelForm(ChannelForm):
    type: Optional[str] = None


class ChannelResponse(ChannelModel):
    is_manager: bool = False
    write_access: bool = False

    user_count: Optional[int] = None


# Router-level models

class ChannelListItemResponse(ChannelModel):
    user_ids: Optional[list[str]] = None  # 'dm' channels only
    users: Optional[list[UserIdNameStatusResponse]] = None  # 'dm' channels only

    last_message_at: Optional[int] = None  # timestamp in epoch (time_ns)
    unread_count: int = 0


class ChannelFullResponse(ChannelResponse):
    user_ids: Optional[list[str]] = None  # 'group'/'dm' channels only
    users: Optional[list[UserIdNameStatusResponse]] = None  # 'group'/'dm' channels only

    last_read_at: Optional[int] = None  # timestamp in epoch (time_ns)
    unread_count: int = 0


class UpdateActiveMemberForm(BaseModel):
    is_active: bool


class UpdateMembersForm(BaseModel):
    user_ids: list[str] = []
    group_ids: list[str] = []


class RemoveMembersForm(BaseModel):
    user_ids: list[str] = []

