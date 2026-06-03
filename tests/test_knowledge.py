"""Tests for Knowledge endpoints."""

import pytest
import time
import uuid
import zipfile
import io
from httpx import HTTPStatusError
from owui_client.client import OpenWebUI
from owui_client.models.knowledge import (
    KnowledgeForm,
    KnowledgeDirectoryCreateForm,
    KnowledgeDirectoryUpdateForm,
    KnowledgeFileMoveForm,
    SyncDiffForm,
    SyncCleanupForm,
    FileManifestEntry,
)

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio


async def test_knowledge_lifecycle(client):
    """
    Test creating, retrieving, updating, and deleting a knowledge base.
    """
    # Sign in as admin (handled by fixture)

    # Create knowledge base
    name = f"Test Knowledge {int(time.time())}"
    description = "A test knowledge base"

    form_data = KnowledgeForm(name=name, description=description)

    created_kb = await client.knowledge.create_new_knowledge(form_data)
    assert created_kb is not None
    assert created_kb.name == name
    assert created_kb.description == description
    kb_id = created_kb.id

    # 3. Get knowledge by ID
    fetched_kb = await client.knowledge.get_knowledge_by_id(kb_id)
    assert fetched_kb is not None
    assert fetched_kb.id == kb_id

    # 4. Get all knowledge bases
    response = await client.knowledge.get_knowledge()
    assert response.total > 0
    assert len(response.items) > 0
    ids = [kb.id for kb in response.items]
    assert kb_id in ids

    # 5. Update knowledge base
    new_name = "Updated Knowledge Base"
    form_data.name = new_name
    updated_kb = await client.knowledge.update_knowledge_by_id(kb_id, form_data)
    assert updated_kb is not None
    assert updated_kb.name == new_name

    # 6. Delete knowledge base
    deleted = await client.knowledge.delete_knowledge_by_id(kb_id)
    assert deleted is True

    # 7. Verify deletion
    with pytest.raises(HTTPStatusError):
        await client.knowledge.get_knowledge_by_id(kb_id)


async def test_knowledge_access_grants(client):
    """
    Test updating access grants on a knowledge base.
    """
    # Sign in as admin (handled by fixture)

    # Create knowledge base
    name = f"Access Test KB {int(time.time())}"
    kb = await client.knowledge.create_new_knowledge(
        KnowledgeForm(name=name, description="Test access grants")
    )
    assert kb is not None
    kb_id = kb.id

    # Update access grants with public read access
    access_grants = [
        {"principal_type": "user", "principal_id": "*", "permission": "read"}
    ]
    updated_kb = await client.knowledge.update_knowledge_access(kb_id, access_grants)
    assert updated_kb is not None
    assert updated_kb.id == kb_id

    # Verify the knowledge base still exists and is accessible
    fetched_kb = await client.knowledge.get_knowledge_by_id(kb_id)
    assert fetched_kb is not None

    # Clean up
    await client.knowledge.delete_knowledge_by_id(kb_id)


async def test_knowledge_search(client):
    """
    Test searching knowledge bases.
    """
    # Sign in as admin (handled by fixture)

    # Create a knowledge base with unique name
    unique_name = f"SearchTest {int(time.time())}"
    kb = await client.knowledge.create_new_knowledge(
        KnowledgeForm(name=unique_name, description="For search testing")
    )
    assert kb is not None
    kb_id = kb.id

    # Search for the knowledge base
    results = await client.knowledge.search_knowledge_bases(query="SearchTest")
    assert results is not None
    assert len(results.items) >= 1
    found_ids = [item.id for item in results.items]
    assert kb_id in found_ids

    # Clean up
    await client.knowledge.delete_knowledge_by_id(kb_id)


async def test_knowledge_reindex_metadata(client):
    """
    Test reindexing knowledge base metadata embeddings (admin only).
    """
    # Sign in as admin (handled by fixture)

    # Create a knowledge base first
    name = f"Reindex Test KB {int(time.time())}"
    kb = await client.knowledge.create_new_knowledge(
        KnowledgeForm(name=name, description="For reindex testing")
    )
    assert kb is not None
    kb_id = kb.id

    # Reindex metadata
    result = await client.knowledge.reindex_metadata()
    assert result is not None
    assert "total" in result
    assert "success" in result
    assert isinstance(result["total"], int)
    assert isinstance(result["success"], int)

    # Clean up
    await client.knowledge.delete_knowledge_by_id(kb_id)


