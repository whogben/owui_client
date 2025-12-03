import pytest
from owui_client.models.tasks import TaskConfigForm
from owui_client.models.openai import OpenAIConfigForm

@pytest.mark.asyncio
async def test_tasks_config(client):
    # Get initial config
    config = await client.tasks.get_config()
    assert isinstance(config, dict)
    assert "TASK_MODEL" in config

    # Update config
    # We'll toggle ENABLE_TITLE_GENERATION to ensure we see a change
    initial_value = config["ENABLE_TITLE_GENERATION"]
    new_value = not initial_value

    form = TaskConfigForm(
        TASK_MODEL=config.get("TASK_MODEL"),
        TASK_MODEL_EXTERNAL=config.get("TASK_MODEL_EXTERNAL"),
        ENABLE_TITLE_GENERATION=new_value,
        TITLE_GENERATION_PROMPT_TEMPLATE=config.get("TITLE_GENERATION_PROMPT_TEMPLATE", ""),
        IMAGE_PROMPT_GENERATION_PROMPT_TEMPLATE=config.get("IMAGE_PROMPT_GENERATION_PROMPT_TEMPLATE", ""),
        ENABLE_AUTOCOMPLETE_GENERATION=config.get("ENABLE_AUTOCOMPLETE_GENERATION", False),
        AUTOCOMPLETE_GENERATION_INPUT_MAX_LENGTH=config.get("AUTOCOMPLETE_GENERATION_INPUT_MAX_LENGTH", 50),
        TAGS_GENERATION_PROMPT_TEMPLATE=config.get("TAGS_GENERATION_PROMPT_TEMPLATE", ""),
        FOLLOW_UP_GENERATION_PROMPT_TEMPLATE=config.get("FOLLOW_UP_GENERATION_PROMPT_TEMPLATE", ""),
        ENABLE_FOLLOW_UP_GENERATION=config.get("ENABLE_FOLLOW_UP_GENERATION", False),
        ENABLE_TAGS_GENERATION=config.get("ENABLE_TAGS_GENERATION", False),
        ENABLE_SEARCH_QUERY_GENERATION=config.get("ENABLE_SEARCH_QUERY_GENERATION", False),
        ENABLE_RETRIEVAL_QUERY_GENERATION=config.get("ENABLE_RETRIEVAL_QUERY_GENERATION", False),
        QUERY_GENERATION_PROMPT_TEMPLATE=config.get("QUERY_GENERATION_PROMPT_TEMPLATE", ""),
        TOOLS_FUNCTION_CALLING_PROMPT_TEMPLATE=config.get("TOOLS_FUNCTION_CALLING_PROMPT_TEMPLATE", ""),
        VOICE_MODE_PROMPT_TEMPLATE=config.get("VOICE_MODE_PROMPT_TEMPLATE", ""),
    )

    updated_config = await client.tasks.update_config(form)
    assert updated_config["ENABLE_TITLE_GENERATION"] == new_value

    # Verify with get
    final_config = await client.tasks.get_config()
    assert final_config["ENABLE_TITLE_GENERATION"] == new_value

    # Revert
    form.ENABLE_TITLE_GENERATION = initial_value
    await client.tasks.update_config(form)


@pytest.mark.asyncio
async def test_title_generation(client, mock_openai_server):
    # 1. Configure OWUI to use the mock OpenAI server
    openai_config = OpenAIConfigForm(
        ENABLE_OPENAI_API=True,
        OPENAI_API_BASE_URLS=[mock_openai_server],
        OPENAI_API_KEYS=["sk-mock-key"],
        OPENAI_API_CONFIGS={"0": {"enable": True}}
    )
    await client.openai.update_config(openai_config)

    # 2. Ensure we have a model available
    # We need to hit the main /api/models endpoint to force OWUI to refresh models from the providers
    # We loop until the model is found to handle async refreshing
    import asyncio
    for _ in range(10):
        models_response = await client.root.get_models()
        model_ids = [m["id"] for m in models_response.get("data", [])]
        if "gpt-3.5-turbo" in model_ids:
            break
        await asyncio.sleep(0.5)
    else:
        pytest.fail("Mock model 'gpt-3.5-turbo' did not appear in /models list after retries")
    
    # 3. Enable title generation
    config = await client.tasks.get_config()
    form = TaskConfigForm(
        TASK_MODEL="gpt-3.5-turbo", # Use the mock model
        TASK_MODEL_EXTERNAL=config.get("TASK_MODEL_EXTERNAL"),
        ENABLE_TITLE_GENERATION=True,
        TITLE_GENERATION_PROMPT_TEMPLATE=config.get("TITLE_GENERATION_PROMPT_TEMPLATE", ""),
        IMAGE_PROMPT_GENERATION_PROMPT_TEMPLATE=config.get("IMAGE_PROMPT_GENERATION_PROMPT_TEMPLATE", ""),
        ENABLE_AUTOCOMPLETE_GENERATION=config.get("ENABLE_AUTOCOMPLETE_GENERATION", False),
        AUTOCOMPLETE_GENERATION_INPUT_MAX_LENGTH=config.get("AUTOCOMPLETE_GENERATION_INPUT_MAX_LENGTH", 50),
        TAGS_GENERATION_PROMPT_TEMPLATE=config.get("TAGS_GENERATION_PROMPT_TEMPLATE", ""),
        FOLLOW_UP_GENERATION_PROMPT_TEMPLATE=config.get("FOLLOW_UP_GENERATION_PROMPT_TEMPLATE", ""),
        ENABLE_FOLLOW_UP_GENERATION=config.get("ENABLE_FOLLOW_UP_GENERATION", False),
        ENABLE_TAGS_GENERATION=config.get("ENABLE_TAGS_GENERATION", False),
        ENABLE_SEARCH_QUERY_GENERATION=config.get("ENABLE_SEARCH_QUERY_GENERATION", False),
        ENABLE_RETRIEVAL_QUERY_GENERATION=config.get("ENABLE_RETRIEVAL_QUERY_GENERATION", False),
        QUERY_GENERATION_PROMPT_TEMPLATE=config.get("QUERY_GENERATION_PROMPT_TEMPLATE", ""),
        TOOLS_FUNCTION_CALLING_PROMPT_TEMPLATE=config.get("TOOLS_FUNCTION_CALLING_PROMPT_TEMPLATE", ""),
        VOICE_MODE_PROMPT_TEMPLATE=config.get("VOICE_MODE_PROMPT_TEMPLATE", ""),
    )
    await client.tasks.update_config(form)

    # 4. Call generate_title
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Hello world"}
        ]
    }
    response = await client.tasks.generate_title(payload)
    
    # The mock server returns a chat completion response
    assert "choices" in response
    assert len(response["choices"]) > 0
    assert "message" in response["choices"][0]

@pytest.mark.asyncio
async def test_list_and_stop_tasks(client):
    # This is testing the top-level task endpoints
    # Since we can't easily create a long-running task to stop in this test environment without more complex setup,
    # we'll just test the list endpoint and ensure it returns a valid structure.
    
    tasks_response = await client.tasks.list_tasks()
    assert isinstance(tasks_response, dict)
    assert "tasks" in tasks_response
    assert isinstance(tasks_response["tasks"], list)
    
    # We can try to stop a non-existent task.
    # The backend returns {"status": False, ...} for non-existent tasks (it does not raise 404).
    response = await client.tasks.stop_task("non-existent-task-id")
    assert response["status"] is False

