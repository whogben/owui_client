from typing import Optional, List, Dict, Any
from owui_client.client_base import ResourceBase
from owui_client.models.users import (
    UserGroupIdsListResponse,
    UserInfoListResponse,
    UserIdNameListResponse,
    UserPermissions,
    UserSettings,
    UserResponse,
    UserUpdateForm,
    UserModel,
    UserStatus,
    UserActiveResponse,
)
from owui_client.models.groups import GroupModel
from owui_client.models.oauth_sessions import OAuthSessionModel


class UsersClient(ResourceBase):
    async def get_users(
        self,
        query: Optional[str] = None,
        order_by: Optional[str] = None,
        direction: Optional[str] = None,
        page: Optional[int] = 1,
    ) -> UserGroupIdsListResponse:
        """
        Get users with pagination and filtering.

        :param query: Search query
        :param order_by: Field to order by
        :param direction: Sort direction ('asc' or 'desc')
        :param page: Page number (starts at 1)
        :return: List of users with group IDs and total count
        """
        params = {}
        if query:
            params["query"] = query
        if order_by:
            params["order_by"] = order_by
        if direction:
            params["direction"] = direction
        if page:
            params["page"] = page

        return await self._request(
            "GET",
            "/v1/users/",
            model=UserGroupIdsListResponse,
            params=params,
        )

    async def get_all_users(self) -> UserInfoListResponse:
        """
        Get all users (abbreviated info).

        :return: List of all users with basic info
        """
        return await self._request(
            "GET",
            "/v1/users/all",
            model=UserInfoListResponse,
        )

    async def search_users(self, query: Optional[str] = None) -> UserIdNameListResponse:
        """
        Search users by query (name or email).
        Always returns the first page of results.

        :param query: Search query
        :return: List of users (id and name)
        """
        params = {}
        if query:
            params["query"] = query

        return await self._request(
            "GET",
            "/v1/users/search",
            model=UserIdNameListResponse,
            params=params,
        )

    async def get_user_groups(self) -> List[GroupModel]:
        """
        Get the groups the current user belongs to.

        :return: List of groups
        """
        return await self._request(
            "GET",
            "/v1/users/groups",
            model=GroupModel,
        )

    async def get_user_permissions(self) -> Dict:
        """
        Get the current user's permissions.

        :return: Dictionary of user permissions
        """
        return await self._request(
            "GET",
            "/v1/users/permissions",
        )

    async def get_default_user_permissions(self) -> UserPermissions:
        """
        Get the default user permissions.

        :return: Default user permissions
        """
        return await self._request(
            "GET",
            "/v1/users/default/permissions",
            model=UserPermissions,
        )

    async def update_default_user_permissions(
        self, permissions: UserPermissions
    ) -> UserPermissions:
        """
        Update the default user permissions.

        :param permissions: The new default permissions
        :return: The updated default permissions
        """
        # Note: The backend returns the dict directly, but we can model validate it back to UserPermissions
        return await self._request(
            "POST",
            "/v1/users/default/permissions",
            model=UserPermissions,
            json=permissions.model_dump(),
        )

    async def get_user_settings(self) -> Optional[UserSettings]:
        """
        Get the current session user's settings.

        :return: User settings
        """
        return await self._request(
            "GET",
            "/v1/users/user/settings",
            model=Optional[UserSettings],
        )

    async def update_user_settings(self, settings: UserSettings) -> UserSettings:
        """
        Update the current session user's settings.

        :param settings: The new user settings
        :return: The updated user settings
        """
        return await self._request(
            "POST",
            "/v1/users/user/settings/update",
            model=UserSettings,
            json=settings.model_dump(),
        )

    async def get_user_status(self) -> UserModel:
        """
        Get the current session user's status.

        :return: The user model (which acts as the status in the backend response)
        """
        return await self._request(
            "GET",
            "/v1/users/user/status",
            model=UserModel,
        )

    async def update_user_status(self, status: UserStatus) -> UserModel:
        """
        Update the current session user's status.

        :param status: The new user status
        :return: The updated user model
        """
        return await self._request(
            "POST",
            "/v1/users/user/status/update",
            model=UserModel,
            json=status.model_dump(),
        )

    async def get_user_info(self) -> Optional[Dict[str, Any]]:
        """
        Get the current session user's info.

        :return: User info dictionary
        """
        return await self._request(
            "GET",
            "/v1/users/user/info",
        )

    async def update_user_info(self, info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update the current session user's info.

        :param info: The new info dictionary to merge/update
        :return: The updated user info dictionary
        """
        return await self._request(
            "POST",
            "/v1/users/user/info/update",
            json=info,
        )

    async def get_user_by_id(self, user_id: str) -> UserActiveResponse:
        """
        Get a user by ID.

        :param user_id: The ID of the user
        :return: User response with basic info
        """
        return await self._request(
            "GET",
            f"/v1/users/{user_id}",
            model=UserActiveResponse,
        )

    async def update_user_by_id(
        self, user_id: str, form_data: UserUpdateForm
    ) -> UserModel:
        """
        Update a user by ID.

        :param user_id: The ID of the user to update
        :param form_data: The update form data
        :return: The updated user model
        """
        return await self._request(
            "POST",
            f"/v1/users/{user_id}/update",
            model=UserModel,
            json=form_data.model_dump(),
        )

    async def delete_user_by_id(self, user_id: str) -> bool:
        """
        Delete a user by ID.

        :param user_id: The ID of the user to delete
        :return: True if successful
        """
        return await self._request(
            "DELETE",
            f"/v1/users/{user_id}",
            model=bool,
        )

    async def get_user_oauth_sessions_by_id(
        self, user_id: str
    ) -> List[OAuthSessionModel]:
        """
        Get OAuth sessions for a user by ID.

        :param user_id: The ID of the user
        :return: List of OAuth sessions
        """
        return await self._request(
            "GET",
            f"/v1/users/{user_id}/oauth/sessions",
            model=OAuthSessionModel,
        )

    async def get_user_profile_image_by_id(self, user_id: str) -> bytes:
        """
        Get a user's profile image by ID.
        Returns the image content (bytes).

        :param user_id: The ID of the user
        :return: Image bytes
        """
        return await self._request(
            "GET",
            f"/v1/users/{user_id}/profile/image",
            model=bytes,
            follow_redirects=True,
        )

    async def get_user_active_status_by_id(self, user_id: str) -> Dict[str, bool]:
        """
        Get a user's active status by ID.

        :param user_id: The ID of the user
        :return: Dictionary with 'active' status
        """
        return await self._request(
            "GET",
            f"/v1/users/{user_id}/active",
        )

    async def get_user_groups_by_id(self, user_id: str) -> List[GroupModel]:
        """
        Get the groups a user belongs to by user ID.

        :param user_id: The ID of the user
        :return: List of groups
        """
        return await self._request(
            "GET",
            f"/v1/users/{user_id}/groups",
            model=GroupModel,
        )
