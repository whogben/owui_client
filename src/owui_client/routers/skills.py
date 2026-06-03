from typing import List, Optional

from owui_client.client_base import ResourceBase
from owui_client.models.skills import (
    SkillUserResponse,
    SkillModel,
    SkillResponse,
    SkillForm,
    SkillAccessResponse,
    SkillAccessListResponse,
    SkillAccessGrantsForm,
)


class SkillsClient(ResourceBase):
    """
    Client for the Skills endpoints.
    """

    async def get_skills(self) -> List[SkillUserResponse]:
        """Get all skills the authenticated user can read.

        Admins with bypass access control see all skills. Other users see only
        skills they own or have been granted read access to.

        Returns:
            List[SkillUserResponse]: List of skills with owner details.
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
        """Get a paginated, searchable list of skills with access info.

        Each result includes a `write_access` flag indicating whether the
        requesting user can modify that skill.

        Args:
            query: Optional search string to filter skills by name/description.
            view_option: Optional view filter (e.g. "mine", "shared").
            page: Page number (1-indexed). Defaults to 1.

        Returns:
            `SkillAccessListResponse`: Paginated skills with write access indicators.
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
        """Export all skills the user has read access to.

        Requires the `workspace.skills` permission for non-admin users.

        Returns:
            List[SkillModel]: Full skill models including content.
        """
        return await self._request(
            "GET",
            "/v1/skills/export",
            model=List[SkillModel],
        )

    async def create_new_skill(self, form_data: SkillForm) -> Optional[SkillResponse]:
        """Create a new skill.

        The `id` is lowercased and spaces replaced with hyphens automatically.
        Requires the `workspace.skills` permission for non-admin users.

        Args:
            form_data: The skill data including id, name, content, and meta.

        Returns:
            Optional[SkillResponse]: The created skill metadata (no content field).
        """
        return await self._request(
            "POST",
            "/v1/skills/create",
            json=form_data.model_dump(mode="json", exclude_none=True),
            model=Optional[SkillResponse],
        )

    async def get_skill_by_id(self, id: str) -> Optional[SkillAccessResponse]:
        """Get a single skill by ID with access information.

        Returns the skill details along with a `write_access` flag indicating
        whether the requesting user can modify it.

        Args:
            id: The skill ID.

        Returns:
            Optional[SkillAccessResponse]: The skill with write access indicator.
        """
        return await self._request(
            "GET",
            f"/v1/skills/id/{id}",
            model=Optional[SkillAccessResponse],
        )

    async def update_skill_by_id(
        self, id: str, form_data: SkillForm
    ) -> Optional[SkillModel]:
        """Update a skill by ID.

        Requires owner, write access, or admin role. Public access grants in the
        form data are filtered based on the `sharing.public_skills` permission.

        Args:
            id: The skill ID.
            form_data: The updated skill data.

        Returns:
            Optional[SkillModel]: The updated skill.
        """
        return await self._request(
            "POST",
            f"/v1/skills/id/{id}/update",
            json=form_data.model_dump(mode="json", exclude_none=True),
            model=Optional[SkillModel],
        )

    async def update_skill_access_by_id(
        self, id: str, form_data: SkillAccessGrantsForm
    ) -> Optional[SkillModel]:
        """Update access grants for a skill.

        Sets the access grants controlling who can read or write the skill.
        Requires owner, write access, or admin role. Public grants are filtered
        by the `sharing.public_skills` permission.

        Args:
            id: The skill ID.
            form_data: The access grants form with list of access grant dicts.

        Returns:
            Optional[SkillModel]: The updated skill.
        """
        return await self._request(
            "POST",
            f"/v1/skills/id/{id}/access/update",
            json=form_data.model_dump(mode="json", exclude_none=True),
            model=Optional[SkillModel],
        )

    async def toggle_skill_by_id(self, id: str) -> Optional[SkillModel]:
        """Toggle a skill's active state.

        Flips the `is_active` flag. Requires owner, write access, or admin role.

        Args:
            id: The skill ID.

        Returns:
            Optional[SkillModel]: The updated skill.
        """
        return await self._request(
            "POST",
            f"/v1/skills/id/{id}/toggle",
            model=Optional[SkillModel],
        )

    async def delete_skill_by_id(self, id: str) -> bool:
        """Delete a skill by ID.

        Requires owner, write access, or admin role.

        Args:
            id: The skill ID.

        Returns:
            bool: True if deletion succeeded.
        """
        return await self._request(
            "DELETE",
            f"/v1/skills/id/{id}/delete",
            model=bool,
        )