async def test_knowledge_export(client):
    """
    Test exporting a knowledge base as a zip file (admin only).
    """
    # Sign in as admin (handled by fixture)

    # Create a knowledge base
    name = f"Export Test KB {int(time.time())}"
    kb = await client.knowledge.create_new_knowledge(
        KnowledgeForm(name=name, description="For export testing")
    )
    assert kb is not None
    kb_id = kb.id

    # Export the knowledge base
    zip_bytes = await client.knowledge.export(kb_id)
    assert zip_bytes is not None
    assert isinstance(zip_bytes, bytes)
    assert len(zip_bytes) > 0

    # Verify it's a valid zip file
    zip_buffer = io.BytesIO(zip_bytes)
    with zipfile.ZipFile(zip_buffer, "r") as zf:
        # Empty knowledge base should produce a valid but empty zip
        assert zf.testzip() is None

    # Clean up
    await client.knowledge.delete_knowledge_by_id(kb_id)


async def test_knowledge_directory_models():
    """Verify new knowledge directory models serialize correctly."""
    from owui_client.models.knowledge import (
        KnowledgeDirectoryModel,
        KnowledgeDirectoryCreateForm,
        KnowledgeDirectoryUpdateForm,
        KnowledgeFileMoveForm,
        KnowledgeFileListResponse,
        KnowledgeFileIdForm,
    )

    # KnowledgeDirectoryModel
    dir_model = KnowledgeDirectoryModel(
        id="dir-1",
        knowledge_id="kb-1",
        parent_id=None,
        name="docs",
        user_id="user-1",
        created_at=1000,
        updated_at=2000,
    )
    assert dir_model.name == "docs"
    assert dir_model.parent_id is None

    # KnowledgeDirectoryCreateForm
    create_form = KnowledgeDirectoryCreateForm(name="new-dir", parent_id="dir-1")
    assert create_form.name == "new-dir"
    assert create_form.parent_id == "dir-1"

    # KnowledgeDirectoryUpdateForm — sentinel default
    update_form = KnowledgeDirectoryUpdateForm()
    assert update_form.parent_id == "__unset__"
    update_form_move = KnowledgeDirectoryUpdateForm(parent_id=None)
    assert update_form_move.parent_id is None

    # KnowledgeFileMoveForm
    move_form = KnowledgeFileMoveForm(file_id="f-1", directory_id="dir-1")
    assert move_form.file_id == "f-1"

    # KnowledgeFileIdForm with directory_id
    file_form = KnowledgeFileIdForm(file_id="f-2", directory_id="dir-2")
    assert file_form.directory_id == "dir-2"

    # KnowledgeFileListResponse with directories and breadcrumbs
    list_resp = KnowledgeFileListResponse(
        items=[], directories=[dir_model], breadcrumbs=[], total=0
    )
    assert len(list_resp.directories) == 1
    assert list_resp.directories[0].name == "docs"


async def _create_test_kb(client: OpenWebUI) -> str:
    """Helper: create a knowledge base, return its id."""
    kb = await client.knowledge.create_new_knowledge(
        KnowledgeForm(
            name=f"DirTest {int(time.time() * 1000)}",
            description="Directory endpoint test KB",
        )
    )
    assert kb is not None
    return kb.id


