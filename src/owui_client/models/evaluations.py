from typing import Optional
from pydantic import BaseModel


class UpdateConfigForm(BaseModel):
    """
    Configuration form for updating evaluation settings.
    """

    ENABLE_EVALUATION_ARENA_MODELS: Optional[bool] = None
    """
    Enable or disable the evaluation arena models feature.
    """

    EVALUATION_ARENA_MODELS: Optional[list[dict]] = None
    """
    List of evaluation arena models configuration.
    Each item is a dictionary with the following structure:

    Dict Fields:
        - `id` (str, required): Unique identifier for the arena model. Generated from the name field (lowercase, hyphen-separated) when creating new models. Must be unique across all arena models.
        - `name` (str, required): Display name of the arena model. Must be unique and is used to generate the ID if not provided.
        - `meta` (dict, required): Metadata including profile image, description, and model filtering settings.

    The `meta` dictionary contains:
        - `profile_image_url` (str, required): URL to the model's profile image. Defaults to '/favicon.png' if not specified.
        - `description` (str, optional): Description of the model. Can be null or empty string.
        - `model_ids` (list[str], optional): List of model IDs to include or exclude. When empty, null, or not specified, includes all available models.
        - `filter_mode` (str, optional): Filter mode for model_ids. Values: 'include' (default) or 'exclude'. Only used when model_ids is specified and non-empty.
        - `access_control` (dict, optional): Access control settings for the arena model. Follows the standard AccessControl component structure. Can be empty dict {}.

    Additional Notes:
    - When ENABLE_EVALUATION_ARENA_MODELS is True but EVALUATION_ARENA_MODELS is empty or null, a default arena model with ID 'arena-model' and name 'Arena Model' is automatically created with all models included.
    - The backend processes these models to create arena model entries with special flags: 'owned_by': 'arena' and 'arena': True.
    - Arena models are treated as virtual models that appear in the model list alongside regular models but are marked as owned by the arena system.
    - Access control settings follow the same structure as the AccessControl component used in the frontend for workspace and model access management.
    - The ID generation algorithm: lowercase the name, replace non-alphanumeric characters with hyphens, collapse multiple hyphens, and remove leading/trailing hyphens.
    """
