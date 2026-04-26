"""SCIM 2.0 models for the Open WebUI API.

Models that mirror the backend's SCIM (System for Cross-domain Identity Management)
schemas and request/response payloads. These are used by the experimental SCIM 2.0
endpoints for user and group provisioning.
"""

from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field

SCIM_USER_SCHEMA = "urn:ietf:params:scim:schemas:core:2.0:User"
SCIM_GROUP_SCHEMA = "urn:ietf:params:scim:schemas:core:2.0:Group"
SCIM_LIST_RESPONSE_SCHEMA = "urn:ietf:params:scim:api:messages:2.0:ListResponse"
SCIM_ERROR_SCHEMA = "urn:ietf:params:scim:api:messages:2.0:Error"


class SCIMError(BaseModel):
    """SCIM-compliant error response.

    Returned when a SCIM operation fails. The `scimType` field provides
    a machine-readable error category per RFC 7644.
    """

    schemas: list[str] = [SCIM_ERROR_SCHEMA]
    """Schema URIs defining this error response. Always includes the SCIM error schema."""

    status: str
    """HTTP status code as a string (e.g. '404', '409')."""

    scimType: Optional[str] = None
    """SCIM-specific error type.

    Common values:
    - `invalidValue`: The request body or parameter is malformed or invalid.
    - `uniqueness`: A resource with the same unique attribute already exists.
    - `invalidSyntax`: The filter or query syntax is invalid.
    """

    detail: Optional[str] = None
    """Human-readable description of the error."""


class SCIMMeta(BaseModel):
    """Metadata attached to every SCIM resource."""

    resourceType: str
    """Type of resource (e.g. 'User', 'Group')."""

    created: str
    """ISO 8601 timestamp of resource creation."""

    lastModified: str
    """ISO 8601 timestamp of the most recent modification."""

    location: Optional[str] = None
    """Full URL where the resource can be retrieved."""

    version: Optional[str] = None
    """ETag version identifier for optimistic concurrency control."""


class SCIMName(BaseModel):
    """Structured name components for a SCIM User."""

    formatted: Optional[str] = None
    """Full formatted name (e.g. 'Dr. John A. Smith Jr.')."""

    familyName: Optional[str] = None
    """Family name or surname."""

    givenName: Optional[str] = None
    """Given or first name."""

    middleName: Optional[str] = None
    """Middle name."""

    honorificPrefix: Optional[str] = None
    """Honorific prefix (e.g. 'Dr.', 'Mr.', 'Ms.')."""

    honorificSuffix: Optional[str] = None
    """Honorific suffix (e.g. 'Jr.', 'III', 'Ph.D.')."""


class SCIMEmail(BaseModel):
    """Email address associated with a SCIM User."""

    value: str
    """The email address value."""

    type: Optional[str] = "work"
    """Email type classification (e.g. 'work', 'home')."""

    primary: bool = True
    """Whether this is the user's primary email address."""

    display: Optional[str] = None
    """Display label for the email address."""


class SCIMPhoto(BaseModel):
    """Photo or image reference for a SCIM User."""

    value: str
    """URL pointing to the photo resource."""

    type: Optional[str] = "photo"
    """Photo type (e.g. 'photo', 'thumbnail')."""

    primary: bool = True
    """Whether this is the primary photo."""

    display: Optional[str] = None
    """Display label for the photo."""


class SCIMGroupMember(BaseModel):
    """Reference to a member of a SCIM Group."""

    model_config = ConfigDict(populate_by_name=True)

    value: str
    """Unique identifier of the member (typically a User ID)."""

    ref: Optional[str] = Field(None, alias="$ref")
    """SCIM resource URI reference to the member.

    Serialized as `$ref` in JSON per SCIM 2.0 spec.
    """

    type: Optional[str] = "User"
    """Type of member resource (typically 'User')."""

    display: Optional[str] = None
    """Display name of the member."""


class SCIMUser(BaseModel):
    """SCIM User resource representation.

    Maps internal Open WebUI user records to the SCIM 2.0 User schema.
    The `userName` field is typically the user's email address.
    """

    model_config = ConfigDict(populate_by_name=True)

    schemas: list[str] = [SCIM_USER_SCHEMA]
    """Schema URIs defining this resource."""

    id: str
    """Unique identifier for the user within Open WebUI."""

    externalId: Optional[str] = None
    """External identifier assigned by the identity provider for account linking."""

    userName: str
    """User identifier, typically the email address."""

    name: Optional[SCIMName] = None
    """Structured name components (givenName, familyName, etc.)."""

    displayName: str
    """Human-readable display name for the user."""

    emails: list[SCIMEmail]
    """List of email addresses associated with the user."""

    active: bool = True
    """Whether the user account is active.

    In Open WebUI, inactive users have role 'pending'.
    """

    photos: Optional[list[SCIMPhoto]] = None
    """List of photo references for the user."""

    groups: Optional[list[dict[str, str]]] = None
    """Groups the user is a member of.

    Dict Fields:
        - `value` (str): Group ID
        - `display` (str): Group display name
        - `$ref` (str): SCIM resource URI for the group
        - `type` (str): Membership type, typically 'direct'
    """

    meta: SCIMMeta
    """Resource metadata including creation time and location."""


