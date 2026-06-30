import pytest
import time
from owui_client.models.models import (
    ModelForm,
    ModelMeta,
    ModelParams,
    ModelAccessGrantsForm,
)
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
        params=ModelParams(),
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
        # Backend returns 404 for not found
        assert e.response.status_code == 404


async def test_get_base_model_tags(client):
    """
    Test the admin-only GET /base/tags endpoint.

    Creates a base model with a tag in its meta, asserts the tag is returned,
    then asserts the empty-list shape is also valid.
    """
    import time

    tag_name = f"base_tag_{int(time.time())}"
    model_id = f"test_base_tags_{int(time.time())}"

    form_data = ModelForm(
        id=model_id,
        name="Base Tags Test Model",
        meta=ModelMeta(description="base tags test", tags=[{"name": tag_name}]),
        params=ModelParams(),
    )

    created_model = await client.models.create_new_model(form_data)
    assert created_model is not None

    try:
        # The created model has no base_model_id, so it is a base model.
        tags = await client.models.get_base_model_tags()
        assert isinstance(tags, list)
        assert tag_name in tags
    finally:
        assert await client.models.delete_model_by_id(model_id) is True


async def test_update_model_access(client):
    """
    Test updating model access grants.
    """
    # Create a model
    model_id = f"test_model_access_{int(time.time())}"
    form_data = ModelForm(
        id=model_id,
        name="Test Model Access",
        meta=ModelMeta(description="A test model for access grants"),
        params=ModelParams(),
    )

    created_model = await client.models.create_new_model(form_data)
    assert created_model is not None
    assert created_model.id == model_id

    try:
        # Update access grants - grant public read access
        access_form = ModelAccessGrantsForm(
            id=model_id,
            access_grants=[
                {"principal_type": "user", "principal_id": "*", "permission": "read"}
            ],
        )

        updated_model = await client.models.update_model_access(access_form)
        assert updated_model is not None
        assert updated_model.id == model_id
        # Verify access_grants are present
        assert len(updated_model.access_grants) == 1
        assert updated_model.access_grants[0].principal_type == "user"
        assert updated_model.access_grants[0].principal_id == "*"
        assert updated_model.access_grants[0].permission == "read"
    finally:
        assert await client.models.delete_model_by_id(model_id) is True

async def test_update_model_preserves_access_grants(client):
    """
    Regression test: updating a model without specifying `access_grants` must
    preserve the model's existing sharing grants rather than silently wiping them.

    The backend's `set_access_grants` deletes and re-inserts grants from whatever
    non-None list it receives, so sending `[]` clears them. `update_model_by_id`
    must therefore re-send the model's current grants when the caller omits them.
    """
    model_id = f"test_model_preserve_{int(time.time())}"
    form_data = ModelForm(
        id=model_id,
        name="Preserve Grants Test",
        meta=ModelMeta(description="model whose grants must survive an update"),
        params=ModelParams(),
    )

    created_model = await client.models.create_new_model(form_data)
    assert created_model is not None

    try:
        # Grant the model public read access so it has a non-empty grant list.
        access_form = ModelAccessGrantsForm(
            id=model_id,
            access_grants=[
                {"principal_type": "user", "principal_id": "*", "permission": "read"}
            ],
        )
        granted = await client.models.update_model_access(access_form)
        assert granted is not None
        assert len(granted.access_grants) == 1

        # Update the model's name WITHOUT specifying access_grants. A naive client
        # would send access_grants=[] here and wipe the public-read grant.
        update_form = ModelForm(
            id=model_id,
            name="Preserve Grants Test (renamed)",
            meta=ModelMeta(description="updated description"),
            params=ModelParams(),
        )
        updated_model = await client.models.update_model_by_id(update_form)
        assert updated_model is not None
        assert updated_model.name == "Preserve Grants Test (renamed)"

        # Re-fetch and confirm the public-read grant survived the update.
        fetched = await client.models.get_model_by_id(model_id)
        assert fetched is not None
        assert len(fetched.access_grants) == 1, (
            f"access_grants were wiped on update; got {fetched.access_grants!r}"
        )
        assert fetched.access_grants[0].principal_type == "user"
        assert fetched.access_grants[0].principal_id == "*"
        assert fetched.access_grants[0].permission == "read"

        # Sanity check the contrasting behavior: an explicit [] DOES clear grants.
        clear_form = ModelForm(
            id=model_id,
            name="Preserve Grants Test (renamed)",
            meta=ModelMeta(description="updated description"),
            params=ModelParams(),
            access_grants=[],
        )
        cleared = await client.models.update_model_by_id(clear_form)
        assert cleared is not None
        fetched_after_clear = await client.models.get_model_by_id(model_id)
        assert fetched_after_clear is not None
        assert fetched_after_clear.access_grants == []
    finally:
        assert await client.models.delete_model_by_id(model_id) is True
