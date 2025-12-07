from typing import Dict, Any, List, Optional
from owui_client.client_base import ResourceBase
from owui_client.models.tasks import TaskConfigForm


class TasksClient(ResourceBase):
    """
    Client for the Tasks endpoints.
    """

    async def get_config(self) -> Dict[str, Any]:
        """
        Get the global task configuration.

        This includes settings for title generation, tags, autocomplete, etc.

        Returns:
            Dict[str, Any]: The task configuration dictionary.
        """
        return await self._request(
            "GET",
            "/v1/tasks/config",
            model=dict,
        )

    async def update_config(self, form_data: TaskConfigForm) -> Dict[str, Any]:
        """
        Update the global task configuration.

        Args:
            form_data (TaskConfigForm): The configuration settings to update.

        Returns:
            Dict[str, Any]: The updated task configuration dictionary.
        """
        return await self._request(
            "POST",
            "/v1/tasks/config/update",
            model=dict,
            json=form_data.model_dump(),
        )

    async def generate_title(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a title for a chat conversation.

        Args:
            form_data (Dict[str, Any]): Dictionary containing:
                - `model` (str): The model ID to use.
                - `messages` (List[Dict]): The chat history messages.
                - `chat_id` (Optional[str]): The ID of the chat.

        Returns:
            Dict[str, Any]: The chat completion response containing the generated title.
        """
        return await self._request(
            "POST",
            "/v1/tasks/title/completions",
            model=dict,
            json=form_data,
        )

    async def generate_follow_ups(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate follow-up questions for a chat conversation.

        Args:
            form_data (Dict[str, Any]): Dictionary containing:
                - `model` (str): The model ID to use.
                - `messages` (List[Dict]): The chat history messages.
                - `chat_id` (Optional[str]): The ID of the chat.

        Returns:
            Dict[str, Any]: The chat completion response containing generated follow-up questions.
        """
        return await self._request(
            "POST",
            "/v1/tasks/follow_up/completions",
            model=dict,
            json=form_data,
        )

    async def generate_tags(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate tags for a chat conversation.

        Args:
            form_data (Dict[str, Any]): Dictionary containing:
                - `model` (str): The model ID to use.
                - `messages` (List[Dict]): The chat history messages.
                - `chat_id` (Optional[str]): The ID of the chat.

        Returns:
            Dict[str, Any]: The chat completion response containing generated tags.
        """
        return await self._request(
            "POST",
            "/v1/tasks/tags/completions",
            model=dict,
            json=form_data,
        )

    async def generate_image_prompt(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an image prompt based on the chat context.

        Args:
            form_data (Dict[str, Any]): Dictionary containing:
                - `model` (str): The model ID to use.
                - `messages` (List[Dict]): The chat history messages.
                - `chat_id` (Optional[str]): The ID of the chat.

        Returns:
            Dict[str, Any]: The chat completion response containing the generated image prompt.
        """
        return await self._request(
            "POST",
            "/v1/tasks/image_prompt/completions",
            model=dict,
            json=form_data,
        )

    async def generate_queries(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate search or retrieval queries.

        Args:
            form_data (Dict[str, Any]): Dictionary containing:
                - `type` (str): Either "web_search" or "retrieval".
                - `model` (str): The model ID to use.
                - `messages` (List[Dict]): The chat history messages.
                - `chat_id` (Optional[str]): The ID of the chat.

        Returns:
            Dict[str, Any]: The chat completion response containing generated queries.
        """
        return await self._request(
            "POST",
            "/v1/tasks/queries/completions",
            model=dict,  # Can return list if cached, but usually dict response
            json=form_data,
        )

    async def generate_autocompletion(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate text autocompletion.

        Args:
            form_data (Dict[str, Any]): Dictionary containing:
                - `type` (str): The type of autocompletion context.
                - `prompt` (str): The text to autocomplete.
                - `messages` (List[Dict]): The chat history messages.
                - `model` (str): The model ID to use.
                - `chat_id` (Optional[str]): The ID of the chat.

        Returns:
            Dict[str, Any]: The chat completion response containing the autocompletion.
        """
        return await self._request(
            "POST",
            "/v1/tasks/auto/completions",
            model=dict,
            json=form_data,
        )

    async def generate_emoji(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an emoji based on the prompt.

        Args:
            form_data (Dict[str, Any]): Dictionary containing:
                - `prompt` (str): The text to generate an emoji for.
                - `model` (str): The model ID to use.
                - `chat_id` (Optional[str]): The ID of the chat.

        Returns:
            Dict[str, Any]: The chat completion response containing the generated emoji.
        """
        return await self._request(
            "POST",
            "/v1/tasks/emoji/completions",
            model=dict,
            json=form_data,
        )

    async def generate_moa_response(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a Mixture of Agents (MoA) response.

        Args:
            form_data (Dict[str, Any]): Dictionary containing:
                - `model` (str): The model ID to use (aggregator model).
                - `prompt` (str): The original user prompt.
                - `responses` (List[str]): The responses from other agents/models to aggregate.
                - `stream` (bool): Whether to stream the response (default False).

        Returns:
            Dict[str, Any]: The chat completion response.
        """
        return await self._request(
            "POST",
            "/v1/tasks/moa/completions",
            model=dict,
            json=form_data,
        )

    # Top-level task management endpoints

    async def list_tasks(self) -> Dict[str, List[str]]:
        """
        List all active background tasks.

        Returns:
            Dict[str, List[str]]: Dictionary with 'tasks' key containing a list of task IDs.
        """
        return await self._request(
            "GET",
            "/tasks",
            model=dict,
        )

    async def stop_task(self, task_id: str) -> Dict[str, Any]:
        """
        Stop a specific background task.

        Args:
            task_id (str): The ID of the task to stop.

        Returns:
            Dict[str, Any]: Status dictionary (e.g., {"status": True}).
        """
        return await self._request(
            "POST",
            f"/tasks/stop/{task_id}",
            model=dict,
        )

    async def list_tasks_by_chat(self, chat_id: str) -> Dict[str, List[str]]:
        """
        List background tasks associated with a specific chat.

        Args:
            chat_id (str): The ID of the chat.

        Returns:
            Dict[str, List[str]]: Dictionary with 'task_ids' key containing a list of task IDs.
        """
        return await self._request(
            "GET",
            f"/tasks/chat/{chat_id}",
            model=dict,
        )

