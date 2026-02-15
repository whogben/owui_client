import pytest
import time
from owui_client.models.prompts import PromptForm
from owui_client.models.auths import SigninForm

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio


async def test_prompt_lifecycle(client):
    """
    Test creating, retrieving, updating, and deleting a prompt.
    """
    # 1. Sign in as admin (Already authenticated by fixture)
    # form = SigninForm(email="admin@example.com", password="password123")
    # await client.auths.signin(form)

    # 2. Create prompt
    command = f"/test_cmd_{int(time.time())}"
    name = "Test Prompt"
    content = "This is a test prompt content"

    form_data = PromptForm(command=command, name=name, content=content)

    created_prompt = await client.prompts.create_new_prompt(form_data)
    assert created_prompt is not None
    assert created_prompt.command == command
    assert created_prompt.name == name

    # 3. Get prompt by command
    # Remove slash for client call if needed, but client handles stripping?
    # Client method: clean_command = command.lstrip("/")
    # If we pass "/test...", it becomes "test...".
    # Backend endpoint: /command/{command} -> receives "test..."
    # Backend query: f"/{command}" -> "/test..."
    # So it matches.
    fetched_prompt = await client.prompts.get_prompt_by_command(command)
    assert fetched_prompt is not None
    assert fetched_prompt.command == command

    # 4. Get all prompts
    prompts = await client.prompts.get_prompts()
    assert len(prompts) > 0
    commands = [p.command for p in prompts]
    assert command in commands

    # 5. Update prompt
    new_name = "Updated Test Prompt"
    form_data.name = new_name
    updated_prompt = await client.prompts.update_prompt_by_command(command, form_data)
    assert updated_prompt is not None
    assert updated_prompt.name == new_name

    # 6. Delete prompt
    deleted = await client.prompts.delete_prompt_by_command(command)
    assert deleted is True

    # 7. Verify deletion (client returns None when prompt is not found)
    post_delete = await client.prompts.get_prompt_by_command(command)
    assert post_delete is None
