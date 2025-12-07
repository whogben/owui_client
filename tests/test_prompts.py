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
    title = "Test Prompt"
    content = "This is a test prompt content"
    
    form_data = PromptForm(
        command=command,
        title=title,
        content=content
    )

    created_prompt = await client.prompts.create_new_prompt(form_data)
    assert created_prompt is not None
    assert created_prompt.command == command
    assert created_prompt.title == title

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
    new_title = "Updated Test Prompt"
    form_data.title = new_title
    updated_prompt = await client.prompts.update_prompt_by_command(command, form_data)
    assert updated_prompt is not None
    assert updated_prompt.title == new_title

    # 6. Delete prompt
    deleted = await client.prompts.delete_prompt_by_command(command)
    assert deleted is True

    # 7. Verify deletion
    from httpx import HTTPStatusError
    with pytest.raises(HTTPStatusError):
        await client.prompts.get_prompt_by_command(command)
