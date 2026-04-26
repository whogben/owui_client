from typing import Optional, List
from owui_client.client_base import ResourceBase
from owui_client.models.notes import (
    NoteModel,
    NoteForm,
    NoteUserResponse,
    NoteItemResponse,
    NoteListResponse,
    NoteAccessGrantsForm,
)


class NotesClient(ResourceBase):
    """
    Client for the Notes endpoints.
    """

    async def get_notes(self) -> List[NoteItemResponse]:
        """
        Get all notes visible to the user.

        This endpoint returns a list of notes that the user has permission to view.
        If the user is an admin, they can see all notes.
        Otherwise, they can see their own notes and notes shared with them.

        Returns:
            A list of `NoteItemResponse` objects.
        """
        return await self._request(
            "GET",
            "/v1/notes/",
            model=NoteItemResponse,
        )

    async def get_pinned_notes(self) -> List[NoteItemResponse]:
        """
        Get pinned notes visible to the user.

        This endpoint returns a list of notes that the user has pinned.
        If the user is an admin, they can see all pinned notes.
        Otherwise, they can see their own pinned notes and pinned notes shared with them.

        Returns:
            A list of `NoteItemResponse` objects.
        """
        return await self._request(
            "GET",
            "/v1/notes/pinned",
            model=NoteItemResponse,
        )

    async def search_notes(
        self,
        query: Optional[str] = None,
        view_option: Optional[str] = None,
        permission: Optional[str] = None,
        order_by: Optional[str] = None,
        direction: Optional[str] = None,
        page: Optional[int] = 1,
    ) -> NoteListResponse:
        """
        Search for notes.

        Args:
            query: Search query string.
            view_option: View option filter (e.g., 'created', 'shared').
            permission: Permission filter (e.g., 'read', 'write').
            order_by: Field to order by.
            direction: Sort direction ('asc', 'desc').
            page: Page number (default 1).

        Returns:
            `NoteListResponse`: List of notes matching the search criteria.
        """
        params = {}
        if query:
            params["query"] = query
        if view_option:
            params["view_option"] = view_option
        if permission:
            params["permission"] = permission
        if order_by:
            params["order_by"] = order_by
        if direction:
            params["direction"] = direction
        if page:
            params["page"] = page

        return await self._request(
            "GET",
            "/v1/notes/search",
            model=NoteListResponse,
            params=params,
        )

    async def create_note(self, form_data: NoteForm) -> Optional[NoteModel]:
        """
        Create a new note.

        Args:
            form_data: The data for the new note.

        Returns:
            The created note, or None if creation failed.
        """
        return await self._request(
            "POST",
            "/v1/notes/create",
            model=Optional[NoteModel],
            json=form_data.model_dump(),
        )

    async def get_note_by_id(self, id: str) -> Optional[NoteModel]:
        """
        Get a specific note by its ID.

        Args:
            id: The unique identifier of the note.

        Returns:
            The requested note, or None if not found or not accessible.
        """
        return await self._request(
            "GET",
            f"/v1/notes/{id}",
            model=Optional[NoteModel],
        )

    async def update_note_by_id(
        self, id: str, form_data: NoteForm
    ) -> Optional[NoteModel]:
        """
        Update an existing note.

        Args:
            id: The unique identifier of the note to update.
            form_data: The updated data for the note. Note that 'title' is required.

        Returns:
            The updated note, or None if update failed.
        """
        return await self._request(
            "POST",
            f"/v1/notes/{id}/update",
            model=Optional[NoteModel],
            json=form_data.model_dump(),
        )

    async def update_note_access_by_id(
        self, id: str, form_data: NoteAccessGrantsForm
    ) -> Optional[NoteModel]:
        """
        Update access grants for a note.

        This endpoint allows setting access grants for a note, controlling who can
        read or write to it. Only the note owner or users with write access can
        modify access grants. Non-admin users cannot set public access grants
        unless they have the 'sharing.public_notes' permission.

        Args:
            id: The unique identifier of the note.
            form_data: The access grants form containing the list of access grants.

        Returns:
            The updated note, or None if update failed.
        """
        return await self._request(
            "POST",
            f"/v1/notes/{id}/access/update",
            model=Optional[NoteModel],
            json=form_data.model_dump(),
        )

    async def pin_note_by_id(self, id: str) -> Optional[NoteModel]:
        """
        Toggle the pinned state of a note.

        If the note is currently pinned, it will be unpinned.
        If it is not pinned, it will be pinned.

        Args:
            id: The unique identifier of the note to pin/unpin.

        Returns:
            The updated note, or None if the operation failed.
        """
        return await self._request(
            "POST",
            f"/v1/notes/{id}/pin",
            model=Optional[NoteModel],
        )

    async def delete_note_by_id(self, id: str) -> bool:
        """
        Delete a note by its ID.

        Args:
            id: The unique identifier of the note to delete.

        Returns:
            True if deletion was successful, False otherwise.
        """
        return await self._request(
            "DELETE",
            f"/v1/notes/{id}/delete",
            model=bool,
        )
