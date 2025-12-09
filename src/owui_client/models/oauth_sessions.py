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

    Dict Fields:
        - `access_token` (str, required): The access token for OAuth authentication
        - `refresh_token` (str, optional): The refresh token for obtaining new access tokens
        - `id_token` (str, optional): The ID token containing user identity information
        - `expires_at` (int, optional): Timestamp when the token expires (epoch)
        - `expires_in` (int, optional): Duration in seconds until token expires
        - `issued_at` (int, optional): Timestamp when the token was issued
    """

    expires_at: int
    """The timestamp (epoch) when the session/token expires."""

    created_at: int
    """The timestamp (epoch) when the session was created."""

    updated_at: int
    """The timestamp (epoch) when the session was last updated."""

    model_config = ConfigDict(from_attributes=True)
