"""
Client for the Images endpoints.
"""

from typing import List, Dict, Optional
from owui_client.client_base import ResourceBase
from owui_client.models.images import (
    ImagesConfig,
    CreateImageForm,
    EditImageForm,
)


class ImagesClient(ResourceBase):
    """
    Client for the Images endpoints.
    """

    async def get_config(self) -> ImagesConfig:
        """
        Get the images configuration.

        Returns:
            ImagesConfig: The current images configuration.
        """
        return await self._request(
            "GET",
            "/v1/images/config",
            model=ImagesConfig,
        )

    async def update_config(self, config: ImagesConfig) -> ImagesConfig:
        """
        Update the images configuration.

        Args:
            config: The new configuration.

        Returns:
            ImagesConfig: The updated configuration.
        """
        return await self._request(
            "POST",
            "/v1/images/config/update",
            model=ImagesConfig,
            json=config.model_dump(),
        )

    async def verify_url(self) -> bool:
        """
        Verify the image generation URL (for Automatic1111 or ComfyUI).

        Returns:
            bool: True if the URL is valid.
        """
        return await self._request(
            "GET",
            "/v1/images/config/url/verify",
            model=bool,
        )

    async def get_models(self) -> List[Dict[str, str]]:
        """
        Get the list of available image models.

        Returns:
            List[Dict[str, str]]: List of models (dictionaries with 'id' and 'name').
        """
        # The backend returns a list of dicts, but not a specific Pydantic model for the list items in the response type signature
        # We can use dict as the model, and _request will handle the list
        return await self._request(
            "GET",
            "/v1/images/models",
            model=dict,
        )

    async def generate_image(self, form_data: CreateImageForm) -> List[Dict[str, str]]:
        """
        Generate images based on the provided parameters.

        Args:
            form_data: The image generation parameters.

        Returns:
            List[Dict[str, str]]: List of generated images (dictionaries with 'url').
        """
        return await self._request(
            "POST",
            "/v1/images/generations",
            model=dict,
            json=form_data.model_dump(),
        )

    async def edit_image(self, form_data: EditImageForm) -> List[Dict[str, str]]:
        """
        Edit an image based on the provided parameters.

        Args:
            form_data: The image edit parameters.

        Returns:
            List[Dict[str, str]]: List of edited images (dictionaries with 'url').
        """
        return await self._request(
            "POST",
            "/v1/images/edit",
            model=dict,
            json=form_data.model_dump(),
        )

