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
    UserResponse,
    AddUserForm,
    SigninResponse,
    AdminDetails,
    LdapServerConfig,
    LdapConfigForm,
    LdapConfigResponse,
    ApiKey,
)
from owui_client.models.users import UpdateProfileForm


class AuthsClient(ResourceBase):
    async def get_session_user(self) -> SessionUserInfoResponse:
        """
        Get the current session user information.

        :return: Session user information
        """
        return await self._request(
            "GET",
            "/v1/auths/",
            model=SessionUserInfoResponse,
        )

    async def update_profile(self, form_data: UpdateProfileForm) -> UserResponse:
        """
        Update the current user's profile.

        :param form_data: The profile update information
        :return: Updated user information
        """
        return await self._request(
            "POST",
            "/v1/auths/update/profile",
            model=UserResponse,
            json=form_data.model_dump(),
        )

    async def update_password(self, form_data: UpdatePasswordForm) -> bool:
        """
        Update the current user's password.

        :param form_data: The password update information (current and new password)
        :return: True if successful
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

        :param form_data: The signin credentials (email, password)
        :param set_client_api_key: If True (default), updates the main client's API key upon success
        :return: Session information including token and user details
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

        :param form_data: The LDAP credentials (user, password)
        :param set_client_api_key: If True (default), updates the main client's API key upon success
        :return: Session information including token and user details
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

        :param form_data: The signup information (name, email, password, etc.)
        :param set_client_api_key: If True (default), updates the main client's API key upon success
        :return: Session information including token and user details
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

        :param form_data: The user information (name, email, password, role, etc.)
        :return: Response including token and user details
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

        :return: Admin details (name, email)
        """
        return await self._request(
            "GET",
            "/v1/auths/admin/details",
            model=AdminDetails,
        )

    async def sign_out(self, unset_client_api_key: bool = True) -> SignoutResponse:
        """
        Sign out the current user.

        :param unset_client_api_key: If True (default), clears the main client's API key upon success
        :return: Signout status
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

        :return: The admin configuration
        """
        return await self._request(
            "GET",
            "/v1/auths/admin/config",
            model=AdminConfig,
        )

    async def update_admin_config(self, config: AdminConfig) -> AdminConfig:
        """
        Update the admin configuration.

        :param config: The new configuration
        :return: The updated configuration
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

        :return: LDAP server configuration
        """
        return await self._request(
            "GET",
            "/v1/auths/admin/config/ldap/server",
            model=LdapServerConfig,
        )

    async def update_ldap_server(self, form_data: LdapServerConfig) -> LdapServerConfig:
        """
        Update the LDAP server configuration.

        :param form_data: The LDAP server configuration
        :return: Updated LDAP server configuration
        """
        return await self._request(
            "POST",
            "/v1/auths/admin/config/ldap/server",
            model=LdapServerConfig,
            json=form_data.model_dump(),
        )

    async def get_ldap_config(self) -> LdapConfigResponse:
        """
        Get the LDAP configuration (enable/disable status).

        :return: LDAP configuration status
        """
        return await self._request(
            "GET",
            "/v1/auths/admin/config/ldap",
            model=LdapConfigResponse,
        )

    async def update_ldap_config(self, form_data: LdapConfigForm) -> LdapConfigResponse:
        """
        Update the LDAP configuration (enable/disable status).

        :param form_data: The LDAP configuration form
        :return: Updated LDAP configuration status
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

        :return: The generated API key
        """
        return await self._request(
            "POST",
            "/v1/auths/api_key",
            model=ApiKey,
        )

    async def delete_api_key(self) -> bool:
        """
        Delete the current user's API key.

        :return: True if successful
        """
        return await self._request(
            "DELETE",
            "/v1/auths/api_key",
            model=bool,
        )

    async def get_api_key(self) -> ApiKey:
        """
        Get the current user's API key.

        :return: The current API key
        """
        return await self._request(
            "GET",
            "/v1/auths/api_key",
            model=ApiKey,
        )
