"""Client for the SCIM 2.0 endpoints.

Provides System for Cross-domain Identity Management endpoints for users and groups.
This is an experimental implementation and may not fully comply with SCIM 2.0 standards.
"""

from typing import Any, Optional

from owui_client.client_base import ResourceBase
from owui_client.models.scim import (
    SCIMGroup,
    SCIMGroupCreateRequest,
    SCIMGroupUpdateRequest,
    SCIMListResponse,
    SCIMPatchRequest,
    SCIMUser,
    SCIMUserCreateRequest,
    SCIMUserUpdateRequest,
)


class SCIMClient(ResourceBase):
    """Client for the SCIM endpoints."""

    async def get_service_provider_config(self) -> dict[str, Any]:
        """Get SCIM Service Provider Configuration.

        Returns the service provider configuration including supported features
        such as patch, bulk, filter, and authentication schemes.
        This endpoint does not require SCIM authentication.

        Returns:
            Dictionary containing service provider configuration.
        """
        return await self._request(
            "GET",
            "/v1/scim/v2/ServiceProviderConfig",
            model=None,
        )

    async def get_resource_types(self) -> list[dict[str, Any]]:
        """Get SCIM Resource Types.

        Returns the list of supported SCIM resource types (User and Group)
        including their endpoints and schemas.
        This endpoint does not require SCIM authentication.

        Returns:
            List of resource type definitions.
        """
        return await self._request(
            "GET",
            "/v1/scim/v2/ResourceTypes",
            model=None,
        )

    async def get_schemas(self) -> list[dict[str, Any]]:
        """Get SCIM Schemas.

        Returns the list of supported SCIM schemas (User and Group)
        including their attributes and requirements.
        This endpoint does not require SCIM authentication.

        Returns:
            List of schema definitions.
        """
        return await self._request(
            "GET",
            "/v1/scim/v2/Schemas",
            model=None,
        )

    async def get_users(
        self,
        startIndex: int = 1,
        count: int = 20,
        filter: Optional[str] = None,
    ) -> SCIMListResponse:
        """List SCIM Users.

        Retrieves a paginated list of users in SCIM format.
        Supports filtering by userName or externalId.
        Requires SCIM authentication.

        Args:
            startIndex: 1-based index of the first result to return.
            count: Maximum number of results to return (0-100).
            filter: SCIM filter expression (e.g. 'userName eq "user@example.com"').

        Returns:
            SCIM list response containing user resources.
        """
        params: dict[str, Any] = {
            "startIndex": startIndex,
            "count": count,
        }
        if filter is not None:
            params["filter"] = filter

        return await self._request(
            "GET",
            "/v1/scim/v2/Users",
            model=SCIMListResponse,
            params=params,
        )

    async def get_user(self, user_id: str) -> SCIMUser:
        """Get SCIM User by ID.

        Retrieves a specific user by their SCIM resource ID.
        Requires SCIM authentication.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            The SCIM user resource.
        """
        return await self._request(
            "GET",
            f"/v1/scim/v2/Users/{user_id}",
            model=SCIMUser,
        )

    async def create_user(self, user_data: SCIMUserCreateRequest) -> SCIMUser:
        """Create SCIM User.

        Creates a new user with the provided SCIM attributes.
        Checks for duplicates by externalId and email.
        Requires SCIM authentication.

        Args:
            user_data: SCIM user creation request data.

        Returns:
            The created SCIM user resource.
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
        """Update SCIM User (full replacement).

        Performs a full replacement update of the specified user.
        Requires SCIM authentication.

        Args:
            user_id: The unique identifier of the user.
            user_data: SCIM user update request data.

        Returns:
            The updated SCIM user resource.
        """
        return await self._request(
            "PUT",
            f"/v1/scim/v2/Users/{user_id}",
            model=SCIMUser,
            json=user_data.model_dump(by_alias=True),
        )

    async def patch_user(self, user_id: str, patch_data: SCIMPatchRequest) -> SCIMUser:
        """Update SCIM User (partial update).

        Applies a set of patch operations to the specified user.
        Supports replacing active status, userName, displayName, emails, and externalId.
        Requires SCIM authentication.

        Args:
            user_id: The unique identifier of the user.
            patch_data: SCIM patch request containing operations.

        Returns:
            The updated SCIM user resource.
        """
        return await self._request(
            "PATCH",
            f"/v1/scim/v2/Users/{user_id}",
            model=SCIMUser,
            json=patch_data.model_dump(by_alias=True),
        )

    async def delete_user(self, user_id: str) -> Any:
        """Delete SCIM User.

        Permanently deletes the specified user.
        Requires SCIM authentication.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            None or empty response on success (HTTP 204).
        """
        return await self._request(
            "DELETE",
            f"/v1/scim/v2/Users/{user_id}",
            model=None,
        )

    async def get_groups(
        self,
        startIndex: int = 1,
        count: int = 20,
        filter: Optional[str] = None,
    ) -> SCIMListResponse:
        """List SCIM Groups.

        Retrieves a paginated list of groups in SCIM format.
        Supports filtering by displayName.
        Requires SCIM authentication.

        Args:
            startIndex: 1-based index of the first result to return.
            count: Maximum number of results to return (0-100).
            filter: SCIM filter expression (e.g. 'displayName eq "Group Name"').

        Returns:
            SCIM list response containing group resources.
        """
        params: dict[str, Any] = {
            "startIndex": startIndex,
            "count": count,
        }
        if filter is not None:
            params["filter"] = filter

        return await self._request(
            "GET",
            "/v1/scim/v2/Groups",
            model=SCIMListResponse,
            params=params,
        )

    async def get_group(self, group_id: str) -> SCIMGroup:
        """Get SCIM Group by ID.

        Retrieves a specific group by its SCIM resource ID.
        Requires SCIM authentication.

        Args:
            group_id: The unique identifier of the group.

        Returns:
            The SCIM group resource.
        """
        return await self._request(
            "GET",
            f"/v1/scim/v2/Groups/{group_id}",
            model=SCIMGroup,
        )

    async def create_group(self, group_data: SCIMGroupCreateRequest) -> SCIMGroup:
        """Create SCIM Group.

        Creates a new group with the provided SCIM attributes.
        Requires SCIM authentication.

        Args:
            group_data: SCIM group creation request data.

        Returns:
            The created SCIM group resource.
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
        """Update SCIM Group (full replacement).

        Performs a full replacement update of the specified group.
        Requires SCIM authentication.

        Args:
            group_id: The unique identifier of the group.
            group_data: SCIM group update request data.

        Returns:
            The updated SCIM group resource.
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
        """Update SCIM Group (partial update).

        Applies a set of patch operations to the specified group.
        Supports add, replace, and remove operations on members and displayName.
        Requires SCIM authentication.

        Args:
            group_id: The unique identifier of the group.
            patch_data: SCIM patch request containing operations.

        Returns:
            The updated SCIM group resource.
        """
        return await self._request(
            "PATCH",
            f"/v1/scim/v2/Groups/{group_id}",
            model=SCIMGroup,
            json=patch_data.model_dump(by_alias=True),
        )

    async def delete_group(self, group_id: str) -> Any:
        """Delete SCIM Group.

        Permanently deletes the specified group.
        Requires SCIM authentication.

        Args:
            group_id: The unique identifier of the group.

        Returns:
            None or empty response on success (HTTP 204).
        """
        return await self._request(
            "DELETE",
            f"/v1/scim/v2/Groups/{group_id}",
            model=None,
        )
