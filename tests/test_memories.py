import pytest
from owui_client.models.memories import (
    AddMemoryForm,
    MemoryUpdateModel,
    QueryMemoryForm,
    ListMemoryPathsForm,
    ReadMemoryPathForm,
)
from owui_client.client import OpenWebUI


@pytest.mark.asyncio
async def test_memories_crud(client: OpenWebUI):
    # 1. Clean up any existing memories for the user (optional, but good for isolation)
    await client.memories.delete_memory_by_user_id()

    # 2. Add a new memory
    content = "Remember to buy milk and cookies"
    add_form = AddMemoryForm(content=content)
    memory = await client.memories.add_memory(add_form)

    assert memory is not None
    assert memory.content == content
    assert memory.user_id is not None
    assert memory.id is not None

    memory_id = memory.id

    # 3. Get all memories and verify
    memories = await client.memories.get_memories()
    assert len(memories) > 0
    found = False
    for m in memories:
        if m.id == memory_id:
            assert m.content == content
            found = True
            break
    assert found

    # 4. Update the memory
    new_content = "Remember to buy milk, cookies, and eggs"
    update_form = MemoryUpdateModel(content=new_content)
    updated_memory = await client.memories.update_memory_by_id(memory_id, update_form)

    assert updated_memory is not None
    assert updated_memory.content == new_content
    assert updated_memory.id == memory_id

    # 5. Verify update via list
    memories = await client.memories.get_memories()
    found = False
    for m in memories:
        if m.id == memory_id:
            assert m.content == new_content
            found = True
            break
    assert found

    # 6. Delete the memory
    deleted = await client.memories.delete_memory_by_id(memory_id)
    assert deleted is True

    # 7. Verify deletion
    memories = await client.memories.get_memories()
    found = False
    for m in memories:
        if m.id == memory_id:
            found = True
            break
    assert not found

    # 8. Test delete all by user (Clean up)
    # Add a couple of memories
    await client.memories.add_memory(AddMemoryForm(content="Memory 1"))
    await client.memories.add_memory(AddMemoryForm(content="Memory 2"))

    memories = await client.memories.get_memories()
    assert len(memories) >= 2

    deleted_all = await client.memories.delete_memory_by_user_id()
    assert deleted_all is True

    memories = await client.memories.get_memories()
    assert len(memories) == 0


@pytest.mark.asyncio
async def test_memories_query(client: OpenWebUI):
    # This test depends on the embedding function working in the backend.
    # If the backend is running in a container without proper embedding setup, this might be flaky or fail.
    # We'll try it.

    await client.memories.delete_memory_by_user_id()

    content = "The secret code is 12345"
    await client.memories.add_memory(AddMemoryForm(content=content))

    # Query
    query_form = QueryMemoryForm(content="secret code", k=1)
    try:
        results = await client.memories.query_memory(query_form)
        # The structure of results depends on vector db response.
        # Usually it's a dict or list.
        # Just check if we get something back.
        assert results is not None
        # If it returns the memory items directly or inside a structure:
        # Assuming standard Chroma/VectorDB response which might be specific.
        # But at least we shouldn't get an error.
    except Exception as e:
        # If embedding function is not working, it might fail.
        # We can warn but maybe not fail the test if it's an environment issue?
        # But strictly, we should expect it to work if the environment is correct.
        pytest.fail(f"Query failed: {e}")


async def _add_pathed_memory(client: OpenWebUI, content: str, path: str, memory_type: str = "context"):
    """Helper: add a memory with a path/type and return it."""
    return await client.memories.add_memory(
        AddMemoryForm(content=content, type=memory_type, path=path)
    )


@pytest.mark.asyncio
async def test_memories_list_paths(client: OpenWebUI):
    # POST /memories/paths groups memories by (path, type) into a tree.
    await client.memories.delete_memory_by_user_id()

    await _add_pathed_memory(client, "work root note", "work")
    await _add_pathed_memory(client, "project a note one", "work/project-a")
    await _add_pathed_memory(client, "project a note two", "work/project-a")
    await _add_pathed_memory(client, "personal note", "personal")

    result = await client.memories.list_memory_paths(ListMemoryPathsForm())

    assert isinstance(result, dict)
    assert "paths" in result and "count" in result
    assert isinstance(result["paths"], list)
    assert isinstance(result["count"], int)
    assert result["count"] >= 3  # work, work/project-a, personal

    # Each group carries the documented keys.
    for group in result["paths"]:
        assert set(group.keys()) >= {"path", "type", "count", "updated_at", "children"}
        assert isinstance(group["children"], list)

    # The "work" group's immediate children should include "work/project-a".
    work_group = next((g for g in result["paths"] if g["path"] == "work"), None)
    assert work_group is not None, "expected a group for path 'work'"
    assert "work/project-a" in work_group["children"]

    # The "work/project-a" group should aggregate the two notes (count >= 2).
    pa_group = next((g for g in result["paths"] if g["path"] == "work/project-a"), None)
    assert pa_group is not None, "expected a group for path 'work/project-a'"
    assert pa_group["count"] >= 2

    await client.memories.delete_memory_by_user_id()


@pytest.mark.asyncio
async def test_memories_read_path(client: OpenWebUI):
    # POST /memories/path returns memory rows at a path plus ancestors/descendants.
    await client.memories.delete_memory_by_user_id()

    await _add_pathed_memory(client, "work root note", "work")
    await _add_pathed_memory(client, "project a note one", "work/project-a")
    await _add_pathed_memory(client, "project a note two", "work/project-a")

    result = await client.memories.read_memory_path(
        ReadMemoryPathForm(path="work/project-a")
    )

    assert isinstance(result, dict)
    assert result["path"] == "work/project-a"
    assert isinstance(result["parents"], list)
    assert isinstance(result["children"], list)
    assert isinstance(result["memories"], list)

    # The ancestor path "work" should be reported and its memory included.
    assert "work" in result["parents"]
    memory_paths = {m["path"] for m in result["memories"]}
    assert "work/project-a" in memory_paths
    assert "work" in memory_paths  # parent memory selected too
    # Each returned memory is a full MemoryModel dict, including new fields.
    for memory in result["memories"]:
        assert {"id", "content", "type", "path", "meta"} <= set(memory.keys())

    await client.memories.delete_memory_by_user_id()


@pytest.mark.asyncio
async def test_memories_embeddings(client: OpenWebUI):
    # Test the /v1/retrieval/ef endpoint (embedding function test)
    # Note: This endpoint is in the retrieval router, not memories router
    try:
        result = await client.retrieval.get_embeddings()
        assert isinstance(result, dict)
        assert "result" in result
        # result["result"] should be the embedding list or similar
        assert isinstance(result["result"], list)
        assert len(result["result"]) > 0
    except Exception as e:
        pytest.fail(f"Get embeddings failed: {e}")
