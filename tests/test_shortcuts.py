from owui_client.shortcuts import Shortcuts

async def test_shortcuts_initialization(client):
    """
    Test that the shortcuts layer is correctly initialized on the client.
    """
    assert hasattr(client, "shortcuts")
    assert isinstance(client.shortcuts, Shortcuts)
    # Ensure the shortcuts instance has a reference back to the client
    assert client.shortcuts.client == client



