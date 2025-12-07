from typing import List, Optional
from owui_client.client_base import ResourceBase
from owui_client.models.chats import (
    ChatModel,
    ChatForm,
    ChatsImportForm,
    ChatResponse,
    ChatTitleIdResponse,
    TagForm,
    TagFilterForm,
    MessageForm,
    EventForm,
    CloneForm,
    ChatFolderIdForm,
)
from owui_client.models.tags import TagModel


class ChatsClient(ResourceBase):
    """
    Client for the Chats endpoints.
    
    Manages chat conversations, including creating, retrieving, updating, and deleting chats,
    as well as managing chat history, tags, and sharing.
    """
    async def get_list(
        self,
        page: Optional[int] = None,
        include_pinned: Optional[bool] = False,
        include_folders: Optional[bool] = False,
    ) -> List[ChatTitleIdResponse]:
        """
        Get a list of chats for the current user.

        Args:
            page: Page number for pagination. If None, returns all chats.
            include_pinned: Whether to include pinned chats in the response.
            include_folders: Whether to include chats that are inside folders.

        Returns:
            List of chat titles and IDs.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if include_pinned:
            params["include_pinned"] = include_pinned
        if include_folders:
            params["include_folders"] = include_folders
            
        return await self._request(
            "GET", "/v1/chats/", model=ChatTitleIdResponse, params=params
        )

    async def delete_all(self) -> bool:
        """
        Delete all chats for the current user.
        
        Returns:
            True if successful.
        """
        return await self._request("DELETE", "/v1/chats/", model=bool)

    async def get_user_list(
        self,
        user_id: str,
        page: Optional[int] = None,
        query: Optional[str] = None,
        order_by: Optional[str] = None,
        direction: Optional[str] = None,
    ) -> List[ChatTitleIdResponse]:
        """
        Get a list of chats for a specific user (Admin only).

        Args:
            user_id: ID of the user to fetch chats for.
            page: Page number for pagination.
            query: Search query for filtering chats.
            order_by: Field to order by.
            direction: Sort direction ('asc' or 'desc').

        Returns:
            List of chat titles and IDs.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if query:
            params["query"] = query
        if order_by:
            params["order_by"] = order_by
        if direction:
            params["direction"] = direction

        return await self._request(
            "GET", f"/v1/chats/list/user/{user_id}", model=ChatTitleIdResponse, params=params
        )

    async def create_new(self, form_data: ChatForm) -> Optional[ChatResponse]:
        """
        Create a new chat.

        Args:
            form_data: The initial data for the chat.

        Returns:
            The created chat object.
        """
        return await self._request(
            "POST", "/v1/chats/new", model=ChatResponse, json=form_data.model_dump()
        )

    async def import_chats(self, form_data: ChatsImportForm) -> List[ChatResponse]:
        """
        Import multiple chats.

        Args:
            form_data: The list of chats to import.

        Returns:
            List of successfully imported chat objects.
        """
        return await self._request(
            "POST", "/v1/chats/import", model=ChatResponse, json=form_data.model_dump()
        )

    async def search(
        self, text: str, page: Optional[int] = None
    ) -> List[ChatTitleIdResponse]:
        """
        Search for chats.

        Args:
            text: The search query text.
            page: Page number for pagination.

        Returns:
            List of chats matching the search query.
        """
        params = {"text": text}
        if page is not None:
            params["page"] = page
            
        return await self._request(
            "GET", "/v1/chats/search", model=ChatTitleIdResponse, params=params
        )

    async def get_by_folder_id(self, folder_id: str) -> List[ChatResponse]:
        """
        Get all chats in a specific folder.

        Args:
            folder_id: ID of the folder.

        Returns:
            List of full chat objects.
        """
        return await self._request(
            "GET", f"/v1/chats/folder/{folder_id}", model=ChatResponse
        )

    async def get_list_by_folder_id(
        self, folder_id: str, page: Optional[int] = 1
    ) -> List[dict]:
        """
        Get a paginated list of chats in a folder.

        Args:
            folder_id: ID of the folder.
            page: Page number for pagination.

        Returns:
            List of dictionaries containing basic chat info (id, title, updated_at).
        """
        params = {}
        if page is not None:
            params["page"] = page
            
        return await self._request(
            "GET", f"/v1/chats/folder/{folder_id}/list", model=dict, params=params
        )

    async def get_pinned(self) -> List[ChatTitleIdResponse]:
        """
        Get all pinned chats for the current user.

        Returns:
            List of pinned chats.
        """
        return await self._request("GET", "/v1/chats/pinned", model=ChatTitleIdResponse)

    async def get_all(self) -> List[ChatResponse]:
        """
        Get all chats for the current user.

        Returns:
            List of all chat objects.
        """
        return await self._request("GET", "/v1/chats/all", model=ChatResponse)

    async def get_all_archived(self) -> List[ChatResponse]:
        """
        Get all archived chats for the current user.

        Returns:
            List of archived chat objects.
        """
        return await self._request("GET", "/v1/chats/all/archived", model=ChatResponse)

    async def get_all_tags(self) -> List[TagModel]:
        """
        Get all tags used by the current user across all chats.

        Returns:
            List of tag objects.
        """
        return await self._request("GET", "/v1/chats/all/tags", model=TagModel)

    async def get_all_db(self) -> List[ChatResponse]:
        """
        Get all chats in the database (Admin only).

        Returns:
            List of all chat objects for all users.
        """
        return await self._request("GET", "/v1/chats/all/db", model=ChatResponse)

    async def get_archived_list(
        self,
        page: Optional[int] = None,
        query: Optional[str] = None,
        order_by: Optional[str] = None,
        direction: Optional[str] = None,
    ) -> List[ChatTitleIdResponse]:
        """
        Get a paginated list of archived chats.

        Args:
            page: Page number for pagination.
            query: Search query string.
            order_by: Field to order results by.
            direction: Sort direction ('asc' or 'desc').

        Returns:
            List of archived chats (lightweight).
        """
        params = {}
        if page is not None:
            params["page"] = page
        if query:
            params["query"] = query
        if order_by:
            params["order_by"] = order_by
        if direction:
            params["direction"] = direction

        return await self._request(
            "GET", "/v1/chats/archived", model=ChatTitleIdResponse, params=params
        )

    async def archive_all(self) -> bool:
        """
        Archive all chats for the current user.

        Returns:
            True if successful.
        """
        return await self._request("POST", "/v1/chats/archive/all", model=bool)

    async def unarchive_all(self) -> bool:
        """
        Unarchive all chats for the current user.

        Returns:
            True if successful.
        """
        return await self._request("POST", "/v1/chats/unarchive/all", model=bool)

    async def get_shared(self, share_id: str) -> Optional[ChatResponse]:
        """
        Get a shared chat.

        Args:
            share_id: The unique identifier for the shared chat.

        Returns:
            The shared chat object.
        """
        return await self._request(
            "GET", f"/v1/chats/share/{share_id}", model=ChatResponse
        )

    async def get_by_tags(self, form_data: TagFilterForm) -> List[ChatTitleIdResponse]:
        """
        Get chats filtered by tags.

        Args:
            form_data: Filter options including the tag name and pagination.

        Returns:
            List of chats matching the tag.
        """
        return await self._request(
            "POST", "/v1/chats/tags", model=ChatTitleIdResponse, json=form_data.model_dump()
        )

    async def get(self, id: str) -> Optional[ChatResponse]:
        """
        Get a chat by ID.

        Args:
            id: The chat ID.

        Returns:
            The chat object.
        """
        return await self._request("GET", f"/v1/chats/{id}", model=ChatResponse)

    async def update(self, id: str, form_data: ChatForm) -> Optional[ChatResponse]:
        """
        Update a chat.

        Args:
            id: The chat ID.
            form_data: The new chat data.

        Returns:
            The updated chat object.
        """
        return await self._request(
            "POST", f"/v1/chats/{id}", model=ChatResponse, json=form_data.model_dump()
        )

    async def update_message(
        self, id: str, message_id: str, form_data: MessageForm
    ) -> Optional[ChatResponse]:
        """
        Update a specific message content within a chat.

        Args:
            id: The chat ID.
            message_id: The message ID.
            form_data: The new message content.

        Returns:
            The updated chat object.
        """
        return await self._request(
            "POST",
            f"/v1/chats/{id}/messages/{message_id}",
            model=ChatResponse,
            json=form_data.model_dump(),
        )

    async def send_message_event(
        self, id: str, message_id: str, form_data: EventForm
    ) -> Optional[bool]:
        """
        Send a socket event related to a message.

        Args:
            id: The chat ID.
            message_id: The message ID.
            form_data: The event details.

        Returns:
            True if successful.
        """
        return await self._request(
            "POST",
            f"/v1/chats/{id}/messages/{message_id}/event",
            model=bool,
            json=form_data.model_dump(),
        )

    async def delete(self, id: str) -> bool:
        """
        Delete a chat.

        Args:
            id: The chat ID.

        Returns:
            True if successful.
        """
        return await self._request("DELETE", f"/v1/chats/{id}", model=bool)

    async def get_pinned_status(self, id: str) -> Optional[bool]:
        """
        Get the pinned status of a chat.

        Args:
            id: The chat ID.

        Returns:
            True if pinned, False otherwise.
        """
        return await self._request("GET", f"/v1/chats/{id}/pinned", model=bool)

    async def pin(self, id: str) -> Optional[ChatResponse]:
        """
        Toggle the pinned status of a chat.

        Args:
            id: The chat ID.

        Returns:
            The updated chat object.
        """
        return await self._request("POST", f"/v1/chats/{id}/pin", model=ChatResponse)

    async def clone(self, id: str, form_data: CloneForm) -> Optional[ChatResponse]:
        """
        Clone a chat.

        Args:
            id: The ID of the chat to clone.
            form_data: Cloning options (e.g. new title).

        Returns:
            The new chat object.
        """
        return await self._request(
            "POST", f"/v1/chats/{id}/clone", model=ChatResponse, json=form_data.model_dump()
        )

    async def clone_shared(self, id: str) -> Optional[ChatResponse]:
        """
        Clone a shared chat.

        Args:
            id: The share ID of the shared chat.

        Returns:
            The newly created chat object.
        """
        return await self._request("POST", f"/v1/chats/{id}/clone/shared", model=ChatResponse)

    async def archive(self, id: str) -> Optional[ChatResponse]:
        """
        Toggle the archived status of a chat.

        Args:
            id: The chat ID.

        Returns:
            The updated chat object.
        """
        return await self._request("POST", f"/v1/chats/{id}/archive", model=ChatResponse)

    async def share(self, id: str) -> Optional[ChatResponse]:
        """
        Share a chat.

        Generates or updates the share ID for the chat.

        Args:
            id: The chat ID.

        Returns:
            The updated chat object containing the share_id.
        """
        return await self._request("POST", f"/v1/chats/{id}/share", model=ChatResponse)

    async def delete_shared(self, id: str) -> Optional[bool]:
        """
        Unshare a chat (delete the shared link).

        Args:
            id: The chat ID.

        Returns:
            True if successful.
        """
        return await self._request("DELETE", f"/v1/chats/{id}/share", model=bool)

    async def update_folder(
        self, id: str, form_data: ChatFolderIdForm
    ) -> Optional[ChatResponse]:
        """
        Move a chat to a folder.

        Args:
            id: The chat ID.
            form_data: The target folder ID.

        Returns:
            The updated chat object.
        """
        return await self._request(
            "POST", f"/v1/chats/{id}/folder", model=ChatResponse, json=form_data.model_dump()
        )

    async def get_tags(self, id: str) -> List[TagModel]:
        """
        Get tags for a chat.

        Args:
            id: The chat ID.

        Returns:
            List of tags associated with the chat.
        """
        return await self._request("GET", f"/v1/chats/{id}/tags", model=TagModel)

    async def add_tag(self, id: str, form_data: TagForm) -> List[TagModel]:
        """
        Add a tag to a chat.

        Args:
            id: The chat ID.
            form_data: The tag to add.

        Returns:
            Updated list of tags for the chat.
        """
        return await self._request(
            "POST", f"/v1/chats/{id}/tags", model=TagModel, json=form_data.model_dump()
        )

    async def delete_tag(self, id: str, form_data: TagForm) -> List[TagModel]:
        """
        Remove a tag from a chat.

        Args:
            id: The chat ID.
            form_data: The tag to remove.

        Returns:
            Updated list of tags for the chat.
        """
        return await self._request(
            "DELETE", f"/v1/chats/{id}/tags", model=TagModel, json=form_data.model_dump()
        )

    async def delete_all_tags(self, id: str) -> Optional[bool]:
        """
        Remove all tags from a chat.

        Args:
            id: The chat ID.

        Returns:
            True if successful.
        """
        return await self._request("DELETE", f"/v1/chats/{id}/tags/all", model=bool)

