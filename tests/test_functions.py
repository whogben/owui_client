import pytest
import time
from owui_client.models.functions import FunctionForm, FunctionMeta
from owui_client.models.auths import SigninForm

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio


async def test_function_lifecycle(client):
    """
    Test creating, retrieving, updating, and deleting a function.
    """
    # 1. Sign in as admin (Already authenticated by fixture)
    # form = SigninForm(email="admin@example.com", password="password123")
    # await client.auths.signin(form)

    # 2. Create a function
    function_id = f"test_func_{int(time.time())}"
    function_content = """
class Pipe:
    def pipe(self, body):
        print("Hello World")
        return body
"""
    form_data = FunctionForm(
        id=function_id,
        name="Test Function",
        content=function_content,
        meta=FunctionMeta(description="A test function", manifest={})
    )

    created_function = await client.functions.create_function(form_data)
    assert created_function is not None
    assert created_function.id == function_id
    assert created_function.name == "Test Function"

    # 3. Get function by ID
    fetched_function = await client.functions.get_function_by_id(function_id)
    assert fetched_function is not None
    assert fetched_function.id == function_id
    assert fetched_function.content == function_content

    # 4. Get all functions
    functions = await client.functions.get_functions()
    assert len(functions) > 0
    ids = [f.id for f in functions]
    assert function_id in ids

    # 5. Update function
    new_name = "Updated Test Function"
    form_data.name = new_name
    updated_function = await client.functions.update_function_by_id(function_id, form_data)
    assert updated_function is not None
    assert updated_function.name == new_name

    # 6. Toggle active
    toggled_function = await client.functions.toggle_function_by_id(function_id)
    assert toggled_function is not None
    # Initial state is False, so it should become True
    assert toggled_function.is_active is True

    # 7. Toggle global
    toggled_global = await client.functions.toggle_global_by_id(function_id)
    assert toggled_global is not None
    # Initial state is False, so it should become True
    assert toggled_global.is_global is True

    # 8. Export functions
    exported = await client.functions.export_functions()
    assert len(exported) > 0
    exported_ids = [f.id for f in exported]
    assert function_id in exported_ids

    # 9. Delete function
    deleted = await client.functions.delete_function_by_id(function_id)
    assert deleted is True

    # 10. Verify deletion
    from httpx import HTTPStatusError
    try:
        await client.functions.get_function_by_id(function_id)
        assert False, "Function should have been deleted"
    except HTTPStatusError as e:
        # Backend returns 401 for not found
        assert e.response.status_code == 401
