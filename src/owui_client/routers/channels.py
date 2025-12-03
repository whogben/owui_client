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
        """
        return await self._request(
            "GET",
            "/v1/channels/",
            model=ChannelListItemResponse,
        )

    async def list_all(self) -> List[ChannelModel]:
        """
        Get all channels (admin only or based on permissions).
        """
        return await self._request(
            "GET",
            "/v1/channels/list",
            model=ChannelModel,
        )

    async def get_dm_by_user(self, user_id: str) -> Optional[ChannelModel]:
        """
        Get or create a DM channel with a specific user.
        """
        return await self._request(
            "GET",
            f"/v1/channels/users/{user_id}",
            model=Optional[ChannelModel],
        )

    async def create(self, form_data: CreateChannelForm) -> Optional[ChannelModel]:
        """
        Create a new channel.
        """
        return await self._request(
            "POST",
            "/v1/channels/create",
            model=Optional[ChannelModel],
            json=form_data.model_dump(),
        )

    async def get(self, id: str) -> Optional[ChannelFullResponse]:
        """
        Get channel details by ID.
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

    async def update_member_active_status(
        self, id: str, is_active: bool
    ) -> bool:
        """
        Update the active status of the current user in the channel.
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
    ) -> list:
        """
        Add members to a channel.
        """
        form = UpdateMembersForm(user_ids=user_ids, group_ids=group_ids)
        # The backend returns a list of ChannelMember objects (implied by logic, though router says return memberships)
        # But the router signature is just generic return in some places or specific.
        # Backend: return [ChannelMemberModel.model_validate(membership) ...]
        # So it returns a list. I'll leave it as list for now or generic.
        return await self._request(
            "POST",
            f"/v1/channels/{id}/update/members/add",
            json=form.model_dump(),
        )

    async def remove_members(self, id: str, user_ids: List[str]) -> int:
        """
        Remove members from a channel. Returns number of deleted members.
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
        """
        return await self._request(
            "POST",
            f"/v1/channels/{id}/messages/post",
            model=Optional[MessageModel],
            json=form_data.model_dump(),
        )

    async def get_message(self, id: str, message_id: str) -> Optional[MessageUserResponse]:
        """
        Get a specific message by ID.
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
        """
        return await self._request(
            "POST",
            f"/v1/channels/{id}/messages/{message_id}/update",
            model=Optional[MessageModel],
            json=form_data.model_dump(),
        )

    async def add_reaction(
        self, id: str, message_id: str, reaction_name: str
    ) -> bool:
        """
        Add a reaction to a message.
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
        """
        return await self._request(
            "DELETE",
            f"/v1/channels/{id}/messages/{message_id}/delete",
            model=bool,
        )

