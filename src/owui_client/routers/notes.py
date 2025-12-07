from typing import Optional, List
from owui_client.client_base import ResourceBase
from owui_client.models.notes import (
    NoteModel,
    NoteForm,
    NoteUserResponse,
    NoteTitleIdResponse,
)


class NotesClient(ResourceBase):
    """
    Client for the Notes endpoints.
    """

    async def get_notes(self) -> List[NoteUserResponse]:
        """
        Get all notes visible to the user.

        This endpoint returns a list of notes that the user has permission to view.
        If the user is an admin, they can see all notes.
        Otherwise, they can see their own notes and notes shared with them.

        Returns:
            A list of NoteUserResponse objects.
        """
        return await self._request(
            "GET",
            "/v1/notes/",
            model=NoteUserResponse,
        )

    async def get_note_list(
        self, page: Optional[int] = None
    ) -> List[NoteTitleIdResponse]:
        """
        Get a paginated list of notes visible to the user.

        This endpoint returns a simplified list of notes (only ID, title, timestamps).
        It supports pagination via the `page` parameter. The page size is fixed at 60.

        Args:
            page: The page number to retrieve (1-based index).

        Returns:
            A list of NoteTitleIdResponse objects.
        """
        params = {}
        if page is not None:
            params["page"] = page

        return await self._request(
            "GET",
            "/v1/notes/list",
            model=NoteTitleIdResponse,
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
