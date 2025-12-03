import pytest
from owui_client.client import OpenWebUI
from owui_client.models.configs import (
    ConnectionsConfigForm,
    OAuthClientRegistrationForm,
    ToolServersConfigForm,
    ToolServerConnection,
    CodeInterpreterConfigForm,
    ModelsConfigForm,
    PromptSuggestion,
    SetDefaultSuggestionsForm,
    BannerModel,
    SetBannersForm
)

@pytest.mark.asyncio
async def test_configs_client_initialization(client: OpenWebUI):
    assert client.configs is not None

@pytest.mark.asyncio
async def test_export_import_config(client: OpenWebUI):
    # 1. Export original config
    original_config = await client.configs.export_config()
    assert isinstance(original_config, dict)

    # 2. Modify a safe setting to verify import works
    # We use a copy to ensure we don't mutate the original_config dict locally
    new_config = original_config.copy()

    # Try to toggle ENABLE_SIGNUP if present, or another safe boolean
    target_key = "ENABLE_SIGNUP"

    if target_key in new_config:
        # Toggle the value
        new_config[target_key] = not new_config[target_key]

        try:
            # Import the modified config
            updated_config = await client.configs.import_config(new_config)

            # Verify the change was applied
            assert updated_config[target_key] == new_config[target_key]

        finally:
            # 3. Restore original config
            await client.configs.import_config(original_config)

            # Verify restoration
            final_config = await client.configs.export_config()
            assert final_config[target_key] == original_config[target_key]
    else:
        # If the key isn't there, just verify we can import the original config back
        # This still tests the endpoint connectivity and payload structure
        updated_config = await client.configs.import_config(original_config)
        assert isinstance(updated_config, dict)

@pytest.mark.asyncio
async def test_connections_config(client: OpenWebUI):
    # 1. Get original config
    original_config = await client.configs.get_connections_config()
    assert isinstance(original_config, ConnectionsConfigForm)

    # 2. Toggle a setting
    new_config_data = original_config.model_copy()
    new_config_data.ENABLE_DIRECT_CONNECTIONS = (
        not new_config_data.ENABLE_DIRECT_CONNECTIONS
    )

    try:
        # 3. Set new config
        updated_config = await client.configs.set_connections_config(new_config_data)
        assert (
            updated_config.ENABLE_DIRECT_CONNECTIONS
            == new_config_data.ENABLE_DIRECT_CONNECTIONS
        )

        # Verify it persisted
        fetched_config = await client.configs.get_connections_config()
        assert (
            fetched_config.ENABLE_DIRECT_CONNECTIONS
            == new_config_data.ENABLE_DIRECT_CONNECTIONS
        )

    finally:
        # 4. Restore original config
        await client.configs.set_connections_config(original_config)

        # Verify restoration
        final_config = await client.configs.get_connections_config()
        assert (
            final_config.ENABLE_DIRECT_CONNECTIONS
            == original_config.ENABLE_DIRECT_CONNECTIONS
        )

@pytest.mark.asyncio
async def test_register_oauth_client(client: OpenWebUI):
    # Note: This test relies on the backend being able to contact the URL provided.
    # Using a dummy URL might fail if the backend validates connectivity immediately.
    # However, based on the code, it seems to fetch metadata.
    # We will use a known public OIDC discovery endpoint if possible, or mock it if we were mocking.
    # Since we are running against a real backend container, let's try a safe failing test or a mock one.
    #
    # If we use a non-existent URL, it should fail with HTTPException(400).
    # Let's test the failure case to verify the endpoint is reachable and validates input.

    form_data = OAuthClientRegistrationForm(
        url="http://non-existent-url.test/well-known/openid-configuration",
        client_id="test-client-id",
        client_name="Test Client",
    )

    # We expect this to raise an error because the URL is invalid/unreachable
    # but it confirms the client call reaches the correct endpoint.
    with pytest.raises(Exception) as excinfo:
        await client.configs.register_oauth_client(form_data)

    # Verify it's an API error (likely 400 or connection error wrapped)
    # The exact error message depends on how the client handles HTTP errors,
    # but catching any exception confirms the code path was executed.
    assert (
        "400" in str(excinfo.value)
        or "Failed to register" in str(excinfo.value)
        or "Connection" in str(excinfo.value)
    )

@pytest.mark.asyncio
async def test_tool_servers_config(client: OpenWebUI):
    # 1. Get original config
    original_config = await client.configs.get_tool_servers_config()
    assert isinstance(original_config, ToolServersConfigForm)

    # 2. Add a dummy tool server
    new_connection = ToolServerConnection(
        url="http://dummy-tool-server.test",
        path="/",
        type="openapi",
        auth_type="none",
        config={
            "enable": False
        },  # Provide config to avoid backend AttributeError (None.get)
    )

    new_config_data = ToolServersConfigForm(
        TOOL_SERVER_CONNECTIONS=original_config.TOOL_SERVER_CONNECTIONS
        + [new_connection]
    )

    try:
        # 3. Set new config
        updated_config = await client.configs.set_tool_servers_config(new_config_data)

        # Verify the new connection is in the list
        # We check if any connection matches our dummy URL
        match = any(
            c.url == new_connection.url for c in updated_config.TOOL_SERVER_CONNECTIONS
        )
        assert match

        # 4. Verify endpoint
        # Since it's a dummy URL, verification should fail (raise exception or return error status)
        with pytest.raises(Exception) as excinfo:
            await client.configs.verify_tool_servers_config(new_connection)

        # Verify it's an API error (likely 400 or connection error wrapped)
        assert "400" in str(excinfo.value) or "Failed to connect" in str(excinfo.value)

    finally:
        # 5. Restore original config
        await client.configs.set_tool_servers_config(original_config)

        # Verify restoration
        final_config = await client.configs.get_tool_servers_config()
        assert len(final_config.TOOL_SERVER_CONNECTIONS) == len(
            original_config.TOOL_SERVER_CONNECTIONS
        )

