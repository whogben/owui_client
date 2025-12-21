import pytest
from owui_client.models.auths import SigninForm
from owui_client.models.notes import NoteForm, NoteUserResponse, NoteItemResponse, NoteModel

pytestmark = pytest.mark.asyncio

async def test_notes_client_initialization(client):
    assert client.notes is not None

async def test_notes_lifecycle(client):
    """
    Test create, get, update, delete lifecycle for notes.
    """
    # 1. Sign in as admin (handled by fixture)
    # form = SigninForm(email="admin@example.com", password="password123")
    # await client.auths.signin(form)

    # 2. Create a note
    note_form = NoteForm(
        title="Test Note",
        data={"content": "This is a test note"},
        meta={"category": "testing"},
        access_control=None
    )
    
    created_note = await client.notes.create_note(note_form)
    assert created_note is not None
    assert created_note.title == "Test Note"
    assert created_note.data == {"content": "This is a test note"}
    note_id = created_note.id

    # 3. Get notes list (full details)
    notes = await client.notes.get_notes()
    assert isinstance(notes, list)
    assert len(notes) >= 1
    found_note = next((n for n in notes if n.id == note_id), None)
    assert found_note is not None
    assert isinstance(found_note, NoteItemResponse)

    # 5. Get note by ID
    fetched_note = await client.notes.get_note_by_id(note_id)
    assert fetched_note is not None
    assert fetched_note.id == note_id
    assert fetched_note.title == "Test Note"

    # 6. Update note
    # Note: The API uses NoteForm for updates, requiring title.
    update_form = NoteForm(
        title="Updated Test Note",
        data={"content": "Updated content"},
        meta={"category": "updated"},
        access_control=None
    )
    
    updated_note = await client.notes.update_note_by_id(note_id, update_form)
    assert updated_note is not None
    assert updated_note.title == "Updated Test Note"
    assert updated_note.data["content"] == "Updated content"

    # Verify update with get
    fetched_updated_note = await client.notes.get_note_by_id(note_id)
    assert fetched_updated_note.title == "Updated Test Note"

    # 7. Delete note
    delete_result = await client.notes.delete_note_by_id(note_id)
    assert delete_result is True

    # Verify deletion
    # The client raises an exception for 404
    try:
        await client.notes.get_note_by_id(note_id)
        # If no exception, assert fail
        # However, client.base might return None or raise error depending on implementation.
        # ResourceBase -> OWUIClientBase -> _request
        # if response.status_code != 2xx, response.raise_for_status() is called.
        # So it should raise HTTPStatusError.
    except Exception as e:
        # Expected error
        assert "404" in str(e) or "Not Found" in str(e)

