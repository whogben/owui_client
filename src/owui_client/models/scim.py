"""Models for the SCIM 2.0 endpoints.

These models implement the SCIM 2.0 protocol (RFC 7643/7644) for user
and group provisioning. Note that this is an experimental implementation
and may not fully comply with SCIM 2.0 standards.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

SCIM_USER_SCHEMA = "urn:ietf:params:scim:schemas:core:2.0:User"
SCIM_GROUP_SCHEMA = "urn:ietf:params:scim:schemas:core:2.0:Group"
SCIM_LIST_RESPONSE_SCHEMA = "urn:ietf:params:scim:api:messages:2.0:ListResponse"
SCIM_ERROR_SCHEMA = "urn:ietf:params:scim:api:messages:2.0:Error"


class SCIMError(BaseModel):
    """SCIM Error Response."""
    schemas: List[str] = [SCIM_ERROR_SCHEMA]
    status: str
    scimType: Optional[str] = None
    detail: Optional[str] = None


class SCIMMeta(BaseModel):
    """SCIM Resource Metadata."""
    resourceType: str
    created: str
    lastModified: str
    location: Optional[str] = None
    version: Optional[str] = None


class SCIMName(BaseModel):
    """SCIM User Name."""
    formatted: Optional[str] = None
    familyName: Optional[str] = None
    givenName: Optional[str] = None
    middleName: Optional[str] = None
    honorificPrefix: Optional[str] = None
    honorificSuffix: Optional[str] = None


class SCIMEmail(BaseModel):
    """SCIM Email."""
    value: str
    type: Optional[str] = "work"
    primary: bool = True
    display: Optional[str] = None


class SCIMPhoto(BaseModel):
    """SCIM Photo."""
    value: str
    type: Optional[str] = "photo"
    primary: bool = True
    display: Optional[str] = None


class SCIMGroupMember(BaseModel):
    """SCIM Group Member."""
    value: str
    ref: Optional[str] = Field(None, alias="$ref")
    type: Optional[str] = "User"
    display: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class SCIMUser(BaseModel):
    """SCIM User Resource."""
    schemas: List[str] = [SCIM_USER_SCHEMA]
    id: str
    externalId: Optional[str] = None
    userName: str
    name: Optional[SCIMName] = None
    displayName: str
    emails: List[SCIMEmail]
    active: bool = True
    photos: Optional[List[SCIMPhoto]] = None
    groups: Optional[List[Dict[str, str]]] = None
    """SCIM groups the user belongs to. Each dict in the list represents a group.

    Dict Fields:
        - `value` (str, required): The unique ID of the group.
        - `display` (str, optional): Human-readable name of the group.
        - `type` (str, optional): Group membership type, e.g. 'direct'.
    """
    meta: SCIMMeta

    model_config = ConfigDict(populate_by_name=True)


class SCIMUserCreateRequest(BaseModel):
    """SCIM User Create Request."""
    schemas: List[str] = [SCIM_USER_SCHEMA]
    externalId: Optional[str] = None
    userName: str
    name: Optional[SCIMName] = None
    displayName: str
    emails: List[SCIMEmail]
    active: bool = True
    password: Optional[str] = None
    photos: Optional[List[SCIMPhoto]] = None

    model_config = ConfigDict(populate_by_name=True)


class SCIMUserUpdateRequest(BaseModel):
    """SCIM User Update Request."""
    schemas: List[str] = [SCIM_USER_SCHEMA]
    id: Optional[str] = None
    externalId: Optional[str] = None
    userName: Optional[str] = None
    name: Optional[SCIMName] = None
    displayName: Optional[str] = None
    emails: Optional[List[SCIMEmail]] = None
    active: Optional[bool] = None
    photos: Optional[List[SCIMPhoto]] = None

    model_config = ConfigDict(populate_by_name=True)


class SCIMGroup(BaseModel):
    """SCIM Group Resource."""
    schemas: List[str] = [SCIM_GROUP_SCHEMA]
    id: str
    displayName: str
    members: Optional[List[SCIMGroupMember]] = []
    meta: SCIMMeta

    model_config = ConfigDict(populate_by_name=True)


class SCIMGroupCreateRequest(BaseModel):
    """SCIM Group Create Request."""
    schemas: List[str] = [SCIM_GROUP_SCHEMA]
    displayName: str
    members: Optional[List[SCIMGroupMember]] = []

    model_config = ConfigDict(populate_by_name=True)


class SCIMGroupUpdateRequest(BaseModel):
    """SCIM Group Update Request."""
    schemas: List[str] = [SCIM_GROUP_SCHEMA]
    displayName: Optional[str] = None
    members: Optional[List[SCIMGroupMember]] = None

    model_config = ConfigDict(populate_by_name=True)


class SCIMListResponse(BaseModel):
    """SCIM List Response."""
    schemas: List[str] = [SCIM_LIST_RESPONSE_SCHEMA]
    totalResults: int
    itemsPerPage: int
    startIndex: int
    Resources: List[Any]


class SCIMPatchOperation(BaseModel):
    """SCIM Patch Operation."""
    op: str
    path: Optional[str] = None
    value: Optional[Any] = None


class SCIMPatchRequest(BaseModel):
    """SCIM Patch Request."""
    schemas: List[str] = ["urn:ietf:params:scim:api:messages:2.0:PatchOp"]
    Operations: List[SCIMPatchOperation]
