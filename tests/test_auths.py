import pytest
from httpx import HTTPStatusError
from owui_client.models.auths import (
    SigninForm,
    SignupForm,
    UpdatePasswordForm,
    AddUserForm,
    LdapServerConfig,
    LdapConfigForm,
)
from owui_client.models.users import UpdateProfileForm
import uuid

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio


async def test_01_admin_config_enable_signup(client):
    """
    Test getting and updating admin config to enable signup.
    This should run before signup tests.
    """
    # 1. Get current config
    config = await client.auths.get_admin_config()
    assert config is not None

    # 2. Enable signup if not enabled
    if not config.ENABLE_SIGNUP:
        config.ENABLE_SIGNUP = True
        updated_config = await client.auths.update_admin_config(config)
        assert updated_config.ENABLE_SIGNUP is True

    # 3. Verify it persisted
    config_check = await client.auths.get_admin_config()
    assert config_check.ENABLE_SIGNUP is True


async def test_signin_success(client):
    """
    Test signing in with valid credentials (the admin user created by the test server).
    """
    # Default credentials from owui_test_util.py
    form = SigninForm(email="admin@example.com", password="password123")

    response = await client.auths.signin(form)

    assert response is not None
    assert response.token is not None
    assert response.email == "admin@example.com"
    # Verify client updated its key
    assert client.api_key == response.token


async def test_signin_failure(client):
    """
    Test signing in with invalid credentials.
    """
    form = SigninForm(email="admin@example.com", password="wrongpassword")

    # Depending on implementation, this might raise an exception or return error response
    # OWUIClientBase usually raises exception for non-200

    with pytest.raises(HTTPStatusError):
        await client.auths.signin(form)


async def test_signup_success(client):
    """
    Test signing up a new user.
    """
    # Ensure we have a fresh client or reset key if needed, but for now we assume
    # test_signin_success might have run or test_01_admin_config ran.
    # If test_signin_success ran last, client.api_key is admin's token.
    # If test_01_admin_config ran last, client.api_key is admin_api_key (from fixture).

    # Note: The previous test (test_01_admin_config_enable_signup) ensures signup is enabled.

    new_email = f"newuser_{uuid.uuid4()}@example.com"
    new_password = "newpassword123"
    new_name = "New User"

    form = SignupForm(email=new_email, password=new_password, name=new_name)

    # We use the client, which should have admin access or at least be valid.
    response = await client.auths.signup(form)

    assert response is not None
    assert response.token is not None
    assert response.email == new_email
    assert response.name == new_name

    # Verify client updated its key to the new user's token
    assert client.api_key == response.token

    # Verify we can sign in with the new user
    signin_form = SigninForm(email=new_email, password=new_password)
    signin_response = await client.auths.signin(signin_form)
    assert signin_response.token is not None
    assert signin_response.email == new_email


async def test_signout_success(client):
    """
    Test signing out.
    """
    # 1. Ensure we are signed in first (e.g. as admin)
    form = SigninForm(email="admin@example.com", password="password123")
    signin_response = await client.auths.signin(form)
    assert client.api_key == signin_response.token

    # 2. Sign out
    response = await client.auths.sign_out()

    # 3. Verify response and side effects
    assert response.status is True
    assert client.api_key is None


async def test_get_session_user(client):
    """
    Test getting the current session user.
    """
    # Ensure signed in
    form = SigninForm(email="admin@example.com", password="password123")
    await client.auths.signin(form)

    user = await client.auths.get_session_user()
    assert user is not None
    assert user.email == "admin@example.com"
    assert user.id is not None


async def test_update_profile(client):
    """
    Test updating the user profile.
    """
    # Ensure signed in
    form = SigninForm(email="admin@example.com", password="password123")
    await client.auths.signin(form)

    # Retrieve current name to revert later if needed, or just check change
    original_user = await client.auths.get_session_user()
    original_name = original_user.name

    new_name = "Admin Updated"
    profile_form = UpdateProfileForm(name=new_name, profile_image_url="/user.png")

    user = await client.auths.update_profile(profile_form)
    assert user.name == new_name

    # Verify change persists
    session_user = await client.auths.get_session_user()
    assert session_user.name == new_name

    # Revert name
    revert_form = UpdateProfileForm(name=original_name, profile_image_url="/user.png")
    await client.auths.update_profile(revert_form)


async def test_update_password(client):
    """
    Test updating the user password.
    """
    # Ensure signed in
    email = "admin@example.com"
    old_password = "password123"
    new_password = "newpassword123"

    form = SigninForm(email=email, password=old_password)
    await client.auths.signin(form)

    password_form = UpdatePasswordForm(password=old_password, new_password=new_password)

    success = await client.auths.update_password(password_form)
    assert success is True

    # Verify old password fails
    with pytest.raises(HTTPStatusError):
        await client.auths.signin(SigninForm(email=email, password=old_password))

    # Verify new password works
    response = await client.auths.signin(SigninForm(email=email, password=new_password))
    assert response.token is not None

    # Revert password
    reset_form = UpdatePasswordForm(password=new_password, new_password=old_password)
    await client.auths.update_password(reset_form)