class SCIMUserCreateRequest(BaseModel):
    """Request payload for creating a SCIM User."""

    model_config = ConfigDict(populate_by_name=True)

    schemas: list[str] = [SCIM_USER_SCHEMA]
    """Schema URIs defining this request."""

    externalId: Optional[str] = None
    """External identifier from the identity provider."""

    userName: str
    """Username, typically the email address."""

    name: Optional[SCIMName] = None
    """Structured name components."""

    displayName: str
    """Display name for the user."""

    emails: list[SCIMEmail]
    """List of email addresses. The primary email is used as the user's email."""

    active: bool = True
    """Whether the user account should be active upon creation."""

    password: Optional[str] = None
    """Initial password for the user (optional)."""

    photos: Optional[list[SCIMPhoto]] = None
    """List of photo URLs for the user's profile."""


class SCIMUserUpdateRequest(BaseModel):
    """Request payload for fully replacing a SCIM User."""

    model_config = ConfigDict(populate_by_name=True)

    schemas: list[str] = [SCIM_USER_SCHEMA]
    """Schema URIs defining this request."""

    id: Optional[str] = None
    """Unique identifier for the user (optional in update payload)."""

    externalId: Optional[str] = None
    """External identifier from the identity provider."""

    userName: Optional[str] = None
    """Username, typically the email address."""

    name: Optional[SCIMName] = None
    """Structured name components."""

    displayName: Optional[str] = None
    """Display name for the user."""

    emails: Optional[list[SCIMEmail]] = None
    """List of email addresses."""

    active: Optional[bool] = None
    """Whether the user account is active."""

    photos: Optional[list[SCIMPhoto]] = None
    """List of photo URLs."""


class SCIMGroup(BaseModel):
    """SCIM Group resource representation.

    Maps internal Open WebUI group records to the SCIM 2.0 Group schema.
    """

    model_config = ConfigDict(populate_by_name=True)

    schemas: list[str] = [SCIM_GROUP_SCHEMA]
    """Schema URIs defining this resource."""

    id: str
    """Unique identifier for the group within Open WebUI."""

    displayName: str
    """Human-readable display name for the group."""

    members: Optional[list[SCIMGroupMember]] = []
    """List of members belonging to the group."""

    meta: SCIMMeta
    """Resource metadata including creation time and location."""


class SCIMGroupCreateRequest(BaseModel):
    """Request payload for creating a SCIM Group."""

    model_config = ConfigDict(populate_by_name=True)

    schemas: list[str] = [SCIM_GROUP_SCHEMA]
    """Schema URIs defining this request."""

    displayName: str
    """Display name for the new group."""

    members: Optional[list[SCIMGroupMember]] = []
    """Initial list of group members to add at creation time."""


class SCIMGroupUpdateRequest(BaseModel):
    """Request payload for fully replacing a SCIM Group."""

    model_config = ConfigDict(populate_by_name=True)

    schemas: list[str] = [SCIM_GROUP_SCHEMA]
    """Schema URIs defining this request."""

    displayName: Optional[str] = None
    """Display name for the group."""

    members: Optional[list[SCIMGroupMember]] = None
    """Complete list of group members (replaces existing members)."""


class SCIMListResponse(BaseModel):
    """Paginated list response format for SCIM queries.

    Used for both User and Group list endpoints. The `Resources` field
    contains the actual resource objects, which will be User or Group dicts
    depending on the endpoint.
    """

    schemas: list[str] = [SCIM_LIST_RESPONSE_SCHEMA]
    """Schema URIs defining this list response."""

    totalResults: int
    """Total number of results available across all pages."""

    itemsPerPage: int
    """Number of items returned in this response page."""

    startIndex: int
    """1-based index of the first result in this page."""

    Resources: list[Any]
    """List of resource objects (SCIM User or Group dicts)."""


class SCIMPatchOperation(BaseModel):
    """Single operation within a SCIM Patch request.

    Supports add, replace, and remove operations on resource attributes.
    The `path` field uses attribute notation (e.g. 'displayName', 'members',
    'emails[primary eq true].value').
    """

    op: str
    """Operation type: 'add', 'replace', or 'remove'."""

    path: Optional[str] = None
    """Target attribute path for the operation.

    Examples:
    - `displayName`
    - `members`
    - `emails[primary eq true].value`
    - `name.formatted`
    """

    value: Optional[Any] = None
    """Value to apply for add or replace operations.

    For remove operations, this is typically omitted.
    For members, this may be a list of dicts with `value` keys.
    """


class SCIMPatchRequest(BaseModel):
    """SCIM Patch request payload for partial resource updates.

    Contains one or more operations to apply atomically to a resource.
    Used for both User and Group patch endpoints.
    """

    schemas: list[str] = ["urn:ietf:params:scim:api:messages:2.0:PatchOp"]
    """Schema URIs defining this patch operation request."""

    Operations: list[SCIMPatchOperation]
    """List of patch operations to apply to the target resource."""
