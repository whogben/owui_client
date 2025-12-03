import pytest
from owui_client.models.chats import ChatForm, MessageForm, TagForm

pytestmark = pytest.mark.asyncio

async def test_chats_lifecycle(client):
    """
    Test create, get, update, delete lifecycle for chats.
    """
    
    # 1. Create new chat
    chat_data = {
        "title": "Test Chat",
        "history": {
            "messages": {},
            "currentId": None
        }
    }
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
    
    # 4. Update chat (title)
    updated_chat_data = {
        "title": "Updated Test Chat",
        "history": {
            "messages": {},
            "currentId": None
        }
    }
    update_form = ChatForm(chat=updated_chat_data)
    updated_chat = await client.chats.update(chat_id, update_form)
    assert updated_chat.title == "Updated Test Chat"
    
    # 5. Add message
    message_id = "msg_1"
    message_form = MessageForm(content="Hello World")
    # We need to use a specific API or update the chat history manually via update() 
    # but there is update_message endpoint: POST /{id}/messages/{message_id}
    
    # The backend upsert_message_to_chat_by_id_and_message_id expects a dict, 
    # but the router takes MessageForm with content.
    # Wait, update_message endpoint only takes content in MessageForm. 
    # It creates a message dict internally? 
    # Router: 
    # chat = Chats.upsert_message_to_chat_by_id_and_message_id(
    #    id, message_id, {"content": form_data.content}
    # )
    # So it only updates content. The message structure might need to exist or it creates a partial one.
    
    msg_updated_chat = await client.chats.update_message(chat_id, message_id, message_form)
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
        assert False, "Should have raised 404" # or 401 as per backend
    except Exception:
        pass

