import pytest
import time
from owui_client.models.tools import (
    ToolForm,
    ToolModel,
    ToolUserResponse,
    ToolMeta,
    ToolAccessGrantsForm,
)

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio


async def test_tools_client_initialization(client):
    assert client.tools is not None


async def test_tools_lifecycle(client):
    """
    Test create, get, update, delete tool.
    """
    # Unique ID to avoid collisions
    unique_id = f"test_tool_{int(time.time())}"

    tool_form = ToolForm(
        id=unique_id,
        name="Test Tool",
        content="""
class Tools:
    def __init__(self):
        pass

    def perform_task(self):
        return "Hello World"
""",
        meta=ToolMeta(description="A test tool"),
        access_control=None,
    )

    # 1. Create tool
    created_tool = await client.tools.create_new_tool(tool_form)
    assert created_tool is not None
    assert created_tool.id == unique_id
    assert created_tool.name == "Test Tool"

    # 2. Get tool list
    tools_list = await client.tools.get_tool_list()
    assert isinstance(tools_list, list)

    # Verify our tool is in the list
    found_tool = next((t for t in tools_list if t.id == unique_id), None)
    assert found_tool is not None
    assert found_tool.id == unique_id

    # 3. Get tool by ID
    fetched_tool = await client.tools.get_tool_by_id(unique_id)
    assert fetched_tool is not None
    assert fetched_tool.id == unique_id

    # 4. Update tool
    update_form = ToolForm(
        id=unique_id,
        name="Updated Test Tool",
        content="""
class Tools:
    def __init__(self):
        pass

    def perform_task(self):
        return "Hello Updated World"
""",
        meta=ToolMeta(description="An updated test tool"),
        access_control=None,
    )

    updated_tool = await client.tools.update_tool_by_id(unique_id, update_form)
    assert updated_tool is not None
    assert updated_tool.name == "Updated Test Tool"

    # 5. Delete tool
    delete_result = await client.tools.delete_tool_by_id(unique_id)
    assert delete_result is True

    # 6. Verify deletion
    try:
        await client.tools.get_tool_by_id(unique_id)
        assert False, "Should have raised exception"
    except Exception:
        pass


async def test_update_tool_access(client):
    """Test updating tool access grants."""
    unique_id = f"test_tool_access_{int(time.time())}"

    # Create a tool
    tool_form = ToolForm(
        id=unique_id,
        name="Test Tool for Access",
        content="""
class Tools:
    def __init__(self):
        pass

    def perform_task(self):
        return "Hello World"
""",
        meta=ToolMeta(description="A test tool for access testing"),
        access_control=None,
    )

    created_tool = await client.tools.create_new_tool(tool_form)
    assert created_tool is not None
    assert created_tool.id == unique_id

    # Update access grants
    access_form = ToolAccessGrantsForm(
        access_grants=[
            {
                "principal_type": "user",
                "principal_id": "*",
                "permission": "read",
            }
        ]
    )

    updated_tool = await client.tools.update_tool_access_by_id(unique_id, access_form)
    assert updated_tool is not None
    assert updated_tool.id == unique_id
    # Verify access_grants field is present
    assert hasattr(updated_tool, "access_grants")

    # Clean up
    await client.tools.delete_tool_by_id(unique_id)
