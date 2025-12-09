from typing import Optional
from datetime import date
from pydantic import BaseModel
from owui_client.models.users import UserProfileImageResponse, UserStatus


class Token(BaseModel):
    """
    `Token` response model.
    """

    token: str
    """The access token string."""

    token_type: str
    """The type of token (e.g., "Bearer")."""


class SigninResponse(Token, UserProfileImageResponse):
    """
    Response model for sign-in operations, containing the token and user profile.
    """

    pass


class SigninForm(BaseModel):
    """
    Form data for user sign-in.
    """

    email: str
    """The user's email address."""

    password: str
    """The user's password."""


class LdapForm(BaseModel):
    """
    Form data for LDAP sign-in.
    """

    user: str
    """The LDAP username."""

    password: str
    """The LDAP password."""


class SignupForm(BaseModel):
    """
    Form data for user sign-up.
    """

    name: str
    """The user's full name."""

    email: str
    """The user's email address."""

    password: str
    """The user's password."""

    profile_image_url: Optional[str] = "/user.png"
    """URL to the user's profile image. Defaults to "/user.png"."""


class AddUserForm(SignupForm):
    """
    Form data for adding a new user (admin only).
    """

    role: Optional[str] = "pending"
    """The user's role. Defaults to "pending"."""


class SessionUserResponse(Token, UserProfileImageResponse):
    """
    Response model for the current session user.
    """

    expires_at: Optional[int] = None
    """The timestamp when the session expires (in epoch seconds)."""

    permissions: Optional[dict] = None
    """The user's permissions.

    Dict Fields:
        - `workspace` (dict, required): Workspace-related permissions
            - `models` (bool, required): Access to models in workspace
            - `knowledge` (bool, required): Access to knowledge in workspace
            - `prompts` (bool, required): Access to prompts in workspace
            - `tools` (bool, required): Access to tools in workspace
            - `models_import` (bool, required): Permission to import models
            - `models_export` (bool, required): Permission to export models
            - `prompts_import` (bool, required): Permission to import prompts
            - `prompts_export` (bool, required): Permission to export prompts
            - `tools_import` (bool, required): Permission to import tools
            - `tools_export` (bool, required): Permission to export tools
        - `sharing` (dict, required): Sharing-related permissions
            - `models` (bool, required): Permission to share models
            - `public_models` (bool, required): Permission to share models publicly
            - `knowledge` (bool, required): Permission to share knowledge
            - `public_knowledge` (bool, required): Permission to share knowledge publicly
            - `prompts` (bool, required): Permission to share prompts
            - `public_prompts` (bool, required): Permission to share prompts publicly
            - `tools` (bool, required): Permission to share tools
            - `public_tools` (bool, required): Permission to share tools publicly
            - `notes` (bool, required): Permission to share notes
            - `public_notes` (bool, required): Permission to share notes publicly
        - `chat` (dict, required): Chat-related permissions
            - `controls` (bool, required): Access to chat controls
            - `valves` (bool, required): Access to chat valves
            - `system_prompt` (bool, required): Access to system prompt configuration
            - `params` (bool, required): Access to chat parameters
            - `file_upload` (bool, required): Permission to upload files
            - `delete` (bool, required): Permission to delete chats
            - `delete_message` (bool, required): Permission to delete messages
            - `continue_response` (bool, required): Permission to continue responses
            - `regenerate_response` (bool, required): Permission to regenerate responses
            - `rate_response` (bool, required): Permission to rate responses
            - `edit` (bool, required): Permission to edit chats
            - `share` (bool, required): Permission to share chats
            - `export` (bool, required): Permission to export chats
            - `stt` (bool, required): Permission to use speech-to-text
            - `tts` (bool, required): Permission to use text-to-speech
            - `call` (bool, required): Permission to make calls
            - `multiple_models` (bool, required): Permission to use multiple models
            - `temporary` (bool, required): Permission to use temporary chats
            - `temporary_enforced` (bool, required): Enforced temporary chat usage
        - `features` (dict, required): Feature-related permissions
            - `api_keys` (bool, required): Access to API keys feature
            - `notes` (bool, required): Access to notes feature
            - `folders` (bool, required): Access to folders feature
            - `channels` (bool, required): Access to channels feature
            - `direct_tool_servers` (bool, required): Access to direct tool servers
            - `web_search` (bool, required): Access to web search feature
            - `image_generation` (bool, required): Access to image generation feature
            - `code_interpreter` (bool, required): Access to code interpreter feature
"""


