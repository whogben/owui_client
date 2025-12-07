import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class UpdateProfileForm(BaseModel):
    profile_image_url: str
    name: str
    bio: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[datetime.date] = None


class UserSettings(BaseModel):
    ui: Optional[dict] = {}
    model_config = ConfigDict(extra="allow")


class UserModel(BaseModel):
    id: str
    name: str

    email: str
    username: Optional[str] = None

    role: str = "pending"
    profile_image_url: Optional[str] = None
    profile_banner_image_url: Optional[str] = None

    bio: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[datetime.date] = None
    timezone: Optional[str] = None

    presence_state: Optional[str] = None
    status_emoji: Optional[str] = None
    status_message: Optional[str] = None
    status_expires_at: Optional[int] = None

    info: Optional[dict] = None
    settings: Optional[UserSettings] = None

    api_key: Optional[str] = None
    oauth: Optional[dict] = None
    oauth_sub: Optional[str] = None

    last_active_at: int  # timestamp in epoch
    updated_at: int  # timestamp in epoch
    created_at: int  # timestamp in epoch

    model_config = ConfigDict(from_attributes=True)


class UserGroupIdsModel(UserModel):
    group_ids: list[str] = []


class UserGroupIdsListResponse(BaseModel):
    users: list[UserGroupIdsModel]
    total: int


class UserModelResponse(UserModel):
    model_config = ConfigDict(extra="allow")


class UserListResponse(BaseModel):
    users: list[UserModelResponse]
    total: int


class UserStatus(BaseModel):
    status_emoji: Optional[str] = None
    status_message: Optional[str] = None
    status_expires_at: Optional[int] = None


class UserInfoResponse(UserStatus):
    id: str
    name: str
    email: str
    role: str


class UserInfoListResponse(BaseModel):
    users: list[UserInfoResponse]
    total: int


class ActiveUsersResponse(BaseModel):
    user_ids: list[str]


class UserActiveResponse(UserStatus):
    name: str
    profile_image_url: Optional[str] = None
    is_active: bool
    model_config = ConfigDict(extra="allow")


class UserIdNameResponse(BaseModel):
    id: str
    name: str


class UserIdNameStatusResponse(UserStatus):
    id: str
    name: str
    is_active: Optional[bool] = None


class UserIdNameListResponse(BaseModel):
    users: list[UserIdNameResponse]
    total: int


class UserNameResponse(BaseModel):
    id: str
    name: str
    role: str


class UserProfileImageResponse(UserNameResponse):
    email: str
    profile_image_url: str


class WorkspacePermissions(BaseModel):
    models: bool = False
    knowledge: bool = False
    prompts: bool = False
    tools: bool = False
    models_import: bool = False
    models_export: bool = False
    prompts_import: bool = False
    prompts_export: bool = False
    tools_import: bool = False
    tools_export: bool = False


class SharingPermissions(BaseModel):
    models: bool = False
    public_models: bool = False
    knowledge: bool = False
    public_knowledge: bool = False
    prompts: bool = False
    public_prompts: bool = False
    tools: bool = False
    public_tools: bool = True
    notes: bool = False
    public_notes: bool = True


class ChatPermissions(BaseModel):
    controls: bool = True
    valves: bool = True
    system_prompt: bool = True
    params: bool = True
    file_upload: bool = True
    delete: bool = True
    delete_message: bool = True
    continue_response: bool = True
    regenerate_response: bool = True
    rate_response: bool = True
    edit: bool = True
    share: bool = True
    export: bool = True
    stt: bool = True
    tts: bool = True
    call: bool = True
    multiple_models: bool = True
    temporary: bool = True
    temporary_enforced: bool = False


class FeaturesPermissions(BaseModel):
    api_keys: bool = False
    direct_tool_servers: bool = False
    web_search: bool = True
    image_generation: bool = True
    code_interpreter: bool = True
    notes: bool = True
    channels: bool = True
    folders: bool = True


class UserPermissions(BaseModel):
    workspace: WorkspacePermissions
    sharing: SharingPermissions
    chat: ChatPermissions
    features: FeaturesPermissions


class UserResponse(UserNameResponse):
    email: str


class UserUpdateForm(BaseModel):
    role: str
    name: str
    email: str
    profile_image_url: str
    password: Optional[str] = None