@pytest.mark.asyncio
async def test_knowledge_directory_crud(client: OpenWebUI):
    """Test create / update / delete of a knowledge directory."""
    kb_id = await _create_test_kb(client)

    try:
        # 1. Create directory
        create_form = KnowledgeDirectoryCreateForm(name="docs")
        created_dir = await client.knowledge.create_knowledge_directory(
            kb_id, create_form
        )
        assert created_dir is not None
        assert created_dir.name == "docs"
        assert created_dir.knowledge_id == kb_id
        dir_id = created_dir.id

        # 2. Update directory (rename)
        update_form = KnowledgeDirectoryUpdateForm(name="renamed-docs")
        updated_dir = await client.knowledge.update_knowledge_directory(
            kb_id, dir_id, update_form
        )
        assert updated_dir is not None
        assert updated_dir.name == "renamed-docs"
        assert updated_dir.id == dir_id

        # 3. Delete directory (move files to parent)
        deleted = await client.knowledge.delete_knowledge_directory(
            kb_id, dir_id, move_files=True
        )
        assert deleted is True
    finally:
        await client.knowledge.delete_knowledge_by_id(kb_id)


@pytest.mark.asyncio
async def test_knowledge_move_file_form_validation(client: OpenWebUI):
    """Test that move_file_in_knowledge accepts a valid form (does not add a real file).

    We don't need to add a real processed file to a knowledge base for this test;
    we only verify that the endpoint accepts a well-formed move form (returning
    a meaningful backend response even if the file_id is unknown). The backend
    response shape is implementation-specific; we only assert the call succeeds
    in the sense that a 5xx server error is not raised.
    """
    kb_id = await _create_test_kb(client)
    try:
        # Form validation only — the backend may return 400 for an unknown file_id,
        # but that is a 4xx (client request), not a 5xx (server error).
        move_form = KnowledgeFileMoveForm(file_id="nonexistent-file-id")
        try:
            await client.knowledge.move_file_in_knowledge(kb_id, move_form)
        except Exception as exc:
            # 4xx is acceptable; we just want to ensure the request was well-formed
            assert "400" in str(exc) or "404" in str(exc) or "File not found" in str(exc), (
                f"Unexpected error: {exc}"
            )
    finally:
        await client.knowledge.delete_knowledge_by_id(kb_id)


@pytest.mark.asyncio
async def test_knowledge_get_pending_files(client: OpenWebUI):
    """Test that get_pending_knowledge_files returns a list (possibly empty)."""
    kb_id = await _create_test_kb(client)
    try:
        pending = await client.knowledge.get_pending_knowledge_files(kb_id)
        # Should return a list, may be empty if no files are mid-processing
        assert isinstance(pending, list)
    finally:
        await client.knowledge.delete_knowledge_by_id(kb_id)


@pytest.mark.asyncio
async def test_knowledge_sync_diff(client: OpenWebUI):
    """Test the sync diff endpoint with a minimal local manifest."""
    kb_id = await _create_test_kb(client)
    try:
        # Empty manifest should produce a diff with no added/modified files
        diff_form = SyncDiffForm(manifest=[])
        diff = await client.knowledge.sync_knowledge_diff(kb_id, diff_form)
        assert diff is not None
        # Verify the response has the expected top-level keys
        assert hasattr(diff, "added")
        assert hasattr(diff, "modified")
        assert hasattr(diff, "deleted")
        # A manifest entry should appear in 'added' if not yet in the KB
        new_entry = FileManifestEntry(
            filename=f"new_{uuid.uuid4().hex[:8]}.txt",
            path="",
            checksum="0" * 64,  # SHA-256 placeholder
            size=12,
        )
        diff_form2 = SyncDiffForm(manifest=[new_entry])
        diff2 = await client.knowledge.sync_knowledge_diff(kb_id, diff_form2)
        assert diff2 is not None
        assert any(
            entry.get("filename") == new_entry.filename
            for entry in diff2.added
        )
    finally:
        await client.knowledge.delete_knowledge_by_id(kb_id)


@pytest.mark.asyncio
async def test_knowledge_sync_cleanup(client: OpenWebUI):
    """Test the sync cleanup endpoint with an empty cleanup form."""
    kb_id = await _create_test_kb(client)
    try:
        # Empty cleanup should succeed (no files/dirs to remove)
        cleanup_form = SyncCleanupForm(file_ids=[], directory_ids=[])
        result = await client.knowledge.sync_knowledge_cleanup(kb_id, cleanup_form)
        assert result is True
    finally:
        await client.knowledge.delete_knowledge_by_id(kb_id)
