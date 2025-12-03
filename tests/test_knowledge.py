import pytest
import uuid
from httpx import HTTPStatusError
from owui_client.models.knowledge import KnowledgeForm

pytestmark = pytest.mark.asyncio


async def test_knowledge_lifecycle(client):
    """
    Test create, get, update, delete lifecycle for knowledge bases.
    """

    # 1. Create a knowledge base
    kb_name = f"Test Knowledge Base {uuid.uuid4()}"
    kb_form = KnowledgeForm(
        name=kb_name,
        description="This is a test knowledge base",
        access_control=None
    )

    created_kb = await client.knowledge.create_new_knowledge(kb_form)
    assert created_kb is not None
    assert created_kb.name == kb_name
    assert created_kb.description == "This is a test knowledge base"
    kb_id = created_kb.id

    # 2. Get knowledge bases list (read access)
    kbs = await client.knowledge.get_knowledge()
    assert isinstance(kbs, list)
    found_kb = next((kb for kb in kbs if kb.id == kb_id), None)
    assert found_kb is not None
    assert found_kb.name == kb_name

    # 3. Get knowledge bases list (write access)
    kbs_list = await client.knowledge.get_knowledge_list()
    assert isinstance(kbs_list, list)
    found_kb_list = next((kb for kb in kbs_list if kb.id == kb_id), None)
    assert found_kb_list is not None

    # 4. Get knowledge base by ID
    fetched_kb = await client.knowledge.get_knowledge_by_id(kb_id)
    assert fetched_kb is not None
    assert fetched_kb.id == kb_id
    assert fetched_kb.name == kb_name

    # 5. Update knowledge base
    update_form = KnowledgeForm(
        name=f"Updated {kb_name}",
        description="Updated description",
        access_control=None
    )

    updated_kb = await client.knowledge.update_knowledge_by_id(kb_id, update_form)
    assert updated_kb is not None
    assert updated_kb.name == f"Updated {kb_name}"
    assert updated_kb.description == "Updated description"

    # 6. Create a file to add
    filename = f"test_file_kb_{uuid.uuid4()}.txt"
    content = b"Content for knowledge base test"
    
    uploaded_file = await client.files.upload_file(
        file=(filename, content, "text/plain"),
        process=False  # Skip processing for speed
    )
    file_id = uploaded_file.id

    # 6.5 Update file content to ensure it's "processed" (has content in data)
    # This is required for add_file_to_knowledge to work
    try:
        await client.files.update_file_data_content_by_id(file_id, "Content for knowledge base test")
    except Exception as e:
        # If embedding fails, we might still be okay if the content was saved.
        # But likely we need a working embedding setup or mock.
        # For now, let's proceed and see if add_file_to_knowledge works.
        print(f"Warning: update_file_data_content_by_id failed: {e}")

    # 7. Add file to knowledge base
    kb_with_file = await client.knowledge.add_file_to_knowledge(kb_id, file_id)
    assert kb_with_file is not None
    assert any(f.id == file_id for f in kb_with_file.files)

    # 8. Remove file from knowledge base
    # We keep the file (delete_file=False) to clean it up manually later if needed, 
    # or let it be deleted by test cleanup if we wanted to test delete_file=True separately.
    # Here we test removing from KB but keeping the file.
    kb_no_file = await client.knowledge.remove_file_from_knowledge(
        kb_id, file_id, delete_file=False
    )
    assert kb_no_file is not None
    assert not any(f.id == file_id for f in kb_no_file.files)

    # 9. Delete knowledge base
    delete_result = await client.knowledge.delete_knowledge_by_id(kb_id)
    assert delete_result is True

    # Verify deletion
    try:
        await client.knowledge.get_knowledge_by_id(kb_id)
        assert False, "Should have raised 404"
    except HTTPStatusError as e:
        assert e.response.status_code == 404 or e.response.status_code == 401 # Depends on implementation details

    # Cleanup file
    await client.files.delete_file_by_id(file_id)