class SessionUserInfoResponse(SessionUserResponse, UserStatus):
    """
    Detailed response model for the current session user, including status and profile details.
    """

    bio: Optional[str] = None
    """The user's biography."""

    gender: Optional[str] = None
    """The user's gender."""

    date_of_birth: Optional[date] = None
    """The user's date of birth."""


class UpdatePasswordForm(BaseModel):
    """
    Form data for updating the user's password.
    """

    password: str
    """The current password."""

    new_password: str
    """The new password."""


class SignoutResponse(BaseModel):
    """
    Response model for sign-out operations.
    """

    status: bool
    """True if sign-out was successful."""

    redirect_url: Optional[str] = None
    """Optional URL to redirect to after sign-out."""


class AdminConfig(BaseModel):
    """
    Configuration settings for the admin.
    """

    SHOW_ADMIN_DETAILS: bool
    """Whether to show admin details to users."""

    WEBUI_URL: str
    """The base URL of the WebUI."""

    ENABLE_SIGNUP: bool
    """Whether user signup is enabled."""

    ENABLE_API_KEYS: bool
    """Whether API keys are enabled."""

    ENABLE_API_KEYS_ENDPOINT_RESTRICTIONS: bool
    """Whether to restrict API key usage to specific endpoints."""

    API_KEYS_ALLOWED_ENDPOINTS: str
    """Comma-separated list of allowed endpoints for API keys."""

    DEFAULT_USER_ROLE: str
    """The default role assigned to new users."""

    DEFAULT_GROUP_ID: str
    """The default group ID assigned to new users."""

    JWT_EXPIRES_IN: str
    """Duration string for JWT expiration (e.g., "-1", "1h")."""

    ENABLE_COMMUNITY_SHARING: bool
    """Whether community sharing is enabled."""

    ENABLE_MESSAGE_RATING: bool
    """Whether message rating is enabled."""

    ENABLE_FOLDERS: bool
    """Whether folders are enabled."""

    ENABLE_CHANNELS: bool
    """Whether channels are enabled."""

    ENABLE_NOTES: bool
    """Whether notes are enabled."""

    ENABLE_USER_WEBHOOKS: bool
    """Whether user webhooks are enabled."""

    PENDING_USER_OVERLAY_TITLE: Optional[str] = None
    """Title for the overlay shown to pending users."""

    PENDING_USER_OVERLAY_CONTENT: Optional[str] = None
    """Content for the overlay shown to pending users."""

    RESPONSE_WATERMARK: Optional[str] = None
    """Text to append to model responses (watermark)."""


class AdminDetails(BaseModel):
    """
    Details of the admin user.
    """

    name: Optional[str] = None
    """The admin's name."""

    email: Optional[str] = None
    """The admin's email address."""


class LdapServerConfig(BaseModel):
    """
    Configuration for the LDAP server.
    """

    label: str
    """Label for the LDAP server configuration."""

    host: str
    """LDAP server hostname or IP."""

    port: Optional[int] = None
    """LDAP server port."""

    attribute_for_mail: str = "mail"
    """LDAP attribute to map to user email."""

    attribute_for_username: str = "uid"
    """LDAP attribute to map to username."""

    app_dn: str
    """Application Distinguished Name (DN) for binding."""

    app_dn_password: str
    """Password for the Application DN."""

    search_base: str
    """Base DN for user searches."""

    search_filters: str = ""
    """Additional LDAP search filters."""

    use_tls: bool = True
    """Whether to use TLS."""

    certificate_path: Optional[str] = None
    """Path to the CA certificate file."""

    validate_cert: bool = True
    """Whether to validate the server certificate."""

    ciphers: Optional[str] = "ALL"
    """OpenSSL cipher string."""


class LdapConfigForm(BaseModel):
    """
    Form data for updating LDAP configuration status.
    """

    enable_ldap: Optional[bool] = None
    """Whether to enable LDAP authentication."""


class LdapConfigResponse(BaseModel):
    """
    Response model for LDAP configuration status.
    """

    ENABLE_LDAP: bool
    """Whether LDAP authentication is enabled."""


class ApiKey(BaseModel):
    """
    API Key model.
    """

    api_key: Optional[str] = None
    """The API key string."""
