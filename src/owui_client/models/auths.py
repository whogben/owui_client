from typing import Optional
from datetime import date
from pydantic import BaseModel


class Token(BaseModel):
    token: str
    token_type: str


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    profile_image_url: str


class SigninResponse(Token, UserResponse):
    pass


class SigninForm(BaseModel):
    email: str
    password: str


class LdapForm(BaseModel):
    user: str
    password: str


class SignupForm(BaseModel):
    name: str
    email: str
    password: str
    profile_image_url: Optional[str] = "/user.png"


class AddUserForm(SignupForm):
    role: Optional[str] = "pending"


class SessionUserResponse(Token, UserResponse):
    expires_at: Optional[int] = None
    permissions: Optional[dict] = None


class SessionUserInfoResponse(SessionUserResponse):
    bio: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None


class UpdatePasswordForm(BaseModel):
    password: str
    new_password: str


class SignoutResponse(BaseModel):
    status: bool
    redirect_url: Optional[str] = None


class AdminConfig(BaseModel):
    SHOW_ADMIN_DETAILS: bool
    WEBUI_URL: str
    ENABLE_SIGNUP: bool
    ENABLE_API_KEYS: bool
    ENABLE_API_KEYS_ENDPOINT_RESTRICTIONS: bool
    API_KEYS_ALLOWED_ENDPOINTS: str
    DEFAULT_USER_ROLE: str
    DEFAULT_GROUP_ID: str
    JWT_EXPIRES_IN: str
    ENABLE_COMMUNITY_SHARING: bool
    ENABLE_MESSAGE_RATING: bool
    ENABLE_FOLDERS: bool
    ENABLE_CHANNELS: bool
    ENABLE_NOTES: bool
    ENABLE_USER_WEBHOOKS: bool
    PENDING_USER_OVERLAY_TITLE: Optional[str] = None
    PENDING_USER_OVERLAY_CONTENT: Optional[str] = None
    RESPONSE_WATERMARK: Optional[str] = None


class AdminDetails(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class LdapServerConfig(BaseModel):
    label: str
    host: str
    port: Optional[int] = None
    attribute_for_mail: str = "mail"
    attribute_for_username: str = "uid"
    app_dn: str
    app_dn_password: str
    search_base: str
    search_filters: str = ""
    use_tls: bool = True
    certificate_path: Optional[str] = None
    validate_cert: bool = True
    ciphers: Optional[str] = "ALL"


class LdapConfigForm(BaseModel):
    enable_ldap: Optional[bool] = None


class LdapConfigResponse(BaseModel):
    ENABLE_LDAP: bool


class ApiKey(BaseModel):
    api_key: Optional[str] = None
