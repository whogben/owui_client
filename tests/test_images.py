import pytest
from owui_client.models.images import ImagesConfig, CreateImageForm, EditImageForm

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio


async def test_images_config(client):
    """
    Test getting and updating images configuration.
    """
    # 1. Get current config
    config = await client.images.get_config()
    assert config is not None
    assert isinstance(config, ImagesConfig)

    # 2. Update config (toggle ENABLE_IMAGE_GENERATION)
    original_state = config.ENABLE_IMAGE_GENERATION
    config.ENABLE_IMAGE_GENERATION = not original_state
    
    # Backend validation might require other fields to be consistent if we send them all back.
    # ImagesConfig includes many fields. The client sends the whole model dump.
    
    updated_config = await client.images.update_config(config)
    assert updated_config.ENABLE_IMAGE_GENERATION != original_state
    assert updated_config.ENABLE_IMAGE_GENERATION == config.ENABLE_IMAGE_GENERATION

    # 3. Verify persistence
    config_check = await client.images.get_config()
    assert config_check.ENABLE_IMAGE_GENERATION == updated_config.ENABLE_IMAGE_GENERATION

    # 4. Revert
    config.ENABLE_IMAGE_GENERATION = original_state
    await client.images.update_config(config)


async def test_get_models(client):
    """
    Test getting available image models.
    """
    models = await client.images.get_models()
    assert isinstance(models, list)
    # Even if empty, it should be a list.
    # If the default engine is openai, it returns a hardcoded list.
    # If not configured, it might error or return empty.
    
    if len(models) > 0:
        assert "id" in models[0]
        assert "name" in models[0]


async def test_verify_url(client):
    """
    Test verifying image generation URL.
    """
    # This depends on configuration. If configured to 'openai', verify_url returns True immediately.
    # Let's ensure engine is OpenAI for this test to pass easily.
    
    config = await client.images.get_config()
    original_engine = config.IMAGE_GENERATION_ENGINE
    
    # Set to 'openai' if not
    if config.IMAGE_GENERATION_ENGINE != "openai":
        config.IMAGE_GENERATION_ENGINE = "openai"
        await client.images.update_config(config)
        
    try:
        result = await client.images.verify_url()
        assert result is True
    finally:
        # Restore engine
        if original_engine != "openai":
            config.IMAGE_GENERATION_ENGINE = original_engine
            await client.images.update_config(config)

