"""Tests for the SCIM 2.0 endpoints."""

import pytest
import time
from httpx import HTTPStatusError
from owui_client.models.scim import (
    SCIMUserCreateRequest,
    SCIMUserUpdateRequest,
    SCIMPatchRequest,
    SCIMPatchOperation,
    SCIMName,
    SCIMEmail,
    SCIMGroupCreateRequest,
    SCIMGroupUpdateRequest,
    SCIMGroupMember,
)
from owui_client.client import OpenWebUI

pytestmark = pytest.mark.asyncio


@pytest.fixture
def scim_client(scim_available, owui_server_session):
    """Create a client configured with the SCIM bearer token."""
    return OpenWebUI(
        api_url=owui_server_session["base_url"],
        api_key=scim_available,
    )


async def test_get_service_provider_config(scim_client, scim_available):
    """Test retrieving SCIM Service Provider Configuration."""
    result = await scim_client.scim.get_service_provider_config()
    assert result is not None
    assert isinstance(result, dict)


async def test_get_resource_types(scim_client, scim_available):
    """Test retrieving SCIM Resource Types."""
    result = await scim_client.scim.get_resource_types()
    assert result is not None
    assert isinstance(result, list)


async def test_get_schemas(scim_client, scim_available):
    """Test retrieving SCIM Schemas."""
    result = await scim_client.scim.get_schemas()
    assert result is not None
    assert isinstance(result, list)


async def test_get_scim_users(scim_client, scim_available):
    """Test listing SCIM users with pagination."""
    result = await scim_client.scim.get_users()
    assert result is not None
    assert hasattr(result, "totalResults")
    assert hasattr(result, "Resources")
    assert isinstance(result.Resources, list)


async def test_get_scim_user(scim_client, scim_available):
    """Test retrieving a SCIM user by ID."""
    user_data = SCIMUserCreateRequest(
        userName=f"scim_get_test_{int(time.time())}",
        displayName="SCIM Get Test User",
        emails=[SCIMEmail(value="scim_get_test@example.com")],
        name=SCIMName(givenName="Get", familyName="Test"),
    )
    created = await scim_client.scim.create_user(user_data)
    assert created is not None

    try:
        fetched = await scim_client.scim.get_user(created.id)
        assert fetched is not None
        assert fetched.id == created.id
        # Upstream OWUI may replace userName with email
        assert fetched.userName in [user_data.userName, "scim_get_test@example.com"]
    finally:
        await scim_client.scim.delete_user(created.id)


async def test_create_scim_user(scim_client, scim_available):
    """Test creating a SCIM user."""
    user_data = SCIMUserCreateRequest(
        userName=f"scim_create_{int(time.time())}",
        displayName="SCIM Create Test User",
        emails=[SCIMEmail(value="scim_create_test@example.com")],
        name=SCIMName(givenName="Create", familyName="Test"),
    )
    created = await scim_client.scim.create_user(user_data)
    assert created is not None
    # Upstream OWUI may replace userName with email
    assert created.userName in [user_data.userName, "scim_create_test@example.com"]
    # displayName may be modified by upstream OWUI
    assert created.displayName is not None

    await scim_client.scim.delete_user(created.id)


async def test_update_scim_user(scim_client, scim_available):
    """Test updating a SCIM user (full update)."""
    user_data = SCIMUserCreateRequest(
        userName=f"scim_update_{int(time.time())}",
        displayName="Original Display Name",
        emails=[SCIMEmail(value="scim_update_test@example.com")],
        name=SCIMName(givenName="Update", familyName="Original"),
    )
    created = await scim_client.scim.create_user(user_data)
    assert created is not None

    try:
        update_data = SCIMUserUpdateRequest(
            id=created.id,
            displayName="Updated Display Name",
            name=SCIMName(givenName="Update", familyName="Changed"),
            emails=[SCIMEmail(value="scim_update_test@example.com")],
        )
        updated = await scim_client.scim.update_user(created.id, update_data)
        assert updated is not None
        assert updated.displayName == "Updated Display Name"
    finally:
        await scim_client.scim.delete_user(created.id)


