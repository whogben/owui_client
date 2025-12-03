import pytest
from owui_client.models.openai import OpenAIConfigForm, ConnectionVerificationForm


@pytest.mark.asyncio
async def test_configure_mock_openai(client, mock_openai_server):
    """
    Test that we can configure Open WebUI to use our mock OpenAI server
    and verify that models are fetched.
    """
    # 1. Get current config
    config = await client.openai.get_config()
    assert "ENABLE_OPENAI_API" in config

    # 2. Update config to point to our mock server
    new_config = OpenAIConfigForm(
        ENABLE_OPENAI_API=True,
        OPENAI_API_BASE_URLS=[mock_openai_server],
        OPENAI_API_KEYS=["sk-mock-key"],
        OPENAI_API_CONFIGS={"0": {"enable": True}},
    )

    updated_config = await client.openai.update_config(new_config)

    assert updated_config["ENABLE_OPENAI_API"] is True
    assert updated_config["OPENAI_API_BASE_URLS"][0] == mock_openai_server

    # 3. Verify we can now see the mock models (this indirectly tests the connection)
    models = await client.openai.get_models()
    assert "data" in models
    # We expect at least gpt-3.5-turbo and gpt-4 from mock server
    assert len(models["data"]) >= 2

    found_model = False
    for m in models["data"]:
        if m["id"] == "gpt-3.5-turbo":
            found_model = True
            break
    assert found_model


@pytest.mark.asyncio
async def test_verify_connection(client, mock_openai_server):
    form = ConnectionVerificationForm(url=mock_openai_server, key="sk-mock-key")

    res = await client.openai.verify_connection(form)
    # Based on backend, it returns the response from /models
    assert "data" in res
    assert len(res["data"]) >= 2


@pytest.mark.asyncio
async def test_chat_completions(client, mock_openai_server):
    # Setup config first to ensure the server allows the request
    new_config = OpenAIConfigForm(
        ENABLE_OPENAI_API=True,
        OPENAI_API_BASE_URLS=[mock_openai_server],
        OPENAI_API_KEYS=["sk-mock-key"],
        OPENAI_API_CONFIGS={"0": {"enable": True}},
    )
    await client.openai.update_config(new_config)

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Hello"}],
    }

    res = await client.openai.chat_completions(payload)
    assert "choices" in res
    assert (
        res["choices"][0]["message"]["content"]
        == "This is a mock response from the test provider."
    )


@pytest.mark.asyncio
async def test_embeddings(client, mock_openai_server):
    # Setup config
    new_config = OpenAIConfigForm(
        ENABLE_OPENAI_API=True,
        OPENAI_API_BASE_URLS=[mock_openai_server],
        OPENAI_API_KEYS=["sk-mock-key"],
        OPENAI_API_CONFIGS={"0": {"enable": True}},
    )
    await client.openai.update_config(new_config)

    payload = {"model": "text-embedding-ada-002", "input": "Hello world"}

    res = await client.openai.embeddings(payload)
    assert "data" in res
    assert res["data"][0]["embedding"] == [0.1, 0.2, 0.3]


@pytest.mark.asyncio
@pytest.mark.xfail(
    reason="Backend limitation: /audio/speech hardcodes use of 'https://api.openai.com/v1', preventing use of custom/mock providers."
)
async def test_speech(client, mock_openai_server):
    # Setup config
    new_config = OpenAIConfigForm(
        ENABLE_OPENAI_API=True,
        OPENAI_API_BASE_URLS=[mock_openai_server],
        OPENAI_API_KEYS=["sk-mock-key"],
        OPENAI_API_CONFIGS={"0": {"enable": True}},
    )
    await client.openai.update_config(new_config)

    payload = {"model": "tts-1", "input": "Hello world", "voice": "alloy"}

    # Note: speech returns bytes
    res = await client.openai.speech(payload)
    assert res == b"FAKE_MP3_DATA"
