import pytest
import time
from owui_client.models.knowledge import KnowledgeForm
from owui_client.models.auths import SigninForm

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio


async def test_knowledge_lifecycle(client):
    """
    Test creating, retrieving, updating, and deleting a knowledge base.
    """
    # 1. Sign in as admin
    form = SigninForm(email="admin@example.com", password="password123")
    await client.auths.signin(form)

    # 2. Create knowledge base
    name = f"Test Knowledge {int(time.time())}"
    description = "A test knowledge base"
    
    form_data = KnowledgeForm(
        name=name,
        description=description
    )

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
    # get_knowledge_by_id raises 404 or returns None depending on implementation?
    # Client raises HTTPStatusError on 404 usually.
    from httpx import HTTPStatusError
    with pytest.raises(HTTPStatusError):
        await client.knowledge.get_knowledge_by_id(kb_id)