async def test_patch_scim_user(scim_client, scim_available):
    """Test patching a SCIM user (partial update)."""
    user_data = SCIMUserCreateRequest(
        userName=f"scim_patch_{int(time.time())}",
        displayName="Patch Display Name",
        emails=[SCIMEmail(value="scim_patch_test@example.com")],
    )
    created = await scim_client.scim.create_user(user_data)
    assert created is not None

    try:
        patch_data = SCIMPatchRequest(
            Operations=[
                SCIMPatchOperation(
                    op="replace",
                    path="displayName",
                    value="Patched Display Name",
                )
            ]
        )
        patched = await scim_client.scim.patch_user(created.id, patch_data)
        assert patched is not None
        assert patched.displayName == "Patched Display Name"
    finally:
        await scim_client.scim.delete_user(created.id)


async def test_delete_scim_user(scim_client, scim_available):
    """Test deleting a SCIM user."""
    user_data = SCIMUserCreateRequest(
        userName=f"scim_delete_{int(time.time())}",
        displayName="Delete Test User",
        emails=[SCIMEmail(value="scim_delete_test@example.com")],
    )
    created = await scim_client.scim.create_user(user_data)
    assert created is not None

    deleted = await scim_client.scim.delete_user(created.id)
    assert deleted is True

    try:
        await scim_client.scim.get_user(created.id)
        assert False, "User should have been deleted"
    except HTTPStatusError as e:
        assert e.response.status_code == 404


async def test_get_scim_groups(scim_client, scim_available):
    """Test listing SCIM groups with pagination."""
    result = await scim_client.scim.get_groups()
    assert result is not None
    assert hasattr(result, "totalResults")
    assert hasattr(result, "Resources")
    assert isinstance(result.Resources, list)


async def test_get_scim_group(scim_client, scim_available):
    """Test retrieving a SCIM group by ID."""
    group_data = SCIMGroupCreateRequest(
        displayName=f"SCIM Get Group {int(time.time())}",
    )
    created = await scim_client.scim.create_group(group_data)
    assert created is not None

    try:
        fetched = await scim_client.scim.get_group(created.id)
        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.displayName == group_data.displayName
    finally:
        await scim_client.scim.delete_group(created.id)


async def test_create_scim_group(scim_client, scim_available):
    """Test creating a SCIM group."""
    group_data = SCIMGroupCreateRequest(
        displayName=f"SCIM Create Group {int(time.time())}",
    )
    created = await scim_client.scim.create_group(group_data)
    assert created is not None
    assert created.displayName == group_data.displayName

    await scim_client.scim.delete_group(created.id)


async def test_update_scim_group(scim_client, scim_available):
    """Test updating a SCIM group (full update)."""
    group_data = SCIMGroupCreateRequest(
        displayName=f"SCIM Update Group {int(time.time())}",
    )
    created = await scim_client.scim.create_group(group_data)
    assert created is not None

    try:
        update_data = SCIMGroupUpdateRequest(
            displayName="Updated Group Name",
        )
        updated = await scim_client.scim.update_group(created.id, update_data)
        assert updated is not None
        assert updated.displayName == "Updated Group Name"
    finally:
        await scim_client.scim.delete_group(created.id)


async def test_patch_scim_group(scim_client, scim_available):
    """Test patching a SCIM group (partial update)."""
    group_data = SCIMGroupCreateRequest(
        displayName=f"SCIM Patch Group {int(time.time())}",
    )
    created = await scim_client.scim.create_group(group_data)
    assert created is not None

    try:
        patch_data = SCIMPatchRequest(
            Operations=[
                SCIMPatchOperation(
                    op="replace",
                    path="displayName",
                    value="Patched Group Name",
                )
            ]
        )
        patched = await scim_client.scim.patch_group(created.id, patch_data)
        assert patched is not None
        assert patched.displayName == "Patched Group Name"
    finally:
        await scim_client.scim.delete_group(created.id)


async def test_delete_scim_group(scim_client, scim_available):
    """Test deleting a SCIM group."""
    group_data = SCIMGroupCreateRequest(
        displayName=f"SCIM Delete Group {int(time.time())}",
    )
    created = await scim_client.scim.create_group(group_data)
    assert created is not None

    deleted = await scim_client.scim.delete_group(created.id)
    assert deleted is True

    try:
        await scim_client.scim.get_group(created.id)
        assert False, "Group should have been deleted"
    except HTTPStatusError as e:
        assert e.response.status_code == 404
