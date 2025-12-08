from owui_client.client_base import ResourceBase
from owui_client.models.auths import (
    SigninForm,
    SignupForm,
    LdapForm,
    SessionUserResponse,
    SessionUserInfoResponse,
    AdminConfig,
    SignoutResponse,
    UpdatePasswordForm,
    AddUserForm,
    SigninResponse,
    AdminDetails,
    LdapServerConfig,
    LdapConfigForm,
    LdapConfigResponse,
    ApiKey,
)
from owui_client.models.users import UpdateProfileForm, UserProfileImageResponse


class AuthsClient(ResourceBase):
    """
    Client for the Auths endpoints.

    This client handles authentication operations such as signin, signup,
    password updates, and administrative configurations.
    """

    async def get_session_user(self) -> SessionUserInfoResponse:
        """
        Get the current session user information.

        This endpoint retrieves detailed information about the currently authenticated user,
        including their profile, permissions, and status.

        Returns:
            `SessionUserInfoResponse`: Session user information
        """
        return await self._request(
            "GET",
            "/v1/auths/",
            model=SessionUserInfoResponse,
        )

    async def update_profile(self, form_data: UpdateProfileForm) -> UserProfileImageResponse:
        """
        Update the current user's profile.

        Updates the user's name, bio, gender, date of birth, and profile image.

        Args:
            form_data: The profile update information

        Returns:
            `UserProfileImageResponse`: Updated user information
        """
        return await self._request(
            "POST",
            "/v1/auths/update/profile",
            model=UserProfileImageResponse,
            json=form_data.model_dump(),
        )

    async def update_password(self, form_data: UpdatePasswordForm) -> bool:
        """
        Update the current user's password.

        Verifies the current password before updating to the new one.

        Args:
            form_data: The password update information (current and new password)

        Returns:
            True if successful
        """
        return await self._request(
            "POST",
            "/v1/auths/update/password",
            model=bool,
            json=form_data.model_dump(),
        )

    async def signin(
        self, form_data: SigninForm, set_client_api_key: bool = True
    ) -> SessionUserResponse:
        """
        Sign in with email and password.

        Authenticates the user using email and password. On success, it returns a session
        token and user details.

        Args:
            form_data: The signin credentials (email, password)
            set_client_api_key: If True (default), updates the main client's API key upon success

        Returns:
            `SessionUserResponse`: Session information including token and user details
        """
        response = await self._request(
            "POST",
            "/v1/auths/signin",
            model=SessionUserResponse,
            json=form_data.model_dump(),
        )

        if set_client_api_key and response.token:
            self._client.api_key = response.token

        return response

    async def signin_ldap(
        self, form_data: LdapForm, set_client_api_key: bool = True
    ) -> SessionUserResponse:
        """
        Sign in with LDAP credentials.

        Authenticates the user using LDAP. Requires LDAP to be enabled and configured on the server.

        Args:
            form_data: The LDAP credentials (user, password)
            set_client_api_key: If True (default), updates the main client's API key upon success

        Returns:
            `SessionUserResponse`: Session information including token and user details
        """
        response = await self._request(
            "POST",
            "/v1/auths/ldap",
            model=SessionUserResponse,
            json=form_data.model_dump(),
        )

        if set_client_api_key and response.token:
            self._client.api_key = response.token

        return response

    async def signup(
        self, form_data: SignupForm, set_client_api_key: bool = True
    ) -> SessionUserResponse:
        """
        Sign up a new user.

        Creates a new user account. If this is the first user, they will be assigned the 'admin' role.
        Subsequent users are assigned the default role (usually 'pending').

        Args:
            form_data: The signup information (name, email, password, etc.)
            set_client_api_key: If True (default), updates the main client's API key upon success

        Returns:
            `SessionUserResponse`: Session information including token and user details
        """
        response = await self._request(
            "POST",
            "/v1/auths/signup",
            model=SessionUserResponse,
            json=form_data.model_dump(),
        )

        if set_client_api_key and response.token:
            self._client.api_key = response.token

        return response

    async def add_user(self, form_data: AddUserForm) -> SigninResponse:
        """
        Add a new user (Admin only).

        Allows an admin to create a new user account directly, specifying their role.

        Args:
            form_data: The user information (name, email, password, role, etc.)

        Returns:
            `SigninResponse`: Response including token and user details
        """
        return await self._request(
            "POST",
            "/v1/auths/add",
            model=SigninResponse,
            json=form_data.model_dump(),
        )

    async def get_admin_details(self) -> AdminDetails:
        """
        Get admin details.

        Retrieves the name and email of the admin user, if configured to be shown.

        Returns:
            `AdminDetails`: Admin details (name, email)
        """
        return await self._request(
            "GET",
            "/v1/auths/admin/details",
            model=AdminDetails,
        )

    async def sign_out(self, unset_client_api_key: bool = True) -> SignoutResponse:
        """
        Sign out the current user.

        Invalidates the current session token.

        Args:
            unset_client_api_key: If True (default), clears the main client's API key upon success

        Returns:
            SignoutResponse: Signout status
        """
        response = await self._request(
            "GET",
            "/v1/auths/signout",
            model=SignoutResponse,
        )

        if unset_client_api_key and response.status:
            self._client.api_key = None

        return response

    async def get_admin_config(self) -> AdminConfig:
        """
        Get the admin configuration.

        Retrieves global configuration settings for the application.

        Returns:
            AdminConfig: The admin configuration
        """
        return await self._request(
            "GET",
            "/v1/auths/admin/config",
            model=AdminConfig,
        )

    async def update_admin_config(self, config: AdminConfig) -> AdminConfig:
        """
        Update the admin configuration.

        Updates global configuration settings. Requires admin privileges.

        Args:
            config: The new configuration

        Returns:
            AdminConfig: The updated configuration
        """
        return await self._request(
            "POST",
            "/v1/auths/admin/config",
            model=AdminConfig,
            json=config.model_dump(),
        )

    async def get_ldap_server(self) -> LdapServerConfig:
        """
        Get the LDAP server configuration.

        Retrieves the LDAP connection settings. Requires admin privileges.

        Returns:
            LdapServerConfig: LDAP server configuration
        """
        return await self._request(
            "GET",
            "/v1/auths/admin/config/ldap/server",
            model=LdapServerConfig,
        )

    async def update_ldap_server(self, form_data: LdapServerConfig) -> LdapServerConfig:
        """
        Update the LDAP server configuration.

        Updates the LDAP connection settings. Requires admin privileges.

        Args:
            form_data: The LDAP server configuration

        Returns:
            LdapServerConfig: Updated LDAP server configuration
        """
        return await self._request(
            "POST",
            "/v1/auths/admin/config/ldap/server",
            model=LdapServerConfig,
            json=form_data.model_dump(),
        )

    async def get_ldap_config(self) -> LdapConfigResponse:
        """
        Get the LDAP configuration status.

        Checks if LDAP authentication is enabled.

        Returns:
            LdapConfigResponse: LDAP configuration status
        """
        return await self._request(
            "GET",
            "/v1/auths/admin/config/ldap",
            model=LdapConfigResponse,
        )

    async def update_ldap_config(self, form_data: LdapConfigForm) -> LdapConfigResponse:
        """
        Update the LDAP configuration status.

        Enables or disables LDAP authentication. Requires admin privileges.

        Args:
            form_data: The LDAP configuration form

        Returns:
            LdapConfigResponse: Updated LDAP configuration status
        """
        return await self._request(
            "POST",
            "/v1/auths/admin/config/ldap",
            model=LdapConfigResponse,
            json=form_data.model_dump(),
        )

    async def generate_api_key(self) -> ApiKey:
        """
        Generate a new API key for the current user.

        Creates or rotates the API key for the current user.

        Returns:
            ApiKey: The generated API key
        """
        return await self._request(
            "POST",
            "/v1/auths/api_key",
            model=ApiKey,
        )

    async def delete_api_key(self) -> bool:
        """
        Delete the current user's API key.

        Removes the API key associated with the current user.

        Returns:
            bool: True if successful
        """
        return await self._request(
            "DELETE",
            "/v1/auths/api_key",
            model=bool,
        )

    async def get_api_key(self) -> ApiKey:
        """
        Get the current user's API key.

        Retrieves the existing API key for the current user.

        Returns:
            ApiKey: The current API key
        """
        return await self._request(
            "GET",
            "/v1/auths/api_key",
            model=ApiKey,
        )
