from typing import Optional
from pydantic import BaseModel, ConfigDict
from owui_client.models.users import UserResponse


class PromptModel(BaseModel):
    """
    Represents a prompt command.
    """
    model_config = ConfigDict(from_attributes=True)

    command: str
    """The command trigger (e.g., '/help'). Must start with a slash."""

    user_id: str
    """The ID of the user who created the prompt."""

    title: str
    """The title of the prompt."""

    content: str
    """The content of the prompt."""

    timestamp: int  # timestamp in epoch
    """Timestamp when the prompt was last updated (epoch time)."""

    access_control: Optional[dict] = None
    """
    Access control settings.
    
    - `None`: Public access, available to all users with the "user" role.
    - `{}`: Private access, restricted exclusively to the owner.
    - Custom permissions: Specific access control for reading and writing.
      Can specify group or user-level restrictions:
      ```json
      {
         "read": {
             "group_ids": ["group_id1", "group_id2"],
             "user_ids":  ["user_id1", "user_id2"]
         },
         "write": {
             "group_ids": ["group_id1", "group_id2"],
             "user_ids":  ["user_id1", "user_id2"]
         }
      }
      ```
    """


class PromptUserResponse(PromptModel):
    """
    Response model for a prompt including user details.
    """
    user: Optional[UserResponse] = None
    """Details of the user who created the prompt."""


class PromptForm(BaseModel):
    """
    Form for creating or updating a prompt.
    """
    command: str
    """The command trigger. Must start with a slash (e.g., '/help')."""

    title: str
    """The title of the prompt."""

    content: str
    """The content of the prompt."""

    access_control: Optional[dict] = None
    """
    Access control settings.
    
    - `None`: Public access, available to all users with the "user" role.
    - `{}`: Private access, restricted exclusively to the owner.
    - Custom permissions: Specific access control for reading and writing.
      Can specify group or user-level restrictions:
      ```json
      {
         "read": {
             "group_ids": ["group_id1", "group_id2"],
             "user_ids":  ["user_id1", "user_id2"]
         },
         "write": {
             "group_ids": ["group_id1", "group_id2"],
             "user_ids":  ["user_id1", "user_id2"]
         }
      }
      ```
    """
