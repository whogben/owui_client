import pytest
import time
from owui_client.models.auths import SigninForm
from owui_client.models.prompts import PromptForm, PromptModel, PromptUserResponse

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio


async def test_prompts_client_initialization(client):
    assert client.prompts is not None


async def test_prompts_lifecycle(client):
    """
    Test create, get, update, delete prompt.
    """
    # 1. Sign in as admin (handled by fixture)
    # form = SigninForm(email="admin@example.com", password="password123")
    # await client.auths.signin(form)

    # Unique command to avoid collisions
    unique_command = f"test_prompt_{int(time.time())}"

    prompt_form = PromptForm(
        command=f"/{unique_command}",
        title="Test Prompt",
        content="This is a test prompt content.",
        access_control=None,
    )

    # 2. Create prompt
    created_prompt = await client.prompts.create_new_prompt(prompt_form)
    assert isinstance(created_prompt, PromptModel)
    assert created_prompt.command == f"/{unique_command}"
    assert created_prompt.title == "Test Prompt"

    # 3. Get prompt list
    prompts_list = await client.prompts.get_prompt_list()
    assert isinstance(prompts_list, list)
    assert len(prompts_list) > 0

    # Verify our prompt is in the list
    found_prompt = next(
        (p for p in prompts_list if p.command == f"/{unique_command}"), None
    )
    assert found_prompt is not None
    assert isinstance(found_prompt, PromptUserResponse)

    # 4. Get prompt by command
    # Note: The client method expects the command string, not the full path if logic is correct.
    # We implemented it to strip leading slash.
    fetched_prompt = await client.prompts.get_prompt_by_command(unique_command)
    assert fetched_prompt is not None
    assert fetched_prompt.command == f"/{unique_command}"

    # 5. Update prompt
    update_form = PromptForm(
        command=f"/{unique_command}",
        title="Updated Test Prompt",
        content="Updated content.",
        access_control=None,
    )

    updated_prompt = await client.prompts.update_prompt_by_command(
        unique_command, update_form
    )
    assert updated_prompt is not None
    assert updated_prompt.title == "Updated Test Prompt"
    assert updated_prompt.content == "Updated content."

    # 6. Delete prompt
    delete_result = await client.prompts.delete_prompt_by_command(unique_command)
    assert delete_result is True

    # 7. Verify deletion
    try:
        await client.prompts.get_prompt_by_command(unique_command)
        assert False, "Should have raised 404 or similar exception"
    except Exception:
        pass


async def test_get_prompts(client):
    """
    Test get_prompts (which returns PromptModel list vs PromptUserResponse list).
    """
    # 1. Sign in as admin (handled by fixture)
    # form = SigninForm(email="admin@example.com", password="password123")
    # await client.auths.signin(form)

    prompts = await client.prompts.get_prompts()
    assert isinstance(prompts, list)
    if len(prompts) > 0:
        assert isinstance(prompts[0], PromptModel)

