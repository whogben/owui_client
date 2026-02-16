"""Tests for Knowledge endpoints."""

import pytest
import time
import zipfile
import io
from httpx import HTTPStatusError
from owui_client.models.knowledge import KnowledgeForm

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
