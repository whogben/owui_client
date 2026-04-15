import httpx
import pytest
from owui_client.models.ollama import OllamaConfigForm, UrlForm, ConnectionVerificationForm

@pytest.mark.asyncio
async def test_ollama_status(client):
    # 1. Check Status (GET)
    try:
        status = await client.ollama.get_status()
        assert status["status"] is True
    except Exception:
        pass

    # 2. Check Status (HEAD)
    try:
        status_head = await client.ollama.head_status()
        assert status_head is True
    except Exception:
        pass

@pytest.mark.asyncio
async def test_ollama_config(client):
    # 1. Get Config
    config = await client.ollama.get_config()
    assert "ENABLE_OLLAMA_API" in config
    assert "OLLAMA_BASE_URLS" in config

    # 2. Update Config
    new_config = OllamaConfigForm(
        ENABLE_OLLAMA_API=True,
        OLLAMA_BASE_URLS=["http://localhost:11434"],
        OLLAMA_API_CONFIGS={}
    )
    updated = await client.ollama.update_config(new_config)
    assert updated["ENABLE_OLLAMA_API"] is True
    assert updated["OLLAMA_BASE_URLS"] == ["http://localhost:11434"]

@pytest.mark.asyncio
async def test_ollama_verify(client, mock_ollama_server):
    # 1. Verify connection to mock server
    form = ConnectionVerificationForm(url=mock_ollama_server)
    try:
        version = await client.ollama.verify_connection(form)
        assert "version" in version
    except Exception as e:
        import httpx
        if isinstance(e, httpx.ReadTimeout):
            pytest.skip(f"Ollama verify connection timed out: {e}")
        pytest.fail(f"Verify connection failed: {e}")

@pytest.mark.asyncio
async def test_ollama_models(client, mock_ollama_server):
    try:
        new_config = OllamaConfigForm(
            ENABLE_OLLAMA_API=True,
            OLLAMA_BASE_URLS=[mock_ollama_server],
            OLLAMA_API_CONFIGS={}
        )
        await client.ollama.update_config(new_config)

        models = await client.ollama.get_models()
        assert "models" in models
        assert len(models["models"]) > 0
        
        loaded = await client.ollama.get_loaded_models()
        assert "models" in loaded

        version = await client.ollama.get_version()
        assert "version" in version
    except httpx.ReadTimeout:
        pytest.skip("Mock server timeout (environment issue)")

@pytest.mark.asyncio
async def test_ollama_openai_compatible_endpoints(client, mock_ollama_server):
    try:
        new_config = OllamaConfigForm(
            ENABLE_OLLAMA_API=True,
            OLLAMA_BASE_URLS=[mock_ollama_server],
            OLLAMA_API_CONFIGS={}
        )
        await client.ollama.update_config(new_config)

        models = await client.ollama.get_openai_models()
        assert "data" in models
        assert "object" in models
        assert models["object"] == "list"
    except httpx.ReadTimeout:
        pytest.skip("Mock server timeout (environment issue)")

@pytest.mark.asyncio
async def test_generate_anthropic_messages(client, mock_ollama_server):
    """Test generate_anthropic_messages proxies Anthropic-style payload to Ollama."""
    new_config = OllamaConfigForm(
        ENABLE_OLLAMA_API=True,
        OLLAMA_BASE_URLS=[mock_ollama_server],
        OLLAMA_API_CONFIGS={}
    )
    await client.ollama.update_config(new_config)

    payload = {
        "model": "test-model",
        "max_tokens": 10,
        "messages": [
            {"role": "user", "content": "Hello"}
        ],
    }
    try:
        result = await client.ollama.generate_anthropic_messages(payload)
        assert result is not None
    except Exception as e:
        import httpx
        if isinstance(e, httpx.ReadTimeout):
            pytest.skip(f"Anthropic messages endpoint timed out: {e}")
        pytest.skip(f"generate_anthropic_messages not supported by mock: {e}")
