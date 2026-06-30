from typing import Optional, Union
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


class UpdateTimezoneForm(BaseModel):
    """
    Form data for updating user timezone.
    """

    timezone: str
    """The new timezone (e.g., "America/New_York")."""


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

    ADMIN_EMAIL: Optional[str] = None
    """The admin email address."""

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

    FOLDER_MAX_FILE_COUNT: Optional[int | str] = None
    """Maximum number of files allowed in a folder."""

    AUTOMATION_MAX_COUNT: Optional[int | str] = None
    """Maximum number of automations allowed per user."""

    AUTOMATION_MIN_INTERVAL: Optional[int | str] = None
    """Minimum interval (in seconds) between automation executions."""

    ENABLE_AUTOMATIONS: bool
    """Whether automations are enabled."""

    ENABLE_CHANNELS: bool
    """Whether channels are enabled."""

    ENABLE_CALENDAR: bool
    """Whether the calendar feature is enabled."""

    ENABLE_MEMORIES: bool
    """Whether memories are enabled."""

    ENABLE_NOTES: bool
    """Whether notes are enabled."""

    ENABLE_USER_WEBHOOKS: bool
    """Whether user webhooks are enabled."""

    ENABLE_USER_STATUS: bool
    """Whether user status updates are enabled."""

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


class OAuthConfigForm(BaseModel):
    """
    All OAuth/OIDC provider settings exposed to the admin Authentication page.

    Every field is optional so partial updates are accepted by
    `AuthsClient.update_oauth_config`; omitted fields are left unchanged.
    Values are persisted under the ``oauth.*`` config namespace. Comma-list
    fields (`OAUTH_ALLOWED_DOMAINS`, `OAUTH_ADMIN_ROLES`, `OAUTH_ALLOWED_ROLES`)
    are returned as a comma-joined string and accepted back the same way.

    Persistence caveat: unless the backend runs with
    ``ENABLE_OAUTH_PERSISTENT_CONFIG=true``, reads of ``oauth.*`` keys return
    compiled/env defaults and writes are not reflected on read.
    """

    # General OAuth
    ENABLE_OAUTH_SIGNUP: Optional[bool] = None
    """Allow new users to sign up via OAuth/OIDC."""

    OAUTH_MERGE_ACCOUNTS_BY_EMAIL: Optional[bool] = None
    """Auto-link OAuth logins to existing local accounts with a matching email."""

    OAUTH_AUTO_REDIRECT: Optional[bool] = None
    """Auto-redirect users to the OAuth provider on load (skip the login page)."""

    OAUTH_ALLOWED_DOMAINS: Optional[str] = None
    """Comma-separated email domains permitted to sign in (``*`` = all)."""

    OAUTH_BLOCKED_GROUPS: Optional[str] = None
    """JSON array (as a string) of provider group names blocked from sign-in."""

    # Role management
    ENABLE_OAUTH_ROLE_MANAGEMENT: Optional[bool] = None
    """Enable mapping provider roles/groups to Open WebUI roles."""

    OAUTH_ROLES_CLAIM: Optional[str] = None
    """JWT claim name carrying role/group info (default ``roles``)."""

    OAUTH_ADMIN_ROLES: Optional[str] = None
    """Comma-separated role/group names that grant the ``admin`` role (default ``admin``)."""

    OAUTH_ALLOWED_ROLES: Optional[str] = None
    """Comma-separated role/group names permitted to sign in."""

    # Group management
    ENABLE_OAUTH_GROUP_MANAGEMENT: Optional[bool] = None
    """Map provider groups to Open WebUI groups on login."""

    ENABLE_OAUTH_GROUP_CREATION: Optional[bool] = None
    """Allow creating Open WebUI groups for provider groups that don't yet exist."""

    OAUTH_GROUP_CLAIM: Optional[str] = None
    """JWT claim name carrying group membership (default ``groups``)."""

    OAUTH_GROUP_DEFAULT_SHARE: Optional[Union[bool, str]] = None
    """Default access for auto-created groups: ``True`` (public), ``False`` (private), or ``'members'``."""

    # OIDC provider settings
    OAUTH_PROVIDER_NAME: Optional[str] = None
    """Display name for the SSO provider shown in the UI (default ``SSO``)."""

    OPENID_PROVIDER_URL: Optional[str] = None
    """OIDC issuer /.well-known/openid-configuration discovery URL."""

    OAUTH_CLIENT_ID: Optional[str] = None
    """OAuth/OIDC client ID registered with the provider."""

    OAUTH_CLIENT_SECRET: Optional[str] = None
    """OAuth/OIDC client secret registered with the provider."""

    OPENID_REDIRECT_URI: Optional[str] = None
    """Redirect URI registered with the provider for the authorization callback."""

    OAUTH_SCOPES: Optional[str] = None
    """Space-separated scopes requested during login (default ``openid email profile``)."""

    OAUTH_CODE_CHALLENGE_METHOD: Optional[str] = None
    """PKCE code challenge method; ``S256`` is the supported value when used."""

    OAUTH_TOKEN_ENDPOINT_AUTH_METHOD: Optional[str] = None
    """Token endpoint auth method (e.g. ``client_secret_post``, ``client_secret_basic``)."""

    OPENID_END_SESSION_ENDPOINT: Optional[str] = None
    """Provider end-session URL used for RP-initiated logout."""

    OAUTH_TIMEOUT: Optional[Union[int, str]] = None
    """HTTP timeout (seconds) for the login OAuth flow; empty string disables it."""

    OAUTH_CLIENT_TIMEOUT: Optional[Union[int, str]] = None
    """HTTP timeout (seconds) for OAuth client operations (e.g. MCP tool servers); empty disables it."""

    # Claims
    OAUTH_EMAIL_CLAIM: Optional[str] = None
    """JWT claim name for the user email (default ``email``)."""

    OAUTH_USERNAME_CLAIM: Optional[str] = None
    """JWT claim name for the username/display name (default ``name``)."""

    OAUTH_PICTURE_CLAIM: Optional[str] = None
    """JWT claim name for the avatar/picture URL (default ``picture``)."""

    OAUTH_SUB_CLAIM: Optional[str] = None
    """JWT claim name for the subject identifier (default ``sub``)."""

    OAUTH_AUDIENCE: Optional[str] = None
    """Audience (``aud``) value sent to the provider, e.g. an API/resource identifier."""

    # Profile update toggles
    OAUTH_UPDATE_EMAIL_ON_LOGIN: Optional[bool] = None
    """Overwrite the local user's email with the provider value on each login."""

    OAUTH_UPDATE_NAME_ON_LOGIN: Optional[bool] = None
    """Overwrite the local user's name with the provider value on each login."""

    OAUTH_UPDATE_PICTURE_ON_LOGIN: Optional[bool] = None
    """Overwrite the local user's avatar with the provider value on each login."""

    # Token
    OAUTH_REFRESH_TOKEN_INCLUDE_SCOPE: Optional[bool] = None
    """Include the original scope when refreshing OAuth tokens."""


class ApiKey(BaseModel):
    """
    API Key model.
    """

    api_key: Optional[str] = None
    """The API key string."""


class TokenExchangeForm(BaseModel):
    """
    Form data for OAuth token exchange.

    Used to exchange an external OAuth provider's access token for an Open WebUI JWT.
    """

    token: str
    """The OAuth access token from the external provider."""
