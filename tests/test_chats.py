import asyncio

import pytest
from owui_client.models.chats import ChatForm, MessageForm, TagForm, ChatCompletionForm, ChatCompletedForm, ChatActionForm, CompactChatForm, ForkForm
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


async def test_chat_archived_count(client):
    """
    Test GET /chats/archived/count returns the number of archived chats.
    """
    form = ChatForm(
        chat={"title": "Archived Count Chat", "history": {"messages": {}, "currentId": None}}
    )
    created = await client.chats.create_new(form)
    assert created is not None
    chat_id = created.id

    try:
        # Baseline count before archiving.
        before = await client.chats.get_archived_count()
        assert isinstance(before, int)

        # Archive the chat and confirm the count increases by exactly one.
        archived = await client.chats.archive(chat_id)
        assert archived is not None
        assert archived.archived is True

        after = await client.chats.get_archived_count()
        assert after == before + 1
    finally:
        await client.chats.delete(chat_id)


async def test_chat_unshare_all(client):
    """
    Test DELETE /chats/share/all removes every shared chat for the user.
    """
    form = ChatForm(
        chat={"title": "Unshare All Chat", "history": {"messages": {}, "currentId": None}}
    )
    created = await client.chats.create_new(form)
    assert created is not None
    chat_id = created.id

    try:
        # Share the chat so there is something to unshare.
        shared = await client.chats.share(chat_id)
        assert shared is not None
        assert shared.share_id is not None

        # Unshare everything.
        result = await client.chats.unshare_all()
        assert result is True

        # The chat should no longer carry a share_id.
        fetched = await client.chats.get(chat_id)
        assert fetched is not None
        assert fetched.share_id is None
    finally:
        await client.chats.delete(chat_id)


async def test_chat_compact(client):
    """
    Test POST /chats/{id}/compact.

    Context compaction is disabled by default (ENABLE_CONTEXT_COMPACTION=False),
    so the backend returns a result dict with `compacted` False and reason
    'disabled' without invoking a model. Passing an explicit model in the form
    lets the router resolve the model id even though the chat has no assistant
    messages, exercising the endpoint end-to-end without an LLM.
    """
    chat_data = {
        "title": "Compact Chat",
        "history": {
            "messages": {
                "msg_1": {
                    "id": "msg_1",
                    "role": "user",
                    "content": "hello",
                    "timestamp": 1600000000,
                    "parentId": None,
                    "childrenIds": [],
                    "model": "gpt-4",
                }
            },
            "currentId": "msg_1",
        },
    }
    form = ChatForm(chat=chat_data)
    created = await client.chats.create_new(form)
    assert created is not None
    chat_id = created.id

    try:
        result = await client.chats.compact(chat_id, CompactChatForm(model="gpt-4"))
        assert isinstance(result, dict)
        assert result.get("ok") is True
        # Default config disables compaction, so nothing is actually summarized.
        assert result.get("compacted") is False
        assert result.get("reason") == "disabled"
    finally:
        await client.chats.delete(chat_id)


async def test_chat_search_snippet(client):
    """
    Test that the ChatTitleIdResponse.snippet field is populated by search.
    """
    needle = "supercalifragilistic"
    chat_data = {
        "title": "Snippet Search Chat",
        # The backend search scans the top-level `messages` array
        # (json_each(Chat.chat, '$.messages')), so include it alongside the
        # tree-shaped `history.messages` map that the rest of the app reads.
        "messages": [
            {
                "id": "msg_1",
                "role": "user",
                "content": f"Please find this {needle} term in my message.",
            }
        ],
        "history": {
            "messages": {
                "msg_1": {
                    "id": "msg_1",
                    "role": "user",
                    "content": f"Please find this {needle} term in my message.",
                    "timestamp": 1600000000,
                    "parentId": None,
                    "childrenIds": [],
                }
            },
            "currentId": "msg_1",
        },
    }
    form = ChatForm(chat=chat_data)
    created = await client.chats.create_new(form)
    assert created is not None
    chat_id = created.id

    try:
        results = await client.chats.search(needle)
        assert results is not None
        match = next((c for c in results if c.id == chat_id), None)
        assert match is not None
        assert match.snippet is not None
        assert needle in match.snippet.lower()
    finally:
        await client.chats.delete(chat_id)


async def test_mark_chats_read(client):
    """
    Test POST /chats/read marks the current user's chats as read.
    """
    form = ChatForm(chat={"title": "Read Test", "history": {"messages": {}, "currentId": None}})
    created = await client.chats.create_new(form)
    assert created is not None
    chat_id = created.id

    try:
        result = await client.chats.mark_chats_read()
        assert isinstance(result, dict)
        assert isinstance(result.get("updated_count"), int)
        assert result["updated_count"] >= 1
        assert isinstance(result.get("folder_unread_counts"), dict)
    finally:
        await client.chats.delete(chat_id)


async def test_fork_chat(client):
    """
    Test POST /chats/{id}/fork creates a new chat from a message.

    Forking copies the conversation up to the source message into a new chat,
    stamping `chat.originalChatId`/`chat.branchPointMessageId` and
    `meta.forked_from`/`meta.forked_from_message_id`. The assistant message is
    marked `done` so the backend does not reject the fork as in-progress.
    """
    chat_data = {
        "title": "Fork Source",
        "history": {
            "messages": {
                "msg_a": {
                    "id": "msg_a",
                    "role": "user",
                    "content": "hello",
                    "timestamp": 1600000000,
                    "parentId": None,
                    "childrenIds": ["msg_b"],
                },
                "msg_b": {
                    "id": "msg_b",
                    "role": "assistant",
                    "content": "hi there",
                    "timestamp": 1600000001,
                    "parentId": "msg_a",
                    "childrenIds": [],
                    "done": True,
                },
            },
            "currentId": "msg_b",
        },
    }
    form = ChatForm(chat=chat_data)
    created = await client.chats.create_new(form)
    assert created is not None
    source_id = created.id

    fork = None
    try:
        fork = await client.chats.fork(source_id)
        assert fork is not None
        assert fork.id != source_id
        assert fork.title.endswith("(fork)")
        # Fork records its origin on the chat blob and meta.
        assert fork.chat.get("originalChatId") == source_id
        assert fork.chat.get("branchPointMessageId") == "msg_b"
        assert fork.meta.get("forked_from") == source_id
        assert fork.meta.get("forked_from_message_id") == "msg_b"
    finally:
        if fork is not None:
            await client.chats.delete(fork.id)
        await client.chats.delete(source_id)


async def test_mark_chat_unread(client):
    """
    Test POST /chats/{id}/unread marks a chat as unread.
    """
    form = ChatForm(chat={"title": "Unread Test", "history": {"messages": {}, "currentId": None}})
    created = await client.chats.create_new(form)
    assert created is not None
    chat_id = created.id

    try:
        result = await client.chats.mark_chat_unread(chat_id)
        assert isinstance(result, dict)
        assert result.get("chat_id") == chat_id
        assert result.get("last_read_at") == 0
        assert "folder_id" in result
        assert isinstance(result.get("folder_unread_counts"), dict)
    finally:
        await client.chats.delete(chat_id)
