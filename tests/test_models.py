import pytest
import time
from owui_client.models.models import (
    ModelForm,
    ModelMeta,
    ModelParams,
    ModelListResponse,
)

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio


async def test_models_client_initialization(client):
    assert client.models is not None


async def test_model_crud_lifecycle(client):
    """
    Test create, get, update, toggle, delete lifecycle for a model.
    """
    # 1. Create a model
    model_id = f"test_model_{int(time.time())}"
    model_name = "Test Model"
    model_meta = ModelMeta(description="A test model description")
    model_params = ModelParams()

    form_data = ModelForm(
        id=model_id,
        base_model_id="gpt-3.5-turbo",
        name=model_name,
        meta=model_meta,
        params=model_params,
        is_active=True,
    )

    created_model = await client.models.create_new_model(form_data)
    assert created_model is not None
    assert created_model.id == model_id
    assert created_model.name == model_name

    # 2. Get model by ID
    fetched_model = await client.models.get_model_by_id(model_id)
    assert fetched_model is not None
    assert fetched_model.id == model_id

    # 3. List models
    models_list = await client.models.get_models()
    assert isinstance(models_list, ModelListResponse)
    found = any(m.id == model_id for m in models_list.items)
    assert found

    # 4. Update model
    new_name = "Updated Test Model"
    form_data.name = new_name
    updated_model = await client.models.update_model_by_id(form_data)
    assert updated_model is not None
    assert updated_model.name == new_name

    # 5. Toggle model
    # First check current status
    assert updated_model.is_active is True
    toggled_model = await client.models.toggle_model_by_id(model_id)
    assert toggled_model is not None
    assert toggled_model.is_active is False

    # Toggle back
    toggled_model = await client.models.toggle_model_by_id(model_id)
    assert toggled_model.is_active is True

    # 6. Delete model
    deleted = await client.models.delete_model_by_id(model_id)
    assert deleted is True

    # Verify deletion
    try:
        await client.models.get_model_by_id(model_id)
        assert False, "Model should have been deleted"
    except Exception:
        pass


async def test_get_base_models(client):
    base_models = await client.models.get_base_models()
    assert isinstance(base_models, list)


async def test_get_model_tags(client):
    tags = await client.models.get_model_tags()
    assert isinstance(tags, list)


async def test_export_models(client):
    models = await client.models.export_models()
    assert isinstance(models, list)

