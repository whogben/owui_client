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
    async def get_groups(self, share: Optional[bool] = None) -> list[GroupResponse]:
        """
        Get all groups.

        :param share: Filter by share status
        :return: List of groups
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

        :param form_data: The group creation information
        :return: The created group
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

        :param id: The group ID
        :return: The group
        """
        return await self._request(
            "GET",
            f"/v1/groups/id/{id}",
            model=GroupResponse,
        )

    async def export_group_by_id(self, id: str) -> Optional[GroupExportResponse]:
        """
        Export group by ID (includes user IDs).

        :param id: The group ID
        :return: The exported group details
        """
        return await self._request(
            "GET",
            f"/v1/groups/id/{id}/export",
            model=GroupExportResponse,
        )

    async def get_users_in_group(self, id: str) -> list[UserInfoResponse]:
        """
        Get users in a group.

        :param id: The group ID
        :return: List of users in the group
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

        :param id: The group ID
        :param form_data: The group update information
        :return: The updated group
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

        :param id: The group ID
        :param form_data: The users to add
        :return: The updated group
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

        :param id: The group ID
        :param form_data: The users to remove
        :return: The updated group
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

        :param id: The group ID
        :return: True if successful
        """
        return await self._request(
            "DELETE",
            f"/v1/groups/id/{id}/delete",
            model=bool,
        )
