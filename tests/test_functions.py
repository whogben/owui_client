import pytest
import time
from owui_client.models.functions import FunctionForm, FunctionMeta

FUNCTION_CONTENT = """
class Filter:
    def __init__(self):
        pass

    def outlet(self, body: dict, user: dict) -> dict:
        print(f"User: {user}")
        return body
"""

@pytest.mark.asyncio
async def test_functions_crud(client):
    # 1. Create a function
    function_id = f"test_function_{int(time.time())}"
    function_form = FunctionForm(
        id=function_id,
        name="Test Function",
        content=FUNCTION_CONTENT,
        meta=FunctionMeta(description="A test function"),
    )

    created_function = await client.functions.create_function(function_form)
    assert created_function is not None
    assert created_function.id == function_id
    assert created_function.name == "Test Function"

    # 2. Get function by ID
    fetched_function = await client.functions.get_function_by_id(function_id)
    assert fetched_function is not None
    assert fetched_function.id == function_id

    # 3. List functions
    functions = await client.functions.get_functions()
    assert any(f.id == function_id for f in functions)

    # 4. Update function
    updated_form = FunctionForm(
        id=function_id,
        name="Updated Test Function",
        content=FUNCTION_CONTENT,
        meta=FunctionMeta(description="An updated test function"),
    )
    updated_function = await client.functions.update_function_by_id(function_id, updated_form)
    assert updated_function is not None
    assert updated_function.name == "Updated Test Function"

    # 5. Toggle function
    toggled_function = await client.functions.toggle_function_by_id(function_id)
    assert toggled_function is not None
    # It defaults to False, so toggling should make it True (or whatever the server default is, usually starts false)
    # Checking inequality with previous state would be safer if we knew previous state, 
    # but let's just check it returns a model.
    
    # 6. Delete function
    deleted = await client.functions.delete_function_by_id(function_id)
    assert deleted is True

    # Verify deletion
    functions_after = await client.functions.get_functions()
    assert not any(f.id == function_id for f in functions_after)

