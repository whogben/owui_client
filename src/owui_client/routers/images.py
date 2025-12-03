from typing import List, Dict, Optional
from owui_client.client_base import ResourceBase
from owui_client.models.images import (
    ImagesConfig,
    CreateImageForm,
    EditImageForm,
)


class ImagesClient(ResourceBase):
    async def get_config(self) -> ImagesConfig:
        """
        Get the images configuration.

        :return: Images configuration
        """
        return await self._request(
            "GET",
            "/v1/images/config",
            model=ImagesConfig,
        )

    async def update_config(self, config: ImagesConfig) -> ImagesConfig:
        """
        Update the images configuration.

        :param config: The new configuration
        :return: The updated configuration
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

        :return: True if valid, raises Exception otherwise
        """
        return await self._request(
            "GET",
            "/v1/images/config/url/verify",
            model=bool,
        )

    async def get_models(self) -> List[Dict[str, str]]:
        """
        Get the list of available image models.

        :return: List of models (dictionaries with 'id' and 'name')
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
        Generate images.

        :param form_data: The image generation parameters
        :return: List of generated images (dictionaries with 'url')
        """
        return await self._request(
            "POST",
            "/v1/images/generations",
            model=dict,
            json=form_data.model_dump(),
        )

    async def edit_image(self, form_data: EditImageForm) -> List[Dict[str, str]]:
        """
        Edit an image.

        :param form_data: The image edit parameters
        :return: List of edited images (dictionaries with 'url')
        """
        return await self._request(
            "POST",
            "/v1/images/edit",
            model=dict,
            json=form_data.model_dump(),
        )

