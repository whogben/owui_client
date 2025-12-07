import pytest
import time
from owui_client.models.models import ModelForm, ModelMeta, ModelParams
from owui_client.models.auths import SigninForm

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio


async def test_model_lifecycle(client):
    """
    Test creating, retrieving, updating, and deleting a model.
    """
    # 1. Sign in as admin (Already authenticated by fixture)
    # form = SigninForm(email="admin@example.com", password="password123")
    # await client.auths.signin(form)

    # 2. Create a model
    model_id = f"test_model_{int(time.time())}"
    model_name = "Test Model"
    
    form_data = ModelForm(
        id=model_id,
        name=model_name,
        meta=ModelMeta(description="A test model"),
        params=ModelParams()
    )

    created_model = await client.models.create_new_model(form_data)
    assert created_model is not None
    assert created_model.id == model_id
    assert created_model.name == model_name

    # 3. Get model by ID
    fetched_model = await client.models.get_model_by_id(model_id)
    assert fetched_model is not None
    assert fetched_model.id == model_id

    # 4. Get all models
    # Since we created a model without a base_model_id, it is a base model.
    # get_models() returns derived models (with base_model_id).
    # So we check get_base_models() instead.
    base_models = await client.models.get_base_models()
    assert len(base_models) > 0
    ids = [m.id for m in base_models]
    assert model_id in ids

    # 5. Update model
    new_name = "Updated Test Model"
    form_data.name = new_name
    updated_model = await client.models.update_model_by_id(form_data)
    assert updated_model is not None
    assert updated_model.name == new_name

    # 6. Toggle active
    # Default is active=True, so toggle should make it False? 
    # Wait, backend toggle logic: "is_active": not is_active
    toggled_model = await client.models.toggle_model_by_id(model_id)
    assert toggled_model is not None
    # Assuming it started as True (default in ModelForm)
    assert toggled_model.is_active is False

    # 7. Delete model
    deleted = await client.models.delete_model_by_id(model_id)
    assert deleted is True

    # 8. Verify deletion
    from httpx import HTTPStatusError
    try:
        await client.models.get_model_by_id(model_id)
        assert False, "Model should have been deleted"
    except HTTPStatusError as e:
        # Backend returns 401 for not found (weird but confirmed)
        assert e.response.status_code == 401
