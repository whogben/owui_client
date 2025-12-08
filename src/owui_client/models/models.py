from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict
from owui_client.models.users import UserResponse


# ModelParams is a model for the data stored in the params field of the Model table
class ModelParams(BaseModel):
    """
    Model parameters configuration.
    Allows extra fields to store various model-specific parameters.

    Common parameters include:
    - `system`: System prompt string.
    - `stop`: List of stop sequences.
    """

    model_config = ConfigDict(extra="allow")


class ModelCapabilities(BaseModel):
    """
    Model capabilities configuration.
    """

    vision: Optional[bool] = True
    """Model accepts image inputs."""

    file_upload: Optional[bool] = True
    """Model accepts file inputs."""

    web_search: Optional[bool] = True
    """Model can search the web for information."""

    image_generation: Optional[bool] = True
    """Model can generate images based on text prompts."""

    code_interpreter: Optional[bool] = True
    """Model can execute code and perform calculations."""

    usage: Optional[bool] = None
    """
    Sends `stream_options: { include_usage: true }` in the request.
    Supported providers will return token usage information in the response when set.
    """

    citations: Optional[bool] = True
    """Displays citations in the response."""

    status_updates: Optional[bool] = True
    """Displays status updates (e.g., web search progress) in the response."""


# ModelMeta is a model for the data stored in the meta field of the Model table
class ModelMeta(BaseModel):
    """
    Metadata for a model.

    Additional fields often used (via extra="allow"):
    - `knowledge` (list): List of knowledge collection items.
    - `toolIds` (list[str]): List of tool IDs enabled for this model.
    - `filterIds` (list[str]): List of filter IDs enabled.
    - `defaultFilterIds` (list[str]): List of default filter IDs.
    - `actionIds` (list[str]): List of action IDs.
    - `defaultFeatureIds` (list[str]): List of default feature IDs.
    - `suggestion_prompts` (list): List of suggestion prompts.
    - `tags` (list): List of tags associated with the model.
    """

    profile_image_url: Optional[str] = "/static/favicon.png"
    """
    URL of the model's profile image.
    """

    description: Optional[str] = None
    """
    User-facing description of the model.
    """

    capabilities: Optional[ModelCapabilities] = None
    """
    Dictionary of model capabilities (e.g., vision, usage).
    """

    model_config = ConfigDict(extra="allow")


class ModelModel(BaseModel):
    """
    Model representing an AI model configuration.
    """

    id: str
    """
    Unique identifier for the model.
    """

    user_id: str
    """
    ID of the user who owns the model.
    """

    base_model_id: Optional[str] = None
    """
    ID of the base model this model is derived from (if any).
    """

    name: str
    """
    Display name of the model.
    """

    params: ModelParams
    """
    Model parameters.
    """

    meta: ModelMeta
    """
    Model metadata.
    """

    access_control: Optional[dict] = None
    """
    Access control settings for the model.
    
    Structure:
    - `None`: Public access, available to all users with the "user" role.
    - `{}`: Private access, restricted exclusively to the owner.
    - Custom permissions:
        ```json
        {
            "read": {
                "group_ids": ["group_id1"],
                "user_ids": ["user_id1"]
            },
            "write": {
                "group_ids": ["group_id2"],
                "user_ids": ["user_id2"]
            }
        }
        ```
    """

    is_active: bool
    """
    Whether the model is currently active.
    """

    updated_at: int  # timestamp in epoch
    """
    Timestamp when the model was last updated (epoch time).
    """

    created_at: int  # timestamp in epoch
    """
    Timestamp when the model was created (epoch time).
    """

    model_config = ConfigDict(from_attributes=True)


class ModelUserResponse(ModelModel):
    """
    Response model for a model including user details.
    """

    user: Optional[UserResponse] = None
    """
    Details of the user who owns the model.
    """


class ModelResponse(ModelModel):
    """
    Response model for model details (alias for `ModelModel`).
    """

    pass


class ModelListResponse(BaseModel):
    """
    Response model for a list of models with pagination info.
    """

    items: list[ModelUserResponse]
    """
    List of models with user details.
    """

    total: int
    """
    Total number of models found.
    """


class ModelForm(BaseModel):
    """
    Form for creating or updating a model.
    """

    id: str
    """
    Unique identifier for the model.
    """

    base_model_id: Optional[str] = None
    """
    ID of the base model.
    """

    name: str
    """
    Display name of the model.
    """

    meta: ModelMeta
    """
    Model metadata.
    """

    params: ModelParams
    """
    Model parameters.
    """

    access_control: Optional[dict] = None
    """
    Access control settings.
    
    Structure:
    - `None`: Public access, available to all users with the "user" role.
    - `{}`: Private access, restricted exclusively to the owner.
    - Custom permissions:
        ```json
        {
            "read": {
                "group_ids": ["group_id1"],
                "user_ids": ["user_id1"]
            },
            "write": {
                "group_ids": ["group_id2"],
                "user_ids": ["user_id2"]
            }
        }
        ```
    """

    is_active: bool = True
    """
    Whether the model is active.
    """


class ModelIdForm(BaseModel):
    """
    Form containing just a model ID.
    """

    id: str
    """
    The model ID.
    """


class ModelsImportForm(BaseModel):
    """
    Form for importing models.
    """

    models: list[dict]
    """
    List of model data dictionaries to import.
    """


class SyncModelsForm(BaseModel):
    """
    Form for syncing models.
    """

    models: list[ModelModel] = []
    """
    List of models to sync.
    """
