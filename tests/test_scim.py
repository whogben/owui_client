import pytest
from owui_client.models.scim import (
    SCIMEmail,
    SCIMGroupCreateRequest,
    SCIMGroupMember,
    SCIMName,
    SCIMPatchOperation,
    SCIMPatchRequest,
    SCIMUserCreateRequest,
)

pytestmark = pytest.mark.asyncio


async def test_scim_public_endpoints(client):
    """Test public SCIM endpoints.

    Skips if SCIM is not enabled on the test server, since the router
    is only mounted when ENABLE_SCIM is set.
    """
    config = await client.scim.get_service_provider_config()
    if not isinstance(config, dict):
        pytest.skip("SCIM is not enabled on this server")

    assert "schemas" in config
    assert config["patch"]["supported"] is True

    resource_types = await client.scim.get_resource_types()
    assert isinstance(resource_types, list)
    ids = [rt.get("id") for rt in resource_types]
    assert "User" in ids
    assert "Group" in ids

    schemas = await client.scim.get_schemas()
    assert isinstance(schemas, list)
    schema_ids = [s.get("id") for s in schemas]
    assert "urn:ietf:params:scim:schemas:core:2.0:User" in schema_ids


async def test_scim_models_serialization():
    """Test SCIM model instantiation and JSON serialization.

    Verifies that request models can be created and dumped correctly,
    including alias handling for fields like `$ref`.
    """
    email = SCIMEmail(value="test@example.com", type="work", primary=True)
    name = SCIMName(givenName="Test", familyName="User", formatted="Test User")

    user_req = SCIMUserCreateRequest(
        userName="test@example.com",
        displayName="Test User",
        emails=[email],
        name=name,
        active=True,
    )
    user_data = user_req.model_dump(by_alias=True)
    assert user_data["userName"] == "test@example.com"
    assert user_data["displayName"] == "Test User"
    assert user_data["emails"][0]["value"] == "test@example.com"

    member = SCIMGroupMember(
        value="user-id",
        display="Test User",
        **{"$ref": "http://example.com/Users/user-id"},
    )
    group_req = SCIMGroupCreateRequest(
        displayName="Test Group",
        members=[member],
    )
    group_data = group_req.model_dump(by_alias=True)
    assert group_data["displayName"] == "Test Group"
    assert group_data["members"][0]["value"] == "user-id"
    assert group_data["members"][0]["$ref"] == "http://example.com/Users/user-id"

    patch = SCIMPatchRequest(
        Operations=[
            SCIMPatchOperation(op="replace", path="displayName", value="New Name")
        ]
    )
    patch_data = patch.model_dump(by_alias=True)
    assert patch_data["Operations"][0]["op"] == "replace"
    assert patch_data["Operations"][0]["path"] == "displayName"
    assert patch_data["Operations"][0]["value"] == "New Name"
