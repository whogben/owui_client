import pytest

@pytest.mark.asyncio
async def test_get_version(client):
    version = await client.root.get_version()
    assert version is not None
    assert "version" in version

@pytest.mark.asyncio
async def test_get_changelog(client):
    changelog = await client.root.get_changelog()
    assert changelog is not None
    assert isinstance(changelog, dict)

@pytest.mark.asyncio
async def test_health(client):
    health = await client.root.health()
    assert health is not None
    assert health.get("status") is True

@pytest.mark.asyncio
async def test_get_config(client):
    config = await client.root.get_config()
    assert config is not None
    assert "version" in config

@pytest.mark.asyncio
async def test_get_models(client):
    models = await client.root.get_models()
    assert models is not None
    assert "data" in models
    assert isinstance(models["data"], list)
