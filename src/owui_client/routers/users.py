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
    """
    Client for User management endpoints.

    This client handles operations related to user accounts, profiles, settings,
    permissions, and groups.
    """

    async def get_users(
        self,
        query: Optional[str] = None,
        order_by: Optional[str] = None,
        direction: Optional[str] = None,
        page: Optional[int] = 1,
    ) -> UserGroupIdsListResponse:
        """
        Get users with pagination and filtering.

        This endpoint is typically used by admins to manage users.
        Note: While the backend model layer supports complex filtering (e.g., by channel_id, user_ids),
        this endpoint currently only exposes query, order_by, direction, and page.

        Args:
            query: Search query for name or email.
            order_by: Field to order by (e.g., 'name', 'email', 'created_at', 'last_active_at', 'updated_at', 'role').
            direction: Sort direction ('asc' or 'desc').
            page: Page number (starts at 1).

        Returns:
            UserGroupIdsListResponse: List of users with group IDs and total count.
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

        Retrieves a list of all users with basic information.
        This is an admin-only endpoint.

        Returns:
            UserInfoListResponse: List of all users with basic info.
        """
        return await self._request(
            "GET",
            "/v1/users/all",
            model=UserInfoListResponse,
        )

    async def search_users(self, query: Optional[str] = None) -> UserIdNameListResponse:
        """
        Search users by query (name or email).

        Searches for users matching the query string.
        Returns the first page of results (limit 30).

        Args:
            query: Search query string.

        Returns:
            UserIdNameListResponse: List of users (ID and name) matching the query.
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

        Returns:
            List[GroupModel]: List of groups the user is a member of.
        """
        return await self._request(
            "GET",
            "/v1/users/groups",
            model=GroupModel,
        )

    async def get_user_permissions(self) -> Dict:
        """
        Get the current user's permissions.

        Returns:
            Dict: Dictionary of user permissions (workspace, sharing, chat, features).
        """
        return await self._request(
            "GET",
            "/v1/users/permissions",
        )

    async def get_default_user_permissions(self) -> UserPermissions:
        """
        Get the default user permissions.

        This is an admin-only endpoint.

        Returns:
            UserPermissions: Default user permissions.
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

        This is an admin-only endpoint.

        Args:
            permissions: The new default permissions.

        Returns:
            UserPermissions: The updated default permissions.
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

        Returns:
            Optional[UserSettings]: User settings if available.
        """
        return await self._request(
            "GET",
            "/v1/users/user/settings",
            model=Optional[UserSettings],
        )

    async def update_user_settings(self, settings: UserSettings) -> UserSettings:
        """
        Update the current session user's settings.

        Args:
            settings: The new user settings.

        Returns:
            UserSettings: The updated user settings.
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

        Returns:
            UserModel: The user model which includes status fields.
        """
        return await self._request(
            "GET",
            "/v1/users/user/status",
            model=UserModel,
        )

    async def update_user_status(self, status: UserStatus) -> UserModel:
        """
        Update the current session user's status.

        Args:
            status: The new user status.

        Returns:
            UserModel: The updated user model.
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

        This returns extra info stored in the user's 'info' JSON field.

        Returns:
            Optional[Dict[str, Any]]: User info dictionary.
        """
        return await self._request(
            "GET",
            "/v1/users/user/info",
        )

    async def update_user_info(self, info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update the current session user's info.

        Merges the provided dictionary with the existing info.

        Args:
            info: The new info dictionary to merge/update.

        Returns:
            Optional[Dict[str, Any]]: The updated user info dictionary.
        """
        return await self._request(
            "POST",
            "/v1/users/user/info/update",
            json=info,
        )

    async def get_user_by_id(self, user_id: str) -> UserActiveResponse:
        """
        Get a user by ID.

        Args:
            user_id: The ID of the user.

        Returns:
            UserActiveResponse: User info including active status.
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

        This is an admin-only endpoint. It can be used to update user details including
        role and password.

        Args:
            user_id: The ID of the user to update.
            form_data: The update form data.

        Returns:
            UserModel: The updated user model.
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

        This is an admin-only endpoint.

        Args:
            user_id: The ID of the user to delete.

        Returns:
            bool: True if successful.
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

        This is an admin-only endpoint.

        Args:
            user_id: The ID of the user.

        Returns:
            List[OAuthSessionModel]: List of OAuth sessions.
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

        Args:
            user_id: The ID of the user.

        Returns:
            bytes: Image content.
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

        Args:
            user_id: The ID of the user.

        Returns:
            Dict[str, bool]: Dictionary with 'active' status key.
        """
        return await self._request(
            "GET",
            f"/v1/users/{user_id}/active",
        )

    async def get_user_groups_by_id(self, user_id: str) -> List[GroupModel]:
        """
        Get the groups a user belongs to by user ID.

        This is an admin-only endpoint.

        Args:
            user_id: The ID of the user.

        Returns:
            List[GroupModel]: List of groups.
        """
        return await self._request(
            "GET",
            f"/v1/users/{user_id}/groups",
            model=GroupModel,
        )
