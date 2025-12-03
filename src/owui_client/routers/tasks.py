from typing import Dict, Any, List, Optional
from owui_client.client_base import ResourceBase
from owui_client.models.tasks import TaskConfigForm


class TasksClient(ResourceBase):
    async def get_config(self) -> Dict[str, Any]:
        """
        Get the task configuration.

        :return: Task configuration dictionary
        """
        return await self._request(
            "GET",
            "/v1/tasks/config",
            model=dict,
        )

    async def update_config(self, form_data: TaskConfigForm) -> Dict[str, Any]:
        """
        Update the task configuration.

        :param form_data: The task configuration form
        :return: Updated task configuration dictionary
        """
        return await self._request(
            "POST",
            "/v1/tasks/config/update",
            model=dict,
            json=form_data.model_dump(),
        )

    async def generate_title(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a title for a chat.

        :param form_data: Dictionary containing 'model' and 'messages'
        :return: Chat completion response with the generated title
        """
        return await self._request(
            "POST",
            "/v1/tasks/title/completions",
            model=dict,
            json=form_data,
        )

    async def generate_follow_ups(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate follow-up questions.

        :param form_data: Dictionary containing 'model' and 'messages'
        :return: Chat completion response with generated follow-ups
        """
        return await self._request(
            "POST",
            "/v1/tasks/follow_up/completions",
            model=dict,
            json=form_data,
        )

    async def generate_tags(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate tags for a chat.

        :param form_data: Dictionary containing 'model' and 'messages'
        :return: Chat completion response with generated tags
        """
        return await self._request(
            "POST",
            "/v1/tasks/tags/completions",
            model=dict,
            json=form_data,
        )

    async def generate_image_prompt(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an image prompt.

        :param form_data: Dictionary containing 'model' and 'messages'
        :return: Chat completion response with generated image prompt
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

        :param form_data: Dictionary containing 'type', 'model', and 'messages'
        :return: Chat completion response with generated queries or list of strings
        """
        return await self._request(
            "POST",
            "/v1/tasks/queries/completions",
            model=dict,  # Can return list if cached, but usually dict response
            json=form_data,
        )

    async def generate_autocompletion(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate autocompletion.

        :param form_data: Dictionary containing 'type', 'prompt', 'messages', 'model'
        :return: Chat completion response with autocompletion
        """
        return await self._request(
            "POST",
            "/v1/tasks/auto/completions",
            model=dict,
            json=form_data,
        )

    async def generate_emoji(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an emoji.

        :param form_data: Dictionary containing 'prompt' and 'model'
        :return: Chat completion response with generated emoji
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

        :param form_data: Dictionary containing 'model', 'prompt', 'responses'
        :return: Chat completion response
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
        List all active tasks.

        :return: Dictionary with 'tasks' key containing list of task IDs
        """
        return await self._request(
            "GET",
            "/tasks",
            model=dict,
        )

    async def stop_task(self, task_id: str) -> Dict[str, Any]:
        """
        Stop a specific task.

        :param task_id: The ID of the task to stop
        :return: Status dictionary
        """
        return await self._request(
            "POST",
            f"/tasks/stop/{task_id}",
            model=dict,
        )

    async def list_tasks_by_chat(self, chat_id: str) -> Dict[str, List[str]]:
        """
        List tasks associated with a chat.

        :param chat_id: The ID of the chat
        :return: Dictionary with 'task_ids' key containing list of task IDs
        """
        return await self._request(
            "GET",
            f"/tasks/chat/{chat_id}",
            model=dict,
        )

