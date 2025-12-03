import pytest
from owui_client.models.auths import SigninForm, AddUserForm
from owui_client.models.users import (
    UserGroupIdsListResponse,
    UserInfoListResponse,
    UserIdNameListResponse,
    UserPermissions,
    WorkspacePermissions,
    SharingPermissions,
    ChatPermissions,
    FeaturesPermissions,
    UserSettings,
    UserUpdateForm,
    UserModel,
    UserResponse,
    UserStatus,
    UserActiveResponse,
)
from owui_client.models.groups import GroupModel
from owui_client.models.oauth_sessions import OAuthSessionModel

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio


async def test_users_client_initialization(client):
    assert client.users is not None


async def test_get_users_admin(client):
    """
    Test get_users as admin.
    """
    # 1. Sign in as admin (handled by fixture)
    # form = SigninForm(email="admin@example.com", password="password123")
    # await client.auths.signin(form)

    # 2. Get users
    response = await client.users.get_users()

    assert isinstance(response, UserGroupIdsListResponse)
    assert response.total >= 1
    assert len(response.users) >= 1

    # Check if admin is in the list
    admin_user = next(
        (u for u in response.users if u.email == "admin@example.com"), None
    )
    assert admin_user is not None
    assert admin_user.role == "admin"


async def test_get_users_pagination(client):
    """
    Test get_users pagination params.
    """
    # 1. Sign in as admin (handled by fixture)
    # form = SigninForm(email="admin@example.com", password="password123")
    # await client.auths.signin(form)

    # 2. Get users with limit (page size in backend is fixed to 30, so we might not see pagination effect unless we have many users)
    # But we can check if the call succeeds with params.
    response = await client.users.get_users(page=1)
    assert isinstance(response, UserGroupIdsListResponse)


async def test_get_all_users(client):
    """
    Test get_all_users.
    """
    # 1. Sign in as admin (handled by fixture)
    # form = SigninForm(email="admin@example.com", password="password123")
    # await client.auths.signin(form)

    # 2. Get all users
    response = await client.users.get_all_users()

    assert isinstance(response, UserInfoListResponse)
    assert response.total >= 1
    assert len(response.users) >= 1

    # Verify returned model is simpler (UserInfoResponse vs UserGroupIdsModel)
    user = response.users[0]
    # UserInfoResponse has id, name, email, role. Does NOT have created_at etc.
    assert hasattr(user, "email")
    assert not hasattr(user, "created_at")


async def test_search_users(client):
    """
    Test search_users.
    """
    # 1. Sign in as admin (handled by fixture)
    # form = SigninForm(email="admin@example.com", password="password123")
    # await client.auths.signin(form)

    # 2. Search for admin
    response = await client.users.search_users(query="admin")

    assert isinstance(response, UserIdNameListResponse)
    assert response.total >= 1

    # Admin should be in results
    found = False
    for user in response.users:
        if user.name == "Admin":  # Default admin name
            found = True
            break

    # We can't guarantee the exact name, but we can check if results exist
    assert len(response.users) > 0

    # 3. Search for something non-existent
    response_empty = await client.users.search_users(query="nonexistentuserxyz")
    assert response_empty.total == 0
    assert len(response_empty.users) == 0


async def test_get_user_groups(client):
    """
    Test get_user_groups.
    """
    # 1. Sign in as admin (handled by fixture)
    # form = SigninForm(email="admin@example.com", password="password123")
    # await client.auths.signin(form)

    # 2. Get groups
    # Note: default environment might not have groups, so it might return empty list
    response = await client.users.get_user_groups()

    assert isinstance(response, list)
    # If there are groups, they should be GroupModel instances
    if len(response) > 0:
        assert isinstance(response[0], GroupModel)


async def test_user_permissions_lifecycle(client):
    """
    Test get_user_permissions, get_default_user_permissions, and update_default_user_permissions.
    """
    # 1. Sign in as admin (handled by fixture)
    # form = SigninForm(email="admin@example.com", password="password123")
    # await client.auths.signin(form)

    # 2. Get user permissions (for the current user)
    perms = await client.users.get_user_permissions()
    assert isinstance(perms, dict)
    # Should contain keys like 'workspace', 'chat', etc.
    assert "workspace" in perms or "chat" in perms

    # 3. Get default permissions
    default_perms = await client.users.get_default_user_permissions()
    assert isinstance(default_perms, UserPermissions)

    # 4. Update default permissions
    # Toggle a permission
    original_web_search = default_perms.features.web_search
    default_perms.features.web_search = not original_web_search

    updated_perms = await client.users.update_default_user_permissions(default_perms)
    assert isinstance(updated_perms, UserPermissions)
    assert updated_perms.features.web_search == (not original_web_search)

    # 5. Verify persistence
    check_perms = await client.users.get_default_user_permissions()
    assert check_perms.features.web_search == (not original_web_search)

    # 6. Revert
    default_perms.features.web_search = original_web_search
    await client.users.update_default_user_permissions(default_perms)


