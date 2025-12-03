import pytest
from owui_client.models.channels import CreateChannelForm, ChannelForm
from owui_client.models.messages import MessageForm

@pytest.mark.asyncio
async def test_channels_crud(client):
    # Create a channel
    create_form = CreateChannelForm(
        name="test-channel",
        description="A test channel",
        is_private=False,
        type="group" # type is required for creation
    )
    
    channel = await client.channels.create(create_form)
    assert channel is not None
    assert channel.name == "test-channel"
    assert channel.description == "A test channel"
    assert channel.type == "group"

    # List channels
    channels = await client.channels.list()
    assert len(channels) > 0
    found = False
    for c in channels:
        if c.id == channel.id:
            found = True
            break
    assert found

    # Get channel details
    channel_full = await client.channels.get(channel.id)
    assert channel_full is not None
    assert channel_full.id == channel.id
    
    # Update channel
    update_form = ChannelForm(
        name="test-channel-updated",
        description="Updated description"
    )
    updated_channel = await client.channels.update(channel.id, update_form)
    assert updated_channel.name == "test-channel-updated"
    assert updated_channel.description == "Updated description"

    # Post a message
    message_form = MessageForm(
        content="Hello world!"
    )
    message = await client.channels.post_message(channel.id, message_form)
    assert message is not None
    assert message.content == "Hello world!"
    assert message.channel_id == channel.id

    # Get messages
    messages = await client.channels.get_messages(channel.id)
    assert len(messages) > 0
    assert messages[0].content == "Hello world!"

    # Add reaction
    reaction = await client.channels.add_reaction(channel.id, message.id, "👍")
    assert reaction is True

    # Pin message to verify reactions (as pinned messages return reactions)
    pinned_res = await client.channels.pin_message(channel.id, message.id, True)
    assert pinned_res.is_pinned is True

    # Get pinned messages
    pinned_messages = await client.channels.get_pinned_messages(channel.id)
    assert len(pinned_messages) > 0
    target_msg = None
    for msg in pinned_messages:
        if msg.id == message.id:
            target_msg = msg
            break
    assert target_msg is not None
    
    # Check reaction on pinned message
    has_reaction = False
    for r in target_msg.reactions:
        if r.name == "👍":
            has_reaction = True
            break
    assert has_reaction

    # Remove reaction
    remove_res = await client.channels.remove_reaction(channel.id, message.id, "👍")
    assert remove_res is True

    # Delete message
    delete_msg_res = await client.channels.delete_message(channel.id, message.id)
    assert delete_msg_res is True

    # Delete channel
    delete_res = await client.channels.delete(channel.id)
    assert delete_res is True
