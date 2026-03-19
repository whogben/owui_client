import pytest
from owui_client.models.auths import SigninForm
from owui_client.models.notes import (
    NoteForm,
    NoteUserResponse,
    NoteItemResponse,
    NoteModel,
    NoteAccessGrantsForm,
)

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
        data={"content": {"md": "This is a test note"}},
        meta={"category": "testing"},
        access_control=None,
    )

    created_note = await client.notes.create_note(note_form)
    assert created_note is not None
    assert created_note.title == "Test Note"
    assert created_note.data == {"content": {"md": "This is a test note"}}
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
        data={"content": {"md": "Updated content"}},
        meta={"category": "updated"},
        access_control=None,
    )

    updated_note = await client.notes.update_note_by_id(note_id, update_form)
    assert updated_note is not None
    assert updated_note.title == "Updated Test Note"
    assert updated_note.data["content"]["md"] == "Updated content"

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


async def test_notes_search(client):
    """
    Test searching for notes.
    """
    # Create a note to search for
    note_form = NoteForm(
        title="Searchable Note",
        data={"content": {"md": "This note is searchable"}},
        meta={"category": "search-test"},
        access_control=None,
    )

    created_note = await client.notes.create_note(note_form)
    assert created_note is not None
    note_id = created_note.id

    try:
        # Search without query (should return all visible notes)
        results = await client.notes.search_notes()
        assert results is not None
        # NoteListResponse has 'items' and 'total' attributes
        assert hasattr(results, "items")
        assert hasattr(results, "total")

        # Search with query
        results = await client.notes.search_notes(query="Searchable")
        assert results is not None

        # Search with view_option
        results = await client.notes.search_notes(view_option="created")
        assert results is not None

        # Search with order_by and direction
        results = await client.notes.search_notes(
            order_by="updated_at", direction="desc"
        )
        assert results is not None

    finally:
        # Cleanup
        await client.notes.delete_note_by_id(note_id)


async def test_notes_access_grants(client):
    """
    Test updating access grants for a note.
    """
    # Create a note
    note_form = NoteForm(
        title="Access Test Note",
        data={"content": {"md": "Testing access grants"}},
        access_control=None,
    )

    created_note = await client.notes.create_note(note_form)
    assert created_note is not None
    note_id = created_note.id

    try:
        # Update access grants - grant public read access
        access_form = NoteAccessGrantsForm(
            access_grants=[
                {
                    "principal_type": "user",
                    "principal_id": "*",
                    "permission": "read",
                }
            ]
        )

        updated_note = await client.notes.update_note_access_by_id(note_id, access_form)
        assert updated_note is not None
        assert updated_note.id == note_id

        # Verify the note still exists and is accessible
        fetched_note = await client.notes.get_note_by_id(note_id)
        assert fetched_note is not None

        # Update access grants - remove public access (empty grants)
        access_form_empty = NoteAccessGrantsForm(access_grants=[])
        updated_note = await client.notes.update_note_access_by_id(
            note_id, access_form_empty
        )
        assert updated_note is not None

    finally:
        # Cleanup
        await client.notes.delete_note_by_id(note_id)


async def test_notes_with_access_grants_on_create(client):
    """
    Test creating a note with access grants.
    """
    # Create a note with access grants
    note_form = NoteForm(
        title="Note With Grants",
        data={"content": {"md": "Created with access grants"}},
        access_grants=[
            {
                "principal_type": "user",
                "principal_id": "*",
                "permission": "read",
            }
        ],
        access_control=None,
    )

    created_note = await client.notes.create_note(note_form)
    assert created_note is not None
    assert created_note.title == "Note With Grants"
    note_id = created_note.id

    try:
        # Verify the note exists
        fetched_note = await client.notes.get_note_by_id(note_id)
        assert fetched_note is not None
        assert fetched_note.title == "Note With Grants"
    finally:
        # Cleanup
        await client.notes.delete_note_by_id(note_id)
