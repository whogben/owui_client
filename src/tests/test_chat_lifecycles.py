"""
Test chat lifecycle operations using current OWUI client APIs.

This test validates the understanding of how to:
1. Start a new chat in a particular folder
2. Generate a chat completion with a particular model and tools
3. Get partial chat results over time until complete (via polling)

Based on research in plans/owui_chat_process_research.py
"""

import asyncio
import uuid
import time
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from owui_client import OpenWebUI
from owui_client.models.chats import ChatForm, ChatFolderIdForm
from owui_client.models.tasks import ActiveChatsForm


class TestChatLifecycles:
    """Test suite for chat lifecycle operations."""

    @pytest.fixture
    def client(self):
        """Create a test client instance."""
        return OpenWebUI(
            api_url="http://localhost:8080/api",
            api_key="test-api-key"
        )

    @pytest.fixture
    def sample_folder_id(self):
        """Sample folder ID for testing."""
        return "test-folder-123"

    @pytest.fixture
    def sample_model_id(self):
        """Sample model ID for testing."""
        return "llama3.1:latest"

    @pytest.fixture
    def sample_tool_ids(self):
        """Sample tool IDs for testing."""
        return ["web_search", "calculator"]

    def test_create_chat_message_graph_structure(self):
        """
        Test that we can construct the correct message graph structure
        that the backend expects for chat creation.
        
        This validates understanding of section 2 of the research:
        - Message graph with parent-child relationships
        - User message with role="user"
        - Assistant placeholder with role="assistant"
        - Proper linking via parentId and childrenIds
        """
        user_msg_id = str(uuid.uuid4())
        assistant_msg_id = str(uuid.uuid4())
        user_prompt = "What's the weather in Paris?"
        
        # Construct the message graph as expected by backend
        chat_object = {
            "id": str(uuid.uuid4()),
            "title": "New Chat",
            "models": ["llama3.1:latest"],
            "params": {
                "temperature": 0.7,
                "function_calling": "native",
            },
            "history": {
                "currentId": assistant_msg_id,
                "messages": {
                    user_msg_id: {
                        "id": user_msg_id,
                        "parentId": None,
                        "childrenIds": [assistant_msg_id],
                        "role": "user",
                        "content": user_prompt,
                        "timestamp": int(datetime.now().timestamp() * 1000),
                    },
                    assistant_msg_id: {
                        "id": assistant_msg_id,
                        "parentId": user_msg_id,
                        "childrenIds": [],
                        "role": "assistant",
                        "content": f"[RESPONSE] {assistant_msg_id}",
                        "done": True,
                        "model": "llama3.1:latest",
                        "timestamp": int(datetime.now().timestamp() * 1000),
                    }
                }
            },
            "messages": [
                {
                    "id": user_msg_id,
                    "role": "user",
                    "content": user_prompt,
                    "timestamp": int(datetime.now().timestamp() * 1000),
                },
                {
                    "id": assistant_msg_id,
                    "role": "assistant",
                    "content": f"[RESPONSE] {assistant_msg_id}",
                    "timestamp": int(datetime.now().timestamp() * 1000),
                }
            ],
            "tags": [],
            "timestamp": int(datetime.now().timestamp()),
        }
        
        # Validate structure
        assert "history" in chat_object
        assert "messages" in chat_object["history"]
        assert "currentId" in chat_object["history"]
        
        # Validate user message
        user_msg = chat_object["history"]["messages"][user_msg_id]
        assert user_msg["role"] == "user"
        assert user_msg["parentId"] is None
        assert assistant_msg_id in user_msg["childrenIds"]
        
        # Validate assistant placeholder
        assistant_msg = chat_object["history"]["messages"][assistant_msg_id]
        assert assistant_msg["role"] == "assistant"
        assert assistant_msg["parentId"] == user_msg_id
        assert assistant_msg["done"] is True

    @pytest.mark.asyncio
    async def test_create_chat_in_folder(self, client, sample_folder_id):
        """
        Task 1: Start a new chat in a particular folder.
        
        Validates:
        - Creating chat with folder_id
        - Proper message graph construction
        - Backend returns chat ID
        """
        user_msg_id = str(uuid.uuid4())
        assistant_msg_id = str(uuid.uuid4())
        chat_id = str(uuid.uuid4())
        
        chat_object = {
            "id": chat_id,
            "title": "New Chat",
            "models": ["llama3.1:latest"],
            "params": {"temperature": 0.7},
            "history": {
                "currentId": assistant_msg_id,
                "messages": {
                    user_msg_id: {
                        "id": user_msg_id,
                        "parentId": None,
                        "childrenIds": [assistant_msg_id],
                        "role": "user",
                        "content": "Test message",
                        "timestamp": int(datetime.now().timestamp() * 1000),
                    },
                    assistant_msg_id: {
                        "id": assistant_msg_id,
                        "parentId": user_msg_id,
                        "childrenIds": [],
                        "role": "assistant",
                        "content": f"[RESPONSE] {assistant_msg_id}",
                        "done": True,
                        "model": "llama3.1:latest",
                        "timestamp": int(datetime.now().timestamp() * 1000),
                    }
                }
            },
            "messages": [
                {
                    "id": user_msg_id,
                    "role": "user",
                    "content": "Test message",
                    "timestamp": int(datetime.now().timestamp() * 1000),
                },
                {
                    "id": assistant_msg_id,
                    "role": "assistant",
                    "content": f"[RESPONSE] {assistant_msg_id}",
                    "timestamp": int(datetime.now().timestamp() * 1000),
                }
            ],
            "tags": [],
            "timestamp": int(datetime.now().timestamp()),
        }
        
        # Mock the API response
        mock_response = MagicMock()
        mock_response.id = "server-generated-chat-id"
        mock_response.chat = chat_object
        
        with patch.object(client.chats, '_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response
            
            form_data = ChatForm(chat=chat_object, folder_id=sample_folder_id)
            result = await client.chats.create_new(form_data)
            
            # Verify the call was made correctly
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/v1/chats/new"
            
            # Verify payload includes folder_id
            payload = call_args[1]["json"]
            assert payload["folder_id"] == sample_folder_id
            assert "chat" in payload
            assert payload["chat"]["history"]["currentId"] == assistant_msg_id

    @pytest.mark.asyncio
    async def test_generate_completion_with_tools(
        self, client, sample_model_id, sample_tool_ids
    ):
        """
        Task 2: Generate a chat completion with a particular model and tools.
        
        Validates:
        - Constructing the completion payload with all required fields
        - Including tool_ids for tool selection
        - Setting function_calling mode for native tool use
        - Proper metadata fields (chat_id, id, parent_id)
        """
        chat_id = "test-chat-id"
        user_msg_id = "user-msg-id"
        assistant_msg_id = "assistant-msg-id"
        
        payload = {
            "model": sample_model_id,
            "model_item": {
                "id": sample_model_id,
                "name": sample_model_id,
                "direct": False,
            },
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
            ],
            "stream": True,
            "stream_options": {"include_usage": True},
            "params": {
                "temperature": 0.7,
                "function_calling": "native",
                "stream_response": True,
            },
            "tool_ids": sample_tool_ids,
            "tool_servers": [],
            "features": {
                "voice": False,
                "memory": False,
                "web_search": False,
                "image_generation": False,
                "code_interpreter": False,
            },
            "chat_id": chat_id,
            "id": assistant_msg_id,
            "parent_id": user_msg_id,
            "parent_message": {
                "id": user_msg_id,
                "role": "user",
                "content": "What is the weather?",
            },
            "variables": {
                "{{USER_NAME}}": "User",
                "{{USER_LOCATION}}": "Unknown",
            },
            "background_tasks": {
                "title_generation": True,
                "tags_generation": True,
                "follow_up_generation": True,
            },
        }
        
        # Mock the API response
        mock_response = {
            "status": True,
            "task_id": "task-123",
        }
        
        with patch.object(client.root, '_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response
            
            result = await client.root.chat_completions(payload)
            
            # Verify the call was made correctly
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/chat/completions"
            
            # Verify payload structure
            sent_payload = call_args[1]["json"]
            assert sent_payload["model"] == sample_model_id
            assert sent_payload["tool_ids"] == sample_tool_ids
            assert sent_payload["params"]["function_calling"] == "native"
            assert sent_payload["chat_id"] == chat_id
            assert sent_payload["id"] == assistant_msg_id
            assert sent_payload["parent_id"] == user_msg_id

    @pytest.mark.asyncio
    async def test_poll_for_results(self, client):
        """
        Task 3: Get partial chat results over time until complete.
        
        Validates:
        - Checking for active tasks on a chat
        - Polling until generation is complete
        - Fetching final chat state with message content
        """
        chat_id = "test-chat-id"
        
        # Mock active chats check - initially active, then complete
        active_response_1 = MagicMock()
        active_response_1.active_chat_ids = [chat_id]
        
        active_response_2 = MagicMock()
        active_response_2.active_chat_ids = []
        
        # Mock final chat with completed message
        final_chat = MagicMock()
        final_chat.chat = {
            "history": {
                "currentId": "assistant-msg-id",
                "messages": {
                    "assistant-msg-id": {
                        "id": "assistant-msg-id",
                        "role": "assistant",
                        "content": "The weather in Paris is sunny.",
                        "done": True,
                    }
                }
            }
        }
        
        call_count = [0]
        
        async def mock_check_active(form_data):
            call_count[0] += 1
            if call_count[0] == 1:
                return active_response_1
            return active_response_2
        
        with patch.object(client.tasks, 'check_active_chats', new_callable=AsyncMock) as mock_check:
            mock_check.side_effect = mock_check_active
            
            with patch.object(client.chats, 'get', new_callable=AsyncMock) as mock_get:
                mock_get.return_value = final_chat
                
                # Simulate polling
                start_time = time.time()
                timeout = 5
                result = None
                
                while time.time() - start_time < timeout:
                    active_form = ActiveChatsForm(chat_ids=[chat_id])
                    active_result = await client.tasks.check_active_chats(active_form)
                    
                    if chat_id not in (active_result.active_chat_ids or []):
                        # Generation complete, fetch final result
                        chat = await client.chats.get(chat_id)
                        if chat and chat.chat:
                            history = chat.chat.get("history", {})
                            messages = history.get("messages", {})
                            current_id = history.get("currentId")
                            
                            if current_id and current_id in messages:
                                final_message = messages[current_id]
                                result = {
                                    "status": "complete",
                                    "content": final_message.get("content", ""),
                                    "done": final_message.get("done", True),
                                }
                        break
                    
                    await asyncio.sleep(0.1)
                
                # Verify polling worked
                assert result is not None
                assert result["status"] == "complete"
                assert result["content"] == "The weather in Paris is sunny."
                assert result["done"] is True
                assert call_count[0] == 2  # Called twice (active, then complete)

    @pytest.mark.asyncio
    async def test_stop_generation(self, client):
        """
        Bonus: Stop an in-progress generation.
        
        Validates:
        - Getting task IDs for a chat
        - Stopping each active task
        """
        chat_id = "test-chat-id"
        
        # Mock tasks list
        mock_tasks = [
            {"id": "task-1"},
            {"id": "task-2"},
        ]
        
        with patch.object(client.tasks, 'list_tasks_by_chat', new_callable=AsyncMock) as mock_list:
            mock_list.return_value = mock_tasks
            
            with patch.object(client.tasks, 'stop_task', new_callable=AsyncMock) as mock_stop:
                mock_stop.return_value = True
                
                # Stop generation
                tasks = await client.tasks.list_tasks_by_chat(chat_id)
                
                for task in tasks:
                    task_id = task.get("id")
                    if task_id:
                        await client.tasks.stop_task(task_id)
                
                # Verify both tasks were stopped
                assert mock_stop.call_count == 2
                mock_stop.assert_any_call("task-1")
                mock_stop.assert_any_call("task-2")

    @pytest.mark.asyncio
    async def test_complete_chat_workflow(
        self, client, sample_folder_id, sample_model_id, sample_tool_ids
    ):
        """
        Integration test: Complete workflow from chat creation to completion.
        
        This test validates the full understanding of the chat lifecycle:
        1. Create chat in folder
        2. Trigger completion with tools
        3. Poll for results
        """
        # Step 1: Create chat
        user_msg_id = str(uuid.uuid4())
        assistant_msg_id = str(uuid.uuid4())
        chat_id = str(uuid.uuid4())
        
        chat_object = {
            "id": chat_id,
            "title": "New Chat",
            "models": [sample_model_id],
            "params": {"temperature": 0.7},
            "history": {
                "currentId": assistant_msg_id,
                "messages": {
                    user_msg_id: {
                        "id": user_msg_id,
                        "parentId": None,
                        "childrenIds": [assistant_msg_id],
                        "role": "user",
                        "content": "What's the weather in Paris?",
                        "timestamp": int(datetime.now().timestamp() * 1000),
                    },
                    assistant_msg_id: {
                        "id": assistant_msg_id,
                        "parentId": user_msg_id,
                        "childrenIds": [],
                        "role": "assistant",
                        "content": f"[RESPONSE] {assistant_msg_id}",
                        "done": True,
                        "model": sample_model_id,
                        "timestamp": int(datetime.now().timestamp() * 1000),
                    }
                }
            },
            "messages": [
                {
                    "id": user_msg_id,
                    "role": "user",
                    "content": "What's the weather in Paris?",
                    "timestamp": int(datetime.now().timestamp() * 1000),
                },
                {
                    "id": assistant_msg_id,
                    "role": "assistant",
                    "content": f"[RESPONSE] {assistant_msg_id}",
                    "timestamp": int(datetime.now().timestamp() * 1000),
                }
            ],
            "tags": [],
            "timestamp": int(datetime.now().timestamp()),
        }
        
        # Mock chat creation
        mock_chat_response = MagicMock()
        mock_chat_response.id = "server-chat-id"
        
        # Mock completion response
        mock_completion_response = {
            "status": True,
            "task_id": "task-123",
        }
        
        # Mock active tasks (complete immediately)
        mock_active_response = MagicMock()
        mock_active_response.active_chat_ids = []
        
        # Mock final chat
        mock_final_chat = MagicMock()
        mock_final_chat.chat = {
            "history": {
                "currentId": assistant_msg_id,
                "messages": {
                    assistant_msg_id: {
                        "id": assistant_msg_id,
                        "role": "assistant",
                        "content": "The weather in Paris is sunny and 22°C.",
                        "done": True,
                    }
                }
            }
        }
        
        with patch.object(client.chats, '_request', new_callable=AsyncMock) as mock_chat_request:
            mock_chat_request.return_value = mock_chat_response
            
            # Create chat
            form_data = ChatForm(chat=chat_object, folder_id=sample_folder_id)
            chat_result = await client.chats.create_new(form_data)
            actual_chat_id = chat_result.id
            
            with patch.object(client.root, '_request', new_callable=AsyncMock) as mock_completion_request:
                mock_completion_request.return_value = mock_completion_response
                
                # Trigger completion
                payload = {
                    "model": sample_model_id,
                    "model_item": {"id": sample_model_id, "name": sample_model_id, "direct": False},
                    "messages": [{"role": "system", "content": "You are helpful."}],
                    "stream": True,
                    "params": {"temperature": 0.7, "function_calling": "native"},
                    "tool_ids": sample_tool_ids,
                    "tool_servers": [],
                    "features": {"voice": False, "memory": False, "web_search": False, 
                               "image_generation": False, "code_interpreter": False},
                    "chat_id": actual_chat_id,
                    "id": assistant_msg_id,
                    "parent_id": user_msg_id,
                    "parent_message": {"id": user_msg_id, "role": "user", "content": "What's the weather?"},
                    "variables": {},
                    "background_tasks": {},
                }
                
                completion_result = await client.root.chat_completions(payload)
                
                with patch.object(client.tasks, 'check_active_chats', new_callable=AsyncMock) as mock_check:
                    mock_check.return_value = mock_active_response
                    
                    with patch.object(client.chats, 'get', new_callable=AsyncMock) as mock_get:
                        mock_get.return_value = mock_final_chat
                        
                        # Poll for results
                        active_form = ActiveChatsForm(chat_ids=[actual_chat_id])
                        active_result = await client.tasks.check_active_chats(active_form)
                        
                        if actual_chat_id not in (active_result.active_chat_ids or []):
                            chat = await client.chats.get(actual_chat_id)
                            if chat and chat.chat:
                                history = chat.chat.get("history", {})
                                messages = history.get("messages", {})
                                current_id = history.get("currentId")
                                
                                if current_id and current_id in messages:
                                    final_message = messages[current_id]
                                    final_result = {
                                        "status": "complete",
                                        "content": final_message.get("content", ""),
                                        "done": final_message.get("done", True),
                                    }
                                    
                                    # Verify complete workflow
                                    assert final_result["status"] == "complete"
                                    assert "Paris" in final_result["content"]
                                    assert final_result["done"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