@pytest.mark.asyncio
async def test_code_execution_config(client: OpenWebUI):
    # 1. Get original config
    original_config = await client.configs.get_code_execution_config()
    assert isinstance(original_config, CodeInterpreterConfigForm)

    # 2. Toggle a setting
    new_config_data = original_config.model_copy()
    # Toggle a safe setting like ENABLE_CODE_EXECUTION
    new_config_data.ENABLE_CODE_EXECUTION = not new_config_data.ENABLE_CODE_EXECUTION

    try:
        # 3. Set new config
        updated_config = await client.configs.set_code_execution_config(new_config_data)
        assert (
            updated_config.ENABLE_CODE_EXECUTION
            == new_config_data.ENABLE_CODE_EXECUTION
        )

        # Verify it persisted
        fetched_config = await client.configs.get_code_execution_config()
        assert (
            fetched_config.ENABLE_CODE_EXECUTION
            == new_config_data.ENABLE_CODE_EXECUTION
        )

    finally:
        # 4. Restore original config
        await client.configs.set_code_execution_config(original_config)

        # Verify restoration
        final_config = await client.configs.get_code_execution_config()
        assert (
            final_config.ENABLE_CODE_EXECUTION == original_config.ENABLE_CODE_EXECUTION
        )

@pytest.mark.asyncio
async def test_models_config(client: OpenWebUI):
    # 1. Get original config
    original_config = await client.configs.get_models_config()
    assert isinstance(original_config, ModelsConfigForm)
    
    # 2. Modify a setting
    new_config_data = original_config.model_copy()
    # Use a dummy model name to test setting the default model
    dummy_model = "test-model"
    new_config_data.DEFAULT_MODELS = dummy_model
    
    try:
        # 3. Set new config
        updated_config = await client.configs.set_models_config(new_config_data)
        assert updated_config.DEFAULT_MODELS == dummy_model
        
        # Verify it persisted
        fetched_config = await client.configs.get_models_config()
        assert fetched_config.DEFAULT_MODELS == dummy_model
        
    finally:
        # 4. Restore original config
        await client.configs.set_models_config(original_config)
        
        # Verify restoration
        final_config = await client.configs.get_models_config()
        assert final_config.DEFAULT_MODELS == original_config.DEFAULT_MODELS

@pytest.mark.asyncio
async def test_suggestions_banners_config(client: OpenWebUI):
    # Note: There is no explicit GET endpoint for suggestions, only POST (set).
    # So we cannot easily "get original" suggestions unless we export the whole config.
    # However, the POST returns the updated list.
    # Banners have both GET and POST.
    
    # --- Banners Test ---
    
    # 1. Get original banners
    original_banners = await client.configs.get_banners()
    
    # 2. Create a test banner
    test_banner = BannerModel(
        id="test-banner",
        type="info",
        title="Test Banner",
        content="This is a test banner",
        timestamp=1234567890
    )
    
    new_banners_form = SetBannersForm(banners=original_banners + [test_banner])
    
    try:
        # 3. Set banners
        updated_banners = await client.configs.set_banners(new_banners_form)
        
        # Verify test banner is present
        assert any(b.id == "test-banner" for b in updated_banners)
        
        # Verify persistence
        fetched_banners = await client.configs.get_banners()
        assert any(b.id == "test-banner" for b in fetched_banners)
        
    finally:
        # 4. Restore banners
        await client.configs.set_banners(SetBannersForm(banners=original_banners))
        
        # Verify restoration
        final_banners = await client.configs.get_banners()
        assert len(final_banners) == len(original_banners)

    # --- Suggestions Test ---
    
    # Since there is no GET for suggestions, we'll just test setting them.
    # Ideally, we should export config first to save state, but export_config 
    # might be heavy or incomplete. However, we can use export_config 
    # to get the current state if it includes suggestions.
    
    full_config = await client.configs.export_config()
    original_suggestions_data = full_config.get("DEFAULT_PROMPT_SUGGESTIONS", [])
    
    # Convert dicts back to models for restoration if needed, 
    # but the SetDefaultSuggestionsForm takes models.
    original_suggestions = [PromptSuggestion(**s) for s in original_suggestions_data]
    
    test_suggestion = PromptSuggestion(
        title=["Test"],
        content="Test suggestion content"
    )
    
    new_suggestions_form = SetDefaultSuggestionsForm(
        suggestions=original_suggestions + [test_suggestion]
    )
    
    try:
        # Set suggestions
        updated_suggestions = await client.configs.set_default_suggestions(new_suggestions_form)
        
        # Verify update
        assert any(s.content == "Test suggestion content" for s in updated_suggestions)
        
    finally:
        # Restore suggestions
        await client.configs.set_default_suggestions(
            SetDefaultSuggestionsForm(suggestions=original_suggestions)
        )