async def test_add_user_success(client):
    """
    Test adding a new user as admin.
    """
    # 1. Ensure signed in as admin
    form = SigninForm(email="admin@example.com", password="password123")
    await client.auths.signin(form)

    # 2. Create user details
    new_email = f"added_user_{uuid.uuid4()}@example.com"
    new_password = "addedpassword123"
    new_name = "Added User"
    role = "user"

    form_data = AddUserForm(
        email=new_email,
        password=new_password,
        name=new_name,
        role=role
    )

    # 3. Add user
    response = await client.auths.add_user(form_data)

    assert response is not None
    assert response.email == new_email
    assert response.role == role
    # Note: The response contains a token for the NEW user, but the client's key should probably remain as Admin if we are just adding a user?
    # The backend implementation of `add_user` returns a `SigninResponse` (including token).
    # The client method `add_user` does NOT update `self._client.api_key` automatically (unlike signin/signup),
    # which is correct because the admin is performing the action, not the new user signing in.

    # 4. Verify we can sign in as the new user
    # Temporarily switch client key? Or just try signin which will overwrite it.
    
    signin_form = SigninForm(email=new_email, password=new_password)
    signin_response = await client.auths.signin(signin_form)
    assert signin_response.token is not None
    assert signin_response.email == new_email


async def test_get_admin_details(client):
    """
    Test getting admin details.
    """
    # 1. Ensure signed in as admin
    form = SigninForm(email="admin@example.com", password="password123")
    await client.auths.signin(form)

    # 2. Ensure SHOW_ADMIN_DETAILS is enabled
    config = await client.auths.get_admin_config()
    if not config.SHOW_ADMIN_DETAILS:
        config.SHOW_ADMIN_DETAILS = True
        await client.auths.update_admin_config(config)

    # 3. Get admin details
    details = await client.auths.get_admin_details()
    assert details is not None
    assert details.email is not None
    # The default admin created by the test fixture might vary, but usually admin@example.com
    assert details.email == "admin@example.com"


async def test_ldap_server_config(client):
    """
    Test getting and updating LDAP server configuration.
    """
    # 1. Ensure signed in as admin
    form = SigninForm(email="admin@example.com", password="password123")
    await client.auths.signin(form)

    # 2. Get current LDAP server config
    server_config = await client.auths.get_ldap_server()
    assert server_config is not None
    
    # 3. Update LDAP server config
    original_label = server_config.label
    new_label = "Test LDAP Server"
    server_config.label = new_label

    # Ensure required fields are populated for the update to succeed
    # Backend requires: label, host, attribute_for_mail, attribute_for_username, app_dn, app_dn_password, search_base
    if not server_config.host:
        server_config.host = "ldap.example.com"
    if not server_config.app_dn:
        server_config.app_dn = "cn=admin,dc=example,dc=com"
    if not server_config.app_dn_password:
        server_config.app_dn_password = "password"
    if not server_config.search_base:
        server_config.search_base = "dc=example,dc=com"
    
    updated_config = await client.auths.update_ldap_server(server_config)
    assert updated_config.label == new_label

    # 4. Verify persistence
    server_config_check = await client.auths.get_ldap_server()
    assert server_config_check.label == new_label

    # 5. Revert (optional, but good practice)
    server_config.label = original_label
    await client.auths.update_ldap_server(server_config)


async def test_ldap_config(client):
    """
    Test getting and updating LDAP general configuration (enable/disable).
    """
    # 1. Ensure signed in as admin
    form = SigninForm(email="admin@example.com", password="password123")
    await client.auths.signin(form)

    # 2. Get current LDAP config
    ldap_config = await client.auths.get_ldap_config()
    assert ldap_config is not None
    
    # 3. Toggle ENABLE_LDAP
    new_state = not ldap_config.ENABLE_LDAP
    
    form_data = LdapConfigForm(enable_ldap=new_state)
    updated_config = await client.auths.update_ldap_config(form_data)
    
    assert updated_config.ENABLE_LDAP == new_state
    
    # 4. Verify persistence
    config_check = await client.auths.get_ldap_config()
    assert config_check.ENABLE_LDAP == new_state
    
    # 5. Revert
    await client.auths.update_ldap_config(LdapConfigForm(enable_ldap=not new_state))


async def test_api_key_lifecycle(client):
    """
    Test generating, retrieving, and deleting an API key.
    """
    # 1. Ensure signed in as admin
    form = SigninForm(email="admin@example.com", password="password123")
    await client.auths.signin(form)

    # 2. Ensure API keys are enabled
    config = await client.auths.get_admin_config()
    if not config.ENABLE_API_KEYS:
        config.ENABLE_API_KEYS = True
        await client.auths.update_admin_config(config)

    # 3. Generate API key
    key_response = await client.auths.generate_api_key()
    assert key_response is not None
    assert key_response.api_key is not None
    new_key = key_response.api_key

    # 4. Get API key
    get_response = await client.auths.get_api_key()
    assert get_response.api_key == new_key

    # 5. Delete API key
    success = await client.auths.delete_api_key()
    assert success is True

    # 6. Verify it's gone (should 404)
    with pytest.raises(HTTPStatusError) as excinfo:
        await client.auths.get_api_key()
    assert excinfo.value.response.status_code == 404
