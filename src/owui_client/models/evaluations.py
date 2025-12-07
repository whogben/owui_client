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
    - id (str): Unique identifier for the arena model.
    - name (str): Display name of the arena model.
    - meta (dict): Metadata including profile image, description, and model filtering settings.
      - profile_image_url (str): URL to the model's profile image.
      - description (str, optional): Description of the model.
      - model_ids (list[str], optional): List of model IDs to include/exclude.
      - filter_mode (str, optional): 'include' or 'exclude' mode for model_ids.
      - access_control (dict, optional): Access control settings.
    """

