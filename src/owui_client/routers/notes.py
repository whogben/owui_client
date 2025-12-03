from typing import Optional, List
from owui_client.client_base import ResourceBase
from owui_client.models.notes import (
    NoteModel,
    NoteForm,
    NoteUserResponse,
    NoteTitleIdResponse,
)


class NotesClient(ResourceBase):
    async def get_notes(self) -> List[NoteUserResponse]:
        """
        Get a list of notes.

        :return: List of notes with user info
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
        Get a list of notes with pagination.

        :param page: Page number (optional)
        :return: List of note titles and IDs
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

        :param form_data: The note form data
        :return: The created note model
        """
        return await self._request(
            "POST",
            "/v1/notes/create",
            model=Optional[NoteModel],
            json=form_data.model_dump(),
        )

    async def get_note_by_id(self, id: str) -> Optional[NoteModel]:
        """
        Get a note by ID.

        :param id: The ID of the note
        :return: The note model
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
        Update a note by ID.

        :param id: The ID of the note
        :param form_data: The note form data
        :return: The updated note model
        """
        return await self._request(
            "POST",
            f"/v1/notes/{id}/update",
            model=Optional[NoteModel],
            json=form_data.model_dump(),
        )

    async def delete_note_by_id(self, id: str) -> bool:
        """
        Delete a note by ID.

        :param id: The ID of the note
        :return: True if successful
        """
        return await self._request(
            "DELETE",
            f"/v1/notes/{id}/delete",
            model=bool,
        )
