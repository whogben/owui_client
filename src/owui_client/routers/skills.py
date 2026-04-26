from typing import List, Optional
from owui_client.client_base import ResourceBase
from owui_client.models.skills import (
    SkillUserResponse,
    SkillAccessResponse,
    SkillAccessListResponse,
    SkillModel,
    SkillResponse,
    SkillForm,
    SkillAccessGrantsForm,
)


class SkillsClient(ResourceBase):
    """
    Client for the Skills endpoints.
    """

    async def get_skills(self) -> List[SkillUserResponse]:
        """
        Get all available skills.

        Returns skills the user has read access to, including their own
        and those shared via access grants.

        Returns:
            List[SkillUserResponse]: List of skills with user information.
        """
        return await self._request(
            "GET",
            "/v1/skills/",
            model=List[SkillUserResponse],
        )

    async def get_skill_list(
        self,
        query: Optional[str] = None,
        view_option: Optional[str] = None,
        page: Optional[int] = 1,
    ) -> SkillAccessListResponse:
        """
        Get a paginated list of skills with access information.

        Supports filtering by query string and view option.

        Args:
            query: Optional search query to filter skills by name or description.
            view_option: Optional view filter - 'created' for own skills, 'shared' for others.
            page: Page number for pagination (1-based). Defaults to 1.

        Returns:
            `SkillAccessListResponse`: Paginated list of skills with write_access flags.
        """
        params = {}
        if query is not None:
            params["query"] = query
        if view_option is not None:
            params["view_option"] = view_option
        if page is not None:
            params["page"] = page

        return await self._request(
            "GET",
            "/v1/skills/list",
            params=params,
            model=SkillAccessListResponse,
        )

    async def export_skills(self) -> List[SkillModel]:
        """
        Export all skills the user has read access to.

        Requires admin role or 'workspace.skills' permission.

        Returns:
            List[SkillModel]: List of skills with full content.
        """
        return await self._request(
            "GET",
            "/v1/skills/export",
            model=List[SkillModel],
        )

    async def create_new_skill(self, form_data: SkillForm) -> Optional[SkillResponse]:
        """
        Create a new skill.

        Requires admin role or 'workspace.skills' permission.
        The skill ID will be normalized to lowercase with spaces replaced by hyphens.

        Args:
            form_data: The skill data, including ID, name, and content.

        Returns:
            Optional[SkillResponse]: The created skill metadata.
        """
        return await self._request(
            "POST",
            "/v1/skills/create",
            json=form_data.model_dump(mode="json"),
            model=Optional[SkillResponse],
        )

    async def get_skill_by_id(self, id: str) -> Optional[SkillAccessResponse]:
        """
        Get a skill by its unique ID.

        Args:
            id: The skill ID.

        Returns:
            Optional[SkillAccessResponse]: The skill details with access information.
        """
        return await self._request(
            "GET",
            f"/v1/skills/id/{id}",
            model=Optional[SkillAccessResponse],
        )

    async def update_skill_by_id(
        self, id: str, form_data: SkillForm
    ) -> Optional[SkillModel]:
        """
        Update a skill by ID.

        Args:
            id: The skill ID.
            form_data: The updated skill data.

        Returns:
            Optional[SkillModel]: The updated skill details.
        """
        return await self._request(
            "POST",
            f"/v1/skills/id/{id}/update",
            json=form_data.model_dump(mode="json"),
            model=Optional[SkillModel],
        )

    async def update_skill_access_by_id(
        self, id: str, form_data: SkillAccessGrantsForm
    ) -> Optional[SkillModel]:
        """
        Update access grants for a skill.

        Sets the access grants for a skill, controlling which users and groups
        can read or write the skill. Requires owner, write access, or admin role.

        Args:
            id: The skill ID.
            form_data: The access grants form with list of access grant dicts.

        Returns:
            Optional[SkillModel]: The updated skill details.
        """
        return await self._request(
            "POST",
            f"/v1/skills/id/{id}/access/update",
            json=form_data.model_dump(mode="json"),
            model=Optional[SkillModel],
        )

    async def toggle_skill_by_id(self, id: str) -> Optional[SkillModel]:
        """
        Toggle a skill's active state by ID.

        Args:
            id: The skill ID.

        Returns:
            Optional[SkillModel]: The updated skill details.
        """
        return await self._request(
            "POST",
            f"/v1/skills/id/{id}/toggle",
            model=Optional[SkillModel],
        )

    async def delete_skill_by_id(self, id: str) -> bool:
        """
        Delete a skill by ID.

        Args:
            id: The skill ID.

        Returns:
            bool: True if successful, False otherwise.
        """
        return await self._request(
            "DELETE",
            f"/v1/skills/id/{id}/delete",
            model=bool,
        )
