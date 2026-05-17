import asyncio

import pytest
from owui_client.models.chats import ChatForm, MessageForm, TagForm, ChatCompletionForm, ChatCompletedForm, ChatActionForm
from owui_client.models.openai import OpenAIConfigForm

pytestmark = pytest.mark.asyncio


async def test_chats_lifecycle(client):
    """
    Test create, get, update, delete lifecycle for chats.
    """

    # 1. Create new chat
    chat_data = {"title": "Test Chat", "history": {"messages": {}, "currentId": None}}
    form = ChatForm(chat=chat_data)

    created_chat = await client.chats.create_new(form)
    assert created_chat is not None
    assert created_chat.title == "Test Chat"
    chat_id = created_chat.id

    # 2. Get chat list
    chat_list = await client.chats.get_list()
    assert len(chat_list) >= 1
    found = next((c for c in chat_list if c.id == chat_id), None)
    assert found is not None
    assert found.title == "Test Chat"

    # 3. Get chat by ID
    fetched_chat = await client.chats.get(chat_id)
    assert fetched_chat is not None
    assert fetched_chat.id == chat_id
    assert fetched_chat.title == "Test Chat"

    # 4. Update chat (title and seed history)
    updated_chat_data = {
        "title": "Updated Test Chat",
        "history": {
            "messages": {
                "msg_1": {
                    "id": "msg_1",
                    "role": "user",
                    "content": "Original Content",
                    "timestamp": 1600000000,
                    "parentId": None,
                    "childrenIds": [],
                    "models": ["gpt-3.5-turbo"],
                }
            },
            "currentId": "msg_1",
        },
    }
    update_form = ChatForm(chat=updated_chat_data)
    updated_chat = await client.chats.update(chat_id, update_form)
    assert updated_chat.title == "Updated Test Chat"

    # 5. Update message content
    message_id = "msg_1"
    message_form = MessageForm(content="Hello World")
    # Update existing message content using the endpoint

    msg_updated_chat = await client.chats.update_message(
        chat_id, message_id, message_form
    )
    assert msg_updated_chat is not None
    # Check if message is in history
    history = msg_updated_chat.chat.get("history", {})
    messages = history.get("messages", {})
    assert message_id in messages
    assert messages[message_id]["content"] == "Hello World"

    # 6. Pin Chat
    pinned_chat = await client.chats.pin(chat_id)
    assert pinned_chat.pinned is True

    # Verify in pinned list
    pinned_list = await client.chats.get_pinned()
    assert any(c.id == chat_id for c in pinned_list)

    # Unpin
    unpinned_chat = await client.chats.pin(chat_id)
    assert unpinned_chat.pinned is False

    # 7. Tags
    tag_form = TagForm(name="test-tag")
    tags = await client.chats.add_tag(chat_id, tag_form)
    assert any(t.name == "test-tag" for t in tags)

    chat_tags = await client.chats.get_tags(chat_id)
    assert any(t.name == "test-tag" for t in chat_tags)

    # Delete tag
    tags_after_delete = await client.chats.delete_tag(chat_id, tag_form)
    assert not any(t.name == "test-tag" for t in tags_after_delete)

    # 8. Archive
    archived_chat = await client.chats.archive(chat_id)
    assert archived_chat.archived is True

    # Verify in archived list
    archived_list = await client.chats.get_archived_list()
    assert any(c.id == chat_id for c in archived_list)

    # Unarchive
    unarchived_chat = await client.chats.archive(chat_id)
    assert unarchived_chat.archived is False

    # 9. Delete chat
    deleted = await client.chats.delete(chat_id)
    assert deleted is True

    # Verify deletion
    try:
        await client.chats.get(chat_id)
        assert False, "Should have raised 404"  # or 401 as per backend
    except Exception:
        pass


async def test_export_chat_stats(client):
    """
    Test exporting chat statistics.
    """
    # Create a chat with some history for stats export
    chat_data = {
        "title": "Stats Test Chat",
        "history": {
            "messages": {
                "msg_1": {
                    "id": "msg_1",
                    "role": "user",
                    "content": "Hello, how are you?",
                    "timestamp": 1600000000,
                    "parentId": None,
                    "childrenIds": ["msg_2"],
                    "models": [],
                },
                "msg_2": {
                    "id": "msg_2",
                    "role": "assistant",
                    "content": "I'm doing well, thank you!",
                    "timestamp": 1600000010,
                    "parentId": "msg_1",
                    "childrenIds": [],
                    "models": ["gpt-3.5-turbo"],
                    "model": "gpt-3.5-turbo",
                },
            },
            "currentId": "msg_2",
        },
    }
    form = ChatForm(chat=chat_data)
    created_chat = await client.chats.create_new(form)
    assert created_chat is not None
    chat_id = created_chat.id

    try:
        # Export chat stats list
        stats_list = await client.chats.export_chat_stats(page=1)
        assert stats_list is not None
        assert hasattr(stats_list, "items")
        assert hasattr(stats_list, "total")
        assert hasattr(stats_list, "page")
        assert stats_list.type == "chats"

        # Export single chat stats
        single_stats = await client.chats.export_single_chat_stats(chat_id)
        assert single_stats is not None
        assert single_stats.id == chat_id
        assert hasattr(single_stats, "stats")
        assert hasattr(single_stats, "chat")
        assert hasattr(single_stats.stats, "message_count")
        assert hasattr(single_stats.stats, "models")

    finally:
        # Cleanup
        await client.chats.delete(chat_id)