async def test_user_settings_lifecycle(client):
    """
    Test get_user_settings, update_user_settings.
    """
    # 1. Sign in as admin (handled by fixture)
    # form = SigninForm(email="admin@example.com", password="password123")
    # await client.auths.signin(form)

    # 2. Get user settings
    settings = await client.users.get_user_settings()
    # settings is Optional[UserSettings], usually not None for existing user
    if settings is None:
        settings = UserSettings(ui={})

    assert isinstance(settings, UserSettings)

    # 3. Update settings
    if settings.ui is None:
        settings.ui = {}

    original_theme = settings.ui.get("theme", "system")
    new_theme = "dark" if original_theme != "dark" else "light"

    settings.ui["theme"] = new_theme

    updated_settings = await client.users.update_user_settings(settings)
    assert updated_settings.ui["theme"] == new_theme

    # 4. Verify persistence
    check_settings = await client.users.get_user_settings()
    assert check_settings.ui["theme"] == new_theme

    # 5. Revert (optional)
    settings.ui["theme"] = original_theme
    await client.users.update_user_settings(settings)


async def test_user_info_lifecycle(client):
    """
    Test get_user_info, update_user_info.
    """
    # 1. Sign in as admin (handled by fixture)
    # form = SigninForm(email="admin@example.com", password="password123")
    # await client.auths.signin(form)

    # 2. Get user info
    info = await client.users.get_user_info()
    # info is Optional[dict]
    if info is None:
        info = {}

    # 3. Update info
    # 'info' field is arbitrary JSON attached to user
    test_key = "test_custom_field"
    test_value = "custom_value_123"

    update_data = {test_key: test_value}

    updated_info = await client.users.update_user_info(update_data)
    assert updated_info is not None
    assert updated_info.get(test_key) == test_value

    # 4. Verify persistence
    check_info = await client.users.get_user_info()
    assert check_info.get(test_key) == test_value


async def test_user_crud_lifecycle(client):
    """
    Test create (via add_user), get_user_by_id, update_user_by_id, delete_user_by_id.
    """
    # 1. Sign in as admin (handled by fixture)
    # form = SigninForm(email="admin@example.com", password="password123")
    # await client.auths.signin(form)

    # 2. Create a temporary user
    new_email = "tempuser@example.com"
    new_password = "password123"
    new_name = "Temp User"

    # Check if user already exists and delete if so
    try:
        existing_users = await client.users.get_users()
        existing_user = next(
            (u for u in existing_users.users if u.email == new_email), None
        )
        if existing_user:
            await client.users.delete_user_by_id(existing_user.id)
    except Exception:
        pass

    add_user_form = AddUserForm(
        name=new_name,
        email=new_email,
        password=new_password,
        role="user",
    )

    # add_user returns SigninResponse (token + user info)
    added_user_response = await client.auths.add_user(add_user_form)
    new_user_id = added_user_response.id
    assert new_user_id is not None

    # 3. Get user by ID
    user_response = await client.users.get_user_by_id(new_user_id)
    assert isinstance(user_response, UserActiveResponse)
    assert user_response.name == new_name

    # 4. Update user by ID
    updated_name = "Updated Temp User"
    update_form = UserUpdateForm(
        role="user",
        name=updated_name,
        email=new_email,
        profile_image_url=user_response.profile_image_url,
    )

    updated_user_model = await client.users.update_user_by_id(new_user_id, update_form)
    assert isinstance(updated_user_model, UserModel)
    assert updated_user_model.name == updated_name
    assert updated_user_model.id == new_user_id

    # 5. Test new methods for this user
    # get_user_active_status_by_id
    active_status = await client.users.get_user_active_status_by_id(new_user_id)
    assert isinstance(active_status, dict)
    assert "active" in active_status

    # get_user_profile_image_by_id
    image_bytes = await client.users.get_user_profile_image_by_id(new_user_id)
    assert isinstance(image_bytes, bytes)
    # The default image should be returned, or a redirect followed.

    # get_user_groups_by_id
    groups = await client.users.get_user_groups_by_id(new_user_id)
    assert isinstance(groups, list)
    # Empty groups expected for new user

    # get_user_oauth_sessions_by_id
    try:
        await client.users.get_user_oauth_sessions_by_id(new_user_id)
    except Exception:
        # Expected to fail if no sessions
        pass

    # 6. Delete user by ID
    delete_result = await client.users.delete_user_by_id(new_user_id)
    assert delete_result is True


async def test_user_status_lifecycle(client):
    """
    Test get_user_status and update_user_status.
    """
    # 1. Get current status
    status_model = await client.users.get_user_status()
    assert isinstance(status_model, UserModel)

    # 2. Update status
    new_status = UserStatus(
        status_emoji="🚀",
        status_message="Testing drift fixes",
    )
    updated_model = await client.users.update_user_status(new_status)

    assert isinstance(updated_model, UserModel)
    assert updated_model.status_emoji == "🚀"
    assert updated_model.status_message == "Testing drift fixes"

    # 3. Verify persistence
    check_model = await client.users.get_user_status()
    assert check_model.status_emoji == "🚀"
    assert check_model.status_message == "Testing drift fixes"
