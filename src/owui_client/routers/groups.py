from typing import Optional
from owui_client.client_base import ResourceBase
from owui_client.models.groups import (
    GroupResponse,
    GroupExportResponse,
    GroupForm,
    GroupUpdateForm,
    UserIdsForm,
)
from owui_client.models.users import UserInfoResponse


class GroupsClient(ResourceBase):
    """
    Client for the Groups endpoints.
    """

    async def get_groups(self, share: Optional[bool] = None) -> list[GroupResponse]:
        """
        Get all groups.

        Retrieves a list of all groups available to the user.
        Admin users can see all groups. Regular users only see groups they are members of.

        Args:
            share: Filter by share status.
                   If True, returns only shared groups.
                   If False, returns only non-shared groups.
                   If None, returns all groups (subject to user role).

        Returns:
            List of groups.
        """
        params = {}
        if share is not None:
            params["share"] = share

        return await self._request(
            "GET",
            "/v1/groups/",
            model=GroupResponse,
            params=params,
        )

    async def create_new_group(self, form_data: GroupForm) -> Optional[GroupResponse]:
        """
        Create a new group.

        Creates a new user group with the provided details.
        Requires admin privileges.

        Args:
            form_data: The group creation information including name, description, and permissions.

        Returns:
            The created group if successful, None otherwise.
        """
        return await self._request(
            "POST",
            "/v1/groups/create",
            model=GroupResponse,
            json=form_data.model_dump(),
        )

    async def get_group_by_id(self, id: str) -> Optional[GroupResponse]:
        """
        Get group by ID.

        Retrieves details of a specific group by its ID.
        Requires admin privileges.

        Args:
            id: The unique identifier of the group.

        Returns:
            The group details if found, None otherwise.
        """
        return await self._request(
            "GET",
            f"/v1/groups/id/{id}",
            model=GroupResponse,
        )

    async def export_group_by_id(self, id: str) -> Optional[GroupExportResponse]:
        """
        Export group by ID (includes user IDs).

        Retrieves group details along with the list of member user IDs.
        Useful for backing up or migrating group data.
        Requires admin privileges.

        Args:
            id: The unique identifier of the group.

        Returns:
            The exported group details including member user IDs if found, None otherwise.
        """
        return await self._request(
            "GET",
            f"/v1/groups/id/{id}/export",
            model=GroupExportResponse,
        )

    async def get_users_in_group(self, id: str) -> list[UserInfoResponse]:
        """
        Get users in a group.

        Retrieves the list of users who are members of the specified group.
        Requires admin privileges.

        Args:
            id: The unique identifier of the group.

        Returns:
            List of user information for members of the group.
        """
        return await self._request(
            "POST",
            f"/v1/groups/id/{id}/users",
            model=UserInfoResponse,
        )

    async def update_group_by_id(
        self, id: str, form_data: GroupUpdateForm
    ) -> Optional[GroupResponse]:
        """
        Update group by ID.

        Updates the details of an existing group.
        Requires admin privileges.

        Args:
            id: The unique identifier of the group.
            form_data: The updated group information.

        Returns:
            The updated group details if successful, None otherwise.
        """
        return await self._request(
            "POST",
            f"/v1/groups/id/{id}/update",
            model=GroupResponse,
            json=form_data.model_dump(),
        )

    async def add_user_to_group(
        self, id: str, form_data: UserIdsForm
    ) -> Optional[GroupResponse]:
        """
        Add users to group.

        Adds one or more users to the specified group.
        Requires admin privileges.

        Args:
            id: The unique identifier of the group.
            form_data: Form containing the list of user IDs to add.

        Returns:
            The updated group details if successful, None otherwise.
        """
        return await self._request(
            "POST",
            f"/v1/groups/id/{id}/users/add",
            model=GroupResponse,
            json=form_data.model_dump(),
        )

    async def remove_users_from_group(
        self, id: str, form_data: UserIdsForm
    ) -> Optional[GroupResponse]:
        """
        Remove users from group.

        Removes one or more users from the specified group.
        Requires admin privileges.

        Args:
            id: The unique identifier of the group.
            form_data: Form containing the list of user IDs to remove.

        Returns:
            The updated group details if successful, None otherwise.
        """
        return await self._request(
            "POST",
            f"/v1/groups/id/{id}/users/remove",
            model=GroupResponse,
            json=form_data.model_dump(),
        )

    async def delete_group_by_id(self, id: str) -> bool:
        """
        Delete group by ID.

        Permanently deletes the specified group.
        Requires admin privileges.

        Args:
            id: The unique identifier of the group.

        Returns:
            True if the group was successfully deleted, False otherwise.
        """
        return await self._request(
            "DELETE",
            f"/v1/groups/id/{id}/delete",
            model=bool,
        )
