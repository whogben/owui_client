"""Client for the SCIM 2.0 endpoints.

Note: SCIM endpoints use a separate bearer token for authentication
(configured via ENABLE_SCIM and SCIM_TOKEN environment variables on the
server), NOT the normal Open WebUI API key. You must configure the
client's api_key to use the SCIM token when calling these endpoints.

This is an experimental implementation and may not fully comply with
SCIM 2.0 standards (RFC 7643/7644).
"""

from typing import Optional
from owui_client.client_base import ResourceBase
from owui_client.models.scim import (
    SCIMUser,
    SCIMUserCreateRequest,
    SCIMUserUpdateRequest,
    SCIMGroup,
    SCIMGroupCreateRequest,
    SCIMGroupUpdateRequest,
    SCIMListResponse,
    SCIMPatchRequest,
)


class ScimClient(ResourceBase):
    """Client for the SCIM 2.0 endpoints.

    Uses a separate bearer token (SCIM_TOKEN) rather than the normal OWUI API key.
    """

    async def get_service_provider_config(self) -> dict:
        """Get SCIM Service Provider Configuration."""
        return await self._request("GET", "/v1/scim/v2/ServiceProviderConfig")

    async def get_resource_types(self) -> list[dict]:
        """Get SCIM Resource Types."""
        return await self._request("GET", "/v1/scim/v2/ResourceTypes")

    async def get_schemas(self) -> list[dict]:
        """Get SCIM Schemas."""
        return await self._request("GET", "/v1/scim/v2/Schemas")

    async def get_users(
        self,
        start_index: int = 1,
        count: int = 20,
        filter: Optional[str] = None,
    ) -> SCIMListResponse:
        """List SCIM Users.

        Args:
            start_index: 1-based pagination start index.
            count: Number of results per page (max 100).
            filter: SCIM filter expression (e.g. 'userName eq "user@example.com"').
        """
        params: dict = {"startIndex": start_index, "count": count}
        if filter:
            params["filter"] = filter
        return await self._request(
            "GET", "/v1/scim/v2/Users", model=SCIMListResponse, params=params
        )

    async def get_user(self, user_id: str) -> SCIMUser:
        """Get a SCIM User by ID.

        Args:
            user_id: The user ID.
        """
        return await self._request(
            "GET", f"/v1/scim/v2/Users/{user_id}", model=SCIMUser
        )

    async def create_user(self, user_data: SCIMUserCreateRequest) -> SCIMUser:
        """Create a SCIM User.

        Args:
            user_data: The user data to create.
        """
        return await self._request(
            "POST",
            "/v1/scim/v2/Users",
            model=SCIMUser,
            json=user_data.model_dump(by_alias=True),
        )

    async def update_user(
        self, user_id: str, user_data: SCIMUserUpdateRequest
    ) -> SCIMUser:
        """Update a SCIM User (full update).

        Args:
            user_id: The user ID.
            user_data: The user data to update.
        """
        return await self._request(
            "PUT",
            f"/v1/scim/v2/Users/{user_id}",
            model=SCIMUser,
            json=user_data.model_dump(by_alias=True),
        )

    async def patch_user(
        self, user_id: str, patch_data: SCIMPatchRequest
    ) -> SCIMUser:
        """Patch a SCIM User (partial update).

        Args:
            user_id: The user ID.
            patch_data: The patch operations to apply.
        """
        return await self._request(
            "PATCH",
            f"/v1/scim/v2/Users/{user_id}",
            model=SCIMUser,
            json=patch_data.model_dump(by_alias=True),
        )

    async def delete_user(self, user_id: str) -> bool:
        """Delete a SCIM User.

        Args:
            user_id: The user ID.

        Returns:
            True if deletion succeeded.

        Raises:
            httpx.HTTPStatusError: If the deletion fails.
        """
        await self._request("DELETE", f"/v1/scim/v2/Users/{user_id}")
        return True

    async def get_groups(
        self,
        start_index: int = 1,
        count: int = 20,
        filter: Optional[str] = None,
    ) -> SCIMListResponse:
        """List SCIM Groups.

        Args:
            start_index: 1-based pagination start index.
            count: Number of results per page (max 100).
            filter: SCIM filter expression (e.g. 'displayName eq "MyGroup"').
        """
        params: dict = {"startIndex": start_index, "count": count}
        if filter:
            params["filter"] = filter
        return await self._request(
            "GET", "/v1/scim/v2/Groups", model=SCIMListResponse, params=params
        )

    async def get_group(self, group_id: str) -> SCIMGroup:
        """Get a SCIM Group by ID.

        Args:
            group_id: The group ID.
        """
        return await self._request(
            "GET", f"/v1/scim/v2/Groups/{group_id}", model=SCIMGroup
        )

    async def create_group(self, group_data: SCIMGroupCreateRequest) -> SCIMGroup:
        """Create a SCIM Group.

        Args:
            group_data: The group data to create.
        """
        return await self._request(
            "POST",
            "/v1/scim/v2/Groups",
            model=SCIMGroup,
            json=group_data.model_dump(by_alias=True),
        )

    async def update_group(
        self, group_id: str, group_data: SCIMGroupUpdateRequest
    ) -> SCIMGroup:
        """Update a SCIM Group (full update).

        Args:
            group_id: The group ID.
            group_data: The group data to update.
        """
        return await self._request(
            "PUT",
            f"/v1/scim/v2/Groups/{group_id}",
            model=SCIMGroup,
            json=group_data.model_dump(by_alias=True),
        )

    async def patch_group(
        self, group_id: str, patch_data: SCIMPatchRequest
    ) -> SCIMGroup:
        """Patch a SCIM Group (partial update).

        Args:
            group_id: The group ID.
            patch_data: The patch operations to apply.
        """
        return await self._request(
            "PATCH",
            f"/v1/scim/v2/Groups/{group_id}",
            model=SCIMGroup,
            json=patch_data.model_dump(by_alias=True),
        )

    async def delete_group(self, group_id: str) -> bool:
        """Delete a SCIM Group.

        Args:
            group_id: The group ID.

        Returns:
            True if deletion succeeded.

        Raises:
            httpx.HTTPStatusError: If the deletion fails.
        """
        await self._request("DELETE", f"/v1/scim/v2/Groups/{group_id}")
        return True