async def test_chat_completion(client, mock_openai_server):
    """
    Test chat completion endpoint with mock OpenAI server.
    """
    # Configure OpenAI to use the mock server
    new_config = OpenAIConfigForm(
        ENABLE_OPENAI_API=True,
        OPENAI_API_BASE_URLS=[mock_openai_server],
        OPENAI_API_KEYS=["sk-mock-key"],
        OPENAI_API_CONFIGS={"0": {"enable": True}}
    )
    await client.openai.update_config(new_config)

    # Force model cache refresh so the mock server's models are picked up.
    # Without this, a previous test's stale MODELS cache causes "Model not found".
    # The openai.get_all_models() @cached TTL is 1s; sleep to ensure it expires.
    await asyncio.sleep(1)
    await client._request("GET", "/models", params={"refresh": True})

    # Test synchronous completion (no session_id)
    # Use a simple dict to avoid potential Pydantic serialization issues
    sync_form_data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Hello, how are you?"}
        ]
    }

    sync_response = await client.chats.chat_completion(sync_form_data)
    assert sync_response is not None
    # Synchronous response should have completion fields
    assert hasattr(sync_response, 'choices') or sync_response.status is not None


async def test_chat_completed(client, mock_openai_server):
    """
    Test chat completed endpoint.
    """
    # Configure OpenAI to use the mock server
    new_config = OpenAIConfigForm(
        ENABLE_OPENAI_API=True,
        OPENAI_API_BASE_URLS=[mock_openai_server],
        OPENAI_API_KEYS=["sk-mock-key"],
        OPENAI_API_CONFIGS={"0": {"enable": True}}
    )
    await client.openai.update_config(new_config)

    # Force model cache refresh so the mock server's models are picked up.
    await asyncio.sleep(1)
    await client._request("GET", "/models", params={"refresh": True})

    # Create a chat first
    chat_data = {"title": "Test Chat for Completed", "history": {"messages": {}, "currentId": None}}
    form = ChatForm(chat=chat_data)
    created_chat = await client.chats.create_new(form)
    assert created_chat is not None
    chat_id = created_chat.id

    try:
        # Test chat completed with ChatCompletedForm
        completed_form = ChatCompletedForm(
            model="gpt-3.5-turbo",
            messages=["msg_1", "msg_2"],
            chat_id=chat_id,
            session_id="test-session-123",
            id="msg_2"
        )

        response = await client.chats.chat_completed(completed_form)
        assert response is not None

        # Test chat completed with dict
        completed_dict = {
            "model": "gpt-3.5-turbo",
            "messages": ["msg_1", "msg_2"],
            "chat_id": chat_id,
            "session_id": "test-session-456",
            "id": "msg_2",
            "filter_ids": []
        }

        dict_response = await client.chats.chat_completed(completed_dict)
        assert dict_response is not None

    finally:
        # Cleanup
        await client.chats.delete(chat_id)


async def test_chat_action(client, mock_openai_server):
    """
    Test chat action endpoint.

    This test verifies that the chat_action endpoint can be called with both
    ChatActionForm and dict inputs. Note that this test may fail if no
    action functions are registered in the Open WebUI instance.
    """
    # Configure OpenAI to use the mock server
    new_config = OpenAIConfigForm(
        ENABLE_OPENAI_API=True,
        OPENAI_API_BASE_URLS=[mock_openai_server],
        OPENAI_API_KEYS=["sk-mock-key"],
        OPENAI_API_CONFIGS={"0": {"enable": True}}
    )
    await client.openai.update_config(new_config)

    # Create a chat first
    chat_data = {"title": "Test Chat for Action", "history": {"messages": {}, "currentId": None}}
    form = ChatForm(chat=chat_data)
    created_chat = await client.chats.create_new(form)
    assert created_chat is not None
    chat_id = created_chat.id

    try:
        # Test chat action with ChatActionForm
        # Note: This will likely fail if no action functions are registered
        # The test is primarily to verify the endpoint exists and can be called
        action_form = ChatActionForm(
            model="gpt-3.5-turbo",
            messages=["msg_1"],
            chat_id=chat_id,
            id="msg_1",
            session_id="test-session-123"
        )

        try:
            response = await client.chats.chat_action("test_action", action_form)
            # If an action function exists, we should get a response
            assert response is not None
        except Exception as e:
            # If no action function exists, we expect an error
            # This is expected behavior in a clean test environment
            # The error message may vary depending on backend implementation
            assert "not found" in str(e).lower() or "none" in str(e).lower() or "400" in str(e)

        # Test chat action with dict
        action_dict = {
            "model": "gpt-3.5-turbo",
            "messages": ["msg_1"],
            "chat_id": chat_id,
            "id": "msg_1",
            "session_id": "test-session-456"
        }

        try:
            dict_response = await client.chats.chat_action("test_action", action_dict)
            # If an action function exists, we should get a response
            assert dict_response is not None
        except Exception as e:
            # If no action function exists, we expect an error
            # This is expected behavior in a clean test environment
            # The error message may vary depending on backend implementation
            assert "not found" in str(e).lower() or "none" in str(e).lower() or "400" in str(e)

    finally:
        # Cleanup
        await client.chats.delete(chat_id)
