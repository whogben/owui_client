from typing import List, Optional, Union
from owui_client.client_base import ResourceBase
from owui_client.models.chats import (
    ChatModel,
    ChatForm,
    ChatsImportForm,
    ChatResponse,
    ChatTitleIdResponse,
    ChatUsageStatsListResponse,
    TagForm,
    TagFilterForm,
    MessageForm,
    EventForm,
    CloneForm,
    ChatFolderIdForm,
    ChatAccessGrantsForm,
    ChatStatsExport,
    ChatStatsExportList,
    ChatCompletionForm,
    ChatCompletionResponse,
    ChatCompletedForm,
    ChatCompletedResponse,
    ChatActionForm,
    ChatActionResponse,
)
from owui_client.models.tags import TagModel
from owui_client.models.access_grants import AccessGrantResponse


class ChatsClient(ResourceBase):
    """
    Client for the Chats endpoints.
    
    Manages chat conversations, including creating, retrieving, updating, and deleting chats,
    as well as managing chat history, tags, and sharing.
    """
    async def get_chat_usage_stats(
        self,
        items_per_page: Optional[int] = 50,
        page: Optional[int] = 1,
    ) -> ChatUsageStatsListResponse:
        """
        Get chat usage statistics.

        Args:
            items_per_page: Number of items per page (default 50).
            page: The page number to retrieve (default 1).

        Returns:
            `ChatUsageStatsListResponse`: A list of chat usage statistics.
        """
        params = {}
        if items_per_page:
            params["items_per_page"] = items_per_page
        if page:
            params["page"] = page

        return await self._request(
            "GET",
            "/v1/chats/stats/usage",
            model=ChatUsageStatsListResponse,
            params=params,
        )

    async def export_chat_stats(
        self,
        updated_at: Optional[int] = None,
        page: Optional[int] = 1,
    ) -> ChatStatsExportList:
        """
        Export chat statistics.

        Args:
            updated_at: Filter by updated_at timestamp.
            page: Page number for pagination.

        Returns:
            List of exported chat statistics.
        """
        params = {}
        if updated_at is not None:
            params["updated_at"] = updated_at
        if page is not None:
            params["page"] = page

        return await self._request(
            "GET", "/v1/chats/stats/export", model=ChatStatsExportList, params=params
        )

    async def export_single_chat_stats(
        self,
        chat_id: str,
    ) -> Optional[ChatStatsExport]:
        """
        Export statistics for a single chat.

        Args:
            chat_id: The ID of the chat.

        Returns:
            Exported statistics for the chat.
        """
        return await self._request(
            "GET", f"/v1/chats/stats/export/{chat_id}", model=ChatStatsExport
        )

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

    async def update_shared_access(
        self, id: str, form_data: ChatAccessGrantsForm
    ) -> Optional[ChatResponse]:
        """Update access grants for a shared chat.

        Sets the access control list for a shared chat, determining which users
        and groups can read or write to it.

        Args:
            id: The chat ID.
            form_data: The access grants to set.

        Returns:
            The updated chat object.
        """
        return await self._request(
            "POST",
            f"/v1/chats/shared/{id}/access/update",
            model=ChatResponse,
            json=form_data.model_dump(),
        )

    async def get_shared_access(self, id: str) -> List[AccessGrantResponse]:
        """Get access grants for a shared chat.

        Args:
            id: The chat ID.

        Returns:
            List of access grants for the shared chat.
        """
        return await self._request(
            "GET", f"/v1/chats/shared/{id}/access", model=AccessGrantResponse
        )

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

    async def chat_completion(
        self, form_data: Union[ChatCompletionForm, dict]
    ) -> Union[ChatCompletionResponse, dict]:
        """
        Generate a chat completion.

        This endpoint provides OpenAI-compatible chat completion functionality with
        Open WebUI-specific features like chat management, file attachments, tools,
        and async processing. The response format depends on whether a session_id
        is provided in the request.

        Args:
            form_data: The chat completion request containing messages, model ID,
                and optional parameters like chat_id, session_id, files, tools, etc.
                Can be a `ChatCompletionForm` or a dict.

        Returns:
            If session_id is provided: Returns a dict with `status` and `task_id`
            for async processing. The task can be queried for completion status.

            If session_id is not provided: Returns the completion response directly,
            which may be a streaming response or a complete response object depending
            on the `stream` parameter.

        Notes:
            - When `session_id` is provided, the request is processed asynchronously
              and returns immediately with a task_id.
            - When `chat_id` is provided, the completion is associated with an existing
              chat and the message is stored in the chat history.
            - The endpoint supports OpenAI-compatible parameters like temperature,
              max_tokens, top_p, etc., which are passed through to the model.
            - File attachments, tools, and retrieval filters can be included for
              enhanced functionality.
        """
        # Convert ChatCompletionForm to dict if needed
        if isinstance(form_data, ChatCompletionForm):
            json_data = form_data.model_dump()
        else:
            json_data = form_data

        return await self._request(
            "POST",
            "/chat/completions",
            model=ChatCompletionResponse,
            json=json_data,
        )

    async def chat_completion_api(
        self, form_data: Union[ChatCompletionForm, dict]
    ) -> Union[ChatCompletionResponse, dict]:
        """
        Generate a chat completion (direct API endpoint).

        This is the legacy endpoint from main.py that provides chat completion functionality.

        Args:
            form_data: The chat completion request containing messages, model ID,
                and optional parameters.

        Returns:
            Chat completion response.
        """
        if isinstance(form_data, ChatCompletionForm):
            json_data = form_data.model_dump()
        else:
            json_data = form_data

        return await self._request(
            "POST",
            "/api/chat/completions",
            model=ChatCompletionResponse,
            json=json_data,
        )

    async def chat_completed(
        self, form_data: Union[ChatCompletedForm, dict]
    ) -> Union[ChatCompletedResponse, dict]:
        """
        Notify that a chat completion has been generated.

        This endpoint is called after a chat completion is generated to process
        outlet filters that may modify the response. Outlet filters can transform
        the message content, add metadata, or perform other post-processing operations.

        Args:
            form_data: The completed chat data containing model ID, message IDs,
                chat ID, session ID, and optional filter IDs. Can be a `ChatCompletedForm`
                or a dict.

        Returns:
            The modified form data after processing outlet filters. The response
            structure matches the request form but may be modified by filters.

        Notes:
            - This endpoint processes outlet filters in the order defined by the model
            - Filters can modify the message content, add metadata, or perform other transformations
            - The endpoint requires authentication and the user must have access to the chat
            - If model_item with direct=True is provided, it bypasses the model registry
        """
        # Convert ChatCompletedForm to dict if needed
        if isinstance(form_data, ChatCompletedForm):
            json_data = form_data.model_dump()
        else:
            json_data = form_data

        return await self._request(
            "POST",
            "/chat/completed",
            model=ChatCompletedResponse,
            json=json_data,
        )

    async def chat_completed_api(
        self, form_data: Union[ChatCompletedForm, dict]
    ) -> Union[ChatCompletedResponse, dict]:
        """
        Notify that a chat completion has been generated (direct API endpoint).

        This is the legacy endpoint from main.py for processing outlet filters.

        Args:
            form_data: The completed chat data.

        Returns:
            Modified form data after processing outlet filters.
        """
        if isinstance(form_data, ChatCompletedForm):
            json_data = form_data.model_dump()
        else:
            json_data = form_data

        return await self._request(
            "POST",
            "/api/chat/completed",
            model=ChatCompletedResponse,
            json=json_data,
        )

    async def chat_action(
        self, action_id: str, form_data: Union[ChatActionForm, dict]
    ) -> Union[ChatActionResponse, dict]:
        """
        Execute a chat action (POST /api/chat/actions/{action_id}).

        This endpoint triggers custom actions (functions) that can process chat messages
        and return results. Actions are user-defined functions that can perform arbitrary
        operations on chat data, such as processing messages, generating content,
        or interacting with external services.

        Args:
            action_id: The ID of the action function to execute. Can include a sub-action
                ID separated by a dot (e.g., "action_id.sub_action_id").
            form_data: The action request containing model ID, message IDs, chat ID,
                session ID, and optional model configuration. Can be a `ChatActionForm` or a dict.

        Returns:
            The result of executing the action function. The response structure varies
            based on the action function being executed. Actions can return any data type,
            so the response may be a dict, list, string, or other types.

        Notes:
            - Actions are user-defined functions registered in the Open WebUI system
            - The action_id can include a sub-action ID separated by a dot for nested actions
            - If model_item with direct=True is provided, it bypasses the model registry
            - The action function receives context including the model, user, and event emitters
            - Actions can emit socket events to update the UI in real-time
            - Actions can return HTML responses or other rich content for display
        """
        # Convert ChatActionForm to dict if needed
        if isinstance(form_data, ChatActionForm):
            json_data = form_data.model_dump()
        else:
            json_data = form_data

        return await self._request(
            "POST",
            f"/chat/actions/{action_id}",
            model=ChatActionResponse,
            json=json_data,
        )

