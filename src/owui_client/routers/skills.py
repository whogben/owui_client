"""Client for the Skills endpoints."""

from typing import Optional
from owui_client.client_base import ResourceBase
from owui_client.models.skills import (
    SkillForm,
    SkillModel,
    SkillResponse,
    SkillUserResponse,
    SkillAccessResponse,
    SkillAccessListResponse,
)


class SkillsClient(ResourceBase):
    """Client for the Skills endpoints."""

    async def get_skills(self) -> list[SkillUserResponse]:
        """Get all skills for the current user."""
        return await self._request("GET", "/v1/skills/")

    async def get_skill_list(
        self,
        query: Optional[str] = None,
        view_option: Optional[str] = None,
        page: Optional[int] = None,
    ) -> SkillAccessListResponse:
        """Get paginated skill list with access info."""
        params = {}
        if query:
            params["query"] = query
        if view_option:
            params["view_option"] = view_option
        if page:
            params["page"] = page
        return await self._request(
            "GET", "/v1/skills/list", model=SkillAccessListResponse, params=params
        )

    async def export_skills(self) -> list[SkillModel]:
        """Export all skills."""
        return await self._request("GET", "/v1/skills/export", model=list[SkillModel])

    async def create_skill(self, form: SkillForm) -> Optional[SkillResponse]:
        """Create a new skill."""
        return await self._request(
            "POST",
            "/v1/skills/create",
            model=Optional[SkillResponse],
            json=form.model_dump(),
        )

    async def get_skill_by_id(self, id: str) -> Optional[SkillAccessResponse]:
        """Get a skill by ID with access info."""
        return await self._request(
            "GET",
            f"/v1/skills/id/{id}",
            model=Optional[SkillAccessResponse],
        )

    async def update_skill_by_id(self, id: str, form: SkillForm) -> Optional[SkillModel]:
        """Update a skill by ID."""
        return await self._request(
            "POST",
            f"/v1/skills/id/{id}/update",
            model=Optional[SkillModel],
            json=form.model_dump(),
        )

    async def update_skill_access_by_id(
        self, id: str, access_grants: list[dict]
    ) -> Optional[SkillModel]:
        """Update skill access grants by ID.

        Args:
            id: The skill ID.
            access_grants: List of access grant dicts to set.
        """
        return await self._request(
            "POST",
            f"/v1/skills/id/{id}/access/update",
            model=Optional[SkillModel],
            json={"access_grants": access_grants},
        )

    async def toggle_skill_by_id(self, id: str) -> Optional[SkillModel]:
        """Toggle a skill's active status by ID."""
        return await self._request(
            "POST",
            f"/v1/skills/id/{id}/toggle",
            model=Optional[SkillModel],
        )

    async def delete_skill_by_id(self, id: str) -> bool:
        """Delete a skill by ID."""
        return await self._request(
            "DELETE",
            f"/v1/skills/id/{id}/delete",
            model=bool,
        )
