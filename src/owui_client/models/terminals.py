from pydantic import BaseModel, ConfigDict


class TerminalServer(BaseModel):
    """A terminal server connection available to the authenticated user.

    Returned by the list terminals endpoint, each item represents an
    admin-configured terminal server that the current user has access to.
    """

    id: str
    """Unique identifier for the terminal server."""

    url: str
    """Base URL of the terminal server."""

    name: str
    """Display name of the terminal server."""

    model_config = ConfigDict(from_attributes=True)
