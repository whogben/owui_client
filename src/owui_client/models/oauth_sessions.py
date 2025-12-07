from pydantic import BaseModel, ConfigDict


class OAuthSessionModel(BaseModel):
    """
    Model representing an OAuth session.

    This model stores information about an active OAuth session, including
    the provider, tokens, and expiration details.
    """

    id: str
    """The unique identifier for the OAuth session."""

    user_id: str
    """The ID of the user associated with this session."""

    provider: str
    """The OAuth provider name (e.g., 'google', 'microsoft')."""

    token: dict
    """
    The OAuth tokens.
    
    Typically contains keys like 'access_token', 'id_token', and 'refresh_token'.
    """

    expires_at: int
    """The timestamp (epoch) when the session/token expires."""

    created_at: int
    """The timestamp (epoch) when the session was created."""

    updated_at: int
    """The timestamp (epoch) when the session was last updated."""

    model_config = ConfigDict(from_attributes=True)
