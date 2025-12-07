from typing import Optional, List
from owui_client.client_base import ResourceBase
from owui_client.models.channels import (
    ChannelListItemResponse,
    ChannelModel,
    CreateChannelForm,
    ChannelFullResponse,
    ChannelForm,
    UpdateActiveMemberForm,
    UpdateMembersForm,
    RemoveMembersForm,
    ChannelMemberModel,
)
from owui_client.models.messages import (
    MessageUserResponse,
    MessageWithReactionsResponse,
    MessageForm,
    MessageModel,
    ReactionForm,
)
from owui_client.models.users import UserListResponse


class ChannelsClient(ResourceBase):
    async def list(self) -> List[ChannelListItemResponse]:
        """
        Get list of channels for the current user.

        Returns:
            List[ChannelListItemResponse]: A list of channels with additional user stats (last message, unread count).
        """
        return await self._request(
            "GET",
            "/v1/channels/",
            model=ChannelListItemResponse,
        )

    async def list_all(self) -> List[ChannelModel]:
        """
        Get all channels available to the user.

        For admins, this returns all channels. For regular users, this returns channels they are a member of.

        Returns:
            List[ChannelModel]: A list of basic channel models.
        """
        return await self._request(
            "GET",
            "/v1/channels/list",
            model=ChannelModel,
        )

    async def get_dm_by_user(self, user_id: str) -> Optional[ChannelModel]:
        """
        Get or create a DM channel with a specific user.

        If a DM channel already exists, it is returned. If not, a new one is created.

        Args:
            user_id: The ID of the user to start a DM with.

        Returns:
            Optional[ChannelModel]: The DM channel model.
        """
        return await self._request(
            "GET",
            f"/v1/channels/users/{user_id}",
            model=Optional[ChannelModel],
        )

    async def create(self, form_data: CreateChannelForm) -> Optional[ChannelModel]:
        """
        Create a new channel.

        Args:
            form_data: The form data for creating the channel (name, type, members, etc.).

        Returns:
            Optional[ChannelModel]: The created channel model, or None if creation failed.
        """
        return await self._request(
            "POST",
            "/v1/channels/create",
            model=Optional[ChannelModel],
            json=form_data.model_dump(),
        )

    async def get(self, id: str) -> Optional[ChannelFullResponse]:
        """
        Get detailed channel information by ID.

        Args:
            id: The channel ID.

        Returns:
            Optional[ChannelFullResponse]: Detailed channel info including members and user permissions.
        """
        return await self._request(
            "GET",
            f"/v1/channels/{id}",
            model=Optional[ChannelFullResponse],
        )

    async def get_members(
        self,
        id: str,
        query: Optional[str] = None,
        order_by: Optional[str] = None,
        direction: Optional[str] = None,
        page: Optional[int] = 1,
    ) -> UserListResponse:
        """
        Get members of a channel.

        Args:
            id: The channel ID.
            query: Optional search query for filtering members.
            order_by: Field to order by.
            direction: Sort direction ('asc' or 'desc').
            page: Page number for pagination.

        Returns:
            UserListResponse: List of users and total count.
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
            f"/v1/channels/{id}/members",
            model=UserListResponse,
            params=params,
        )

    async def update_member_active_status(self, id: str, is_active: bool) -> bool:
        """
        Update the active status of the current user in the channel.

        Args:
            id: The channel ID.
            is_active: The new active status.

        Returns:
            bool: True if successful.
        """
        form = UpdateActiveMemberForm(is_active=is_active)
        return await self._request(
            "POST",
            f"/v1/channels/{id}/members/active",
            model=bool,
            json=form.model_dump(),
        )

    async def add_members(
        self, id: str, user_ids: List[str] = [], group_ids: List[str] = []
    ) -> List[ChannelMemberModel]:
        """
        Add members to a channel.

        Args:
            id: The channel ID.
            user_ids: List of user IDs to add.
            group_ids: List of group IDs to add.

        Returns:
            List[ChannelMemberModel]: List of added memberships.
        """
        form = UpdateMembersForm(user_ids=user_ids, group_ids=group_ids)
        return await self._request(
            "POST",
            f"/v1/channels/{id}/update/members/add",
            model=ChannelMemberModel,
            json=form.model_dump(),
        )

    async def remove_members(self, id: str, user_ids: List[str]) -> int:
        """
        Remove members from a channel.

        Args:
            id: The channel ID.
            user_ids: List of user IDs to remove.

        Returns:
            int: The number of members removed.
        """
        form = RemoveMembersForm(user_ids=user_ids)
        return await self._request(
            "POST",
            f"/v1/channels/{id}/update/members/remove",
            model=int,
            json=form.model_dump(),
        )

    async def update(self, id: str, form_data: ChannelForm) -> Optional[ChannelModel]:
        """
        Update a channel by ID.

        Args:
            id: The channel ID.
            form_data: The update form data.

        Returns:
            Optional[ChannelModel]: The updated channel model.
        """
        return await self._request(
            "POST",
            f"/v1/channels/{id}/update",
            model=Optional[ChannelModel],
            json=form_data.model_dump(),
        )

    async def delete(self, id: str) -> bool:
        """
        Delete a channel by ID.

        Args:
            id: The channel ID.

        Returns:
            bool: True if successful.
        """
        return await self._request(
            "DELETE",
            f"/v1/channels/{id}/delete",
            model=bool,
        )

    async def get_messages(
        self, id: str, skip: int = 0, limit: int = 50
    ) -> List[MessageUserResponse]:
        """
        Get messages from a channel.

        Args:
            id: The channel ID.
            skip: Number of messages to skip.
            limit: Number of messages to return.

        Returns:
            List[MessageUserResponse]: List of messages with user details.
        """
        params = {"skip": skip, "limit": limit}
        return await self._request(
            "GET",
            f"/v1/channels/{id}/messages",
            model=MessageUserResponse,
            params=params,
        )

    async def get_pinned_messages(
        self, id: str, page: int = 1
    ) -> List[MessageWithReactionsResponse]:
        """
        Get pinned messages from a channel.

        Args:
            id: The channel ID.
            page: Page number (1-based).

        Returns:
            List[MessageWithReactionsResponse]: List of pinned messages.
        """
        params = {"page": page}
        return await self._request(
            "GET",
            f"/v1/channels/{id}/messages/pinned",
            model=MessageWithReactionsResponse,
            params=params,
        )

    async def post_message(
        self, id: str, form_data: MessageForm
    ) -> Optional[MessageModel]:
        """
        Post a new message to a channel.

        Args:
            id: The channel ID.
            form_data: The message content and metadata.

        Returns:
            Optional[MessageModel]: The created message model.
        """
        return await self._request(
            "POST",
            f"/v1/channels/{id}/messages/post",
            model=Optional[MessageModel],
            json=form_data.model_dump(),
        )

    async def get_message(
        self, id: str, message_id: str
    ) -> Optional[MessageUserResponse]:
        """
        Get a specific message by ID.

        Args:
            id: The channel ID.
            message_id: The message ID.

        Returns:
            Optional[MessageUserResponse]: The message details.
        """
        return await self._request(
            "GET",
            f"/v1/channels/{id}/messages/{message_id}",
            model=Optional[MessageUserResponse],
        )

    async def pin_message(
        self, id: str, message_id: str, is_pinned: bool
    ) -> Optional[MessageUserResponse]:
        """
        Pin or unpin a message.

        Args:
            id: The channel ID.
            message_id: The message ID.
            is_pinned: True to pin, False to unpin.

        Returns:
            Optional[MessageUserResponse]: The updated message details.
        """
        return await self._request(
            "POST",
            f"/v1/channels/{id}/messages/{message_id}/pin",
            model=Optional[MessageUserResponse],
            json={"is_pinned": is_pinned},
        )

    async def get_thread_messages(
        self, id: str, message_id: str, skip: int = 0, limit: int = 50
    ) -> List[MessageUserResponse]:
        """
        Get thread messages for a specific message.

        Args:
            id: The channel ID.
            message_id: The parent message ID.
            skip: Number of messages to skip.
            limit: Number of messages to return.

        Returns:
            List[MessageUserResponse]: List of thread messages.
        """
        params = {"skip": skip, "limit": limit}
        return await self._request(
            "GET",
            f"/v1/channels/{id}/messages/{message_id}/thread",
            model=MessageUserResponse,
            params=params,
        )

    async def update_message(
        self, id: str, message_id: str, form_data: MessageForm
    ) -> Optional[MessageModel]:
        """
        Update a message.

        Args:
            id: The channel ID.
            message_id: The message ID.
            form_data: The update form data.

        Returns:
            Optional[MessageModel]: The updated message model.
        """
        return await self._request(
            "POST",
            f"/v1/channels/{id}/messages/{message_id}/update",
            model=Optional[MessageModel],
            json=form_data.model_dump(),
        )

    async def add_reaction(self, id: str, message_id: str, reaction_name: str) -> bool:
        """
        Add a reaction to a message.

        Args:
            id: The channel ID.
            message_id: The message ID.
            reaction_name: The name of the reaction (e.g. emoji or shortcode).

        Returns:
            bool: True if successful.
        """
        form = ReactionForm(name=reaction_name)
        return await self._request(
            "POST",
            f"/v1/channels/{id}/messages/{message_id}/reactions/add",
            model=bool,
            json=form.model_dump(),
        )

    async def remove_reaction(
        self, id: str, message_id: str, reaction_name: str
    ) -> bool:
        """
        Remove a reaction from a message.

        Args:
            id: The channel ID.
            message_id: The message ID.
            reaction_name: The name of the reaction to remove.

        Returns:
            bool: True if successful.
        """
        form = ReactionForm(name=reaction_name)
        return await self._request(
            "POST",
            f"/v1/channels/{id}/messages/{message_id}/reactions/remove",
            model=bool,
            json=form.model_dump(),
        )

    async def delete_message(self, id: str, message_id: str) -> bool:
        """
        Delete a message.

        Args:
            id: The channel ID.
            message_id: The message ID.

        Returns:
            bool: True if successful.
        """
        return await self._request(
            "DELETE",
            f"/v1/channels/{id}/messages/{message_id}/delete",
            model=bool,
        )
