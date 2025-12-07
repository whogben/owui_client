"""
Models for root/main endpoints.
"""

from pydantic import BaseModel

class UrlForm(BaseModel):
    """
    Form for updating the webhook URL.
    """
    url: str
    """The new webhook URL."""
