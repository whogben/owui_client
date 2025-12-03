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
    async def get_list(
        self,
        page: Optional[int] = None,
        include_pinned: Optional[bool] = False,
        include_folders: Optional[bool] = False,
    ) -> List[ChatTitleIdResponse]:
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
        return await self._request("DELETE", "/v1/chats/", model=bool)

    async def get_user_list(
        self,
        user_id: str,
        page: Optional[int] = None,
        query: Optional[str] = None,
        order_by: Optional[str] = None,
        direction: Optional[str] = None,
    ) -> List[ChatTitleIdResponse]:
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
        return await self._request(
            "POST", "/v1/chats/new", model=ChatResponse, json=form_data.model_dump()
        )

    async def import_chats(self, form_data: ChatsImportForm) -> List[ChatResponse]:
        return await self._request(
            "POST", "/v1/chats/import", model=ChatResponse, json=form_data.model_dump()
        )

    async def search(
        self, text: str, page: Optional[int] = None
    ) -> List[ChatTitleIdResponse]:
        params = {"text": text}
        if page is not None:
            params["page"] = page
            
        return await self._request(
            "GET", "/v1/chats/search", model=ChatTitleIdResponse, params=params
        )

    async def get_by_folder_id(self, folder_id: str) -> List[ChatResponse]:
        return await self._request(
            "GET", f"/v1/chats/folder/{folder_id}", model=ChatResponse
        )

    async def get_list_by_folder_id(
        self, folder_id: str, page: Optional[int] = 1
    ) -> List[dict]:
        params = {}
        if page is not None:
            params["page"] = page
            
        return await self._request(
            "GET", f"/v1/chats/folder/{folder_id}/list", model=dict, params=params
        )

    async def get_pinned(self) -> List[ChatTitleIdResponse]:
        return await self._request("GET", "/v1/chats/pinned", model=ChatTitleIdResponse)

    async def get_all(self) -> List[ChatResponse]:
        return await self._request("GET", "/v1/chats/all", model=ChatResponse)

    async def get_all_archived(self) -> List[ChatResponse]:
        return await self._request("GET", "/v1/chats/all/archived", model=ChatResponse)

    async def get_all_tags(self) -> List[TagModel]:
        return await self._request("GET", "/v1/chats/all/tags", model=TagModel)

    async def get_all_db(self) -> List[ChatResponse]:
        return await self._request("GET", "/v1/chats/all/db", model=ChatResponse)

    async def get_archived_list(
        self,
        page: Optional[int] = None,
        query: Optional[str] = None,
        order_by: Optional[str] = None,
        direction: Optional[str] = None,
    ) -> List[ChatTitleIdResponse]:
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
        return await self._request("POST", "/v1/chats/archive/all", model=bool)

    async def unarchive_all(self) -> bool:
        return await self._request("POST", "/v1/chats/unarchive/all", model=bool)

    async def get_shared(self, share_id: str) -> Optional[ChatResponse]:
        return await self._request(
            "GET", f"/v1/chats/share/{share_id}", model=ChatResponse
        )

    async def get_by_tags(self, form_data: TagFilterForm) -> List[ChatTitleIdResponse]:
        return await self._request(
            "POST", "/v1/chats/tags", model=ChatTitleIdResponse, json=form_data.model_dump()
        )

    async def get(self, id: str) -> Optional[ChatResponse]:
        return await self._request("GET", f"/v1/chats/{id}", model=ChatResponse)

    async def update(self, id: str, form_data: ChatForm) -> Optional[ChatResponse]:
        return await self._request(
            "POST", f"/v1/chats/{id}", model=ChatResponse, json=form_data.model_dump()
        )

    async def update_message(
        self, id: str, message_id: str, form_data: MessageForm
    ) -> Optional[ChatResponse]:
        return await self._request(
            "POST",
            f"/v1/chats/{id}/messages/{message_id}",
            model=ChatResponse,
            json=form_data.model_dump(),
        )

    async def send_message_event(
        self, id: str, message_id: str, form_data: EventForm
    ) -> Optional[bool]:
        return await self._request(
            "POST",
            f"/v1/chats/{id}/messages/{message_id}/event",
            model=bool,
            json=form_data.model_dump(),
        )

    async def delete(self, id: str) -> bool:
        return await self._request("DELETE", f"/v1/chats/{id}", model=bool)

    async def get_pinned_status(self, id: str) -> Optional[bool]:
        return await self._request("GET", f"/v1/chats/{id}/pinned", model=bool)

    async def pin(self, id: str) -> Optional[ChatResponse]:
        return await self._request("POST", f"/v1/chats/{id}/pin", model=ChatResponse)

    async def clone(self, id: str, form_data: CloneForm) -> Optional[ChatResponse]:
        return await self._request(
            "POST", f"/v1/chats/{id}/clone", model=ChatResponse, json=form_data.model_dump()
        )

    async def clone_shared(self, id: str) -> Optional[ChatResponse]:
        return await self._request("POST", f"/v1/chats/{id}/clone/shared", model=ChatResponse)

    async def archive(self, id: str) -> Optional[ChatResponse]:
        return await self._request("POST", f"/v1/chats/{id}/archive", model=ChatResponse)

    async def share(self, id: str) -> Optional[ChatResponse]:
        return await self._request("POST", f"/v1/chats/{id}/share", model=ChatResponse)

    async def delete_shared(self, id: str) -> Optional[bool]:
        return await self._request("DELETE", f"/v1/chats/{id}/share", model=bool)

    async def update_folder(
        self, id: str, form_data: ChatFolderIdForm
    ) -> Optional[ChatResponse]:
        return await self._request(
            "POST", f"/v1/chats/{id}/folder", model=ChatResponse, json=form_data.model_dump()
        )

    async def get_tags(self, id: str) -> List[TagModel]:
        return await self._request("GET", f"/v1/chats/{id}/tags", model=TagModel)

    async def add_tag(self, id: str, form_data: TagForm) -> List[TagModel]:
        return await self._request(
            "POST", f"/v1/chats/{id}/tags", model=TagModel, json=form_data.model_dump()
        )

    async def delete_tag(self, id: str, form_data: TagForm) -> List[TagModel]:
        return await self._request(
            "DELETE", f"/v1/chats/{id}/tags", model=TagModel, json=form_data.model_dump()
        )

    async def delete_all_tags(self, id: str) -> Optional[bool]:
        return await self._request("DELETE", f"/v1/chats/{id}/tags/all", model=bool)

