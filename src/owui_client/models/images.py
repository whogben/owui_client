"""
Pydantic models for the Images endpoints.
"""

from typing import Optional, List, Union, Dict, Any
from pydantic import BaseModel

class ImagesConfig(BaseModel):
    """
    Configuration for image generation and editing.
    """

    ENABLE_IMAGE_GENERATION: bool
    """Enable image generation features."""

    ENABLE_IMAGE_PROMPT_GENERATION: bool
    """Enable automatic prompt generation for images."""

    IMAGE_GENERATION_ENGINE: str
    """The engine to use for image generation. Options: 'openai', 'comfyui', 'automatic1111', 'gemini'."""

    IMAGE_GENERATION_MODEL: str
    """The model to use for image generation (e.g. 'dall-e-3', 'sd-xl')."""

    IMAGE_SIZE: Optional[str]
    """The default size for generated images (e.g. '512x512')."""

    IMAGE_STEPS: Optional[int]
    """The default number of steps for image generation (for engines that support it)."""

    IMAGES_OPENAI_API_BASE_URL: str
    """Base URL for OpenAI-compatible image generation API."""

    IMAGES_OPENAI_API_KEY: str
    """API key for OpenAI-compatible image generation API."""

    IMAGES_OPENAI_API_VERSION: str
    """API version for OpenAI-compatible image generation API."""

    IMAGES_OPENAI_API_PARAMS: Optional[Union[Dict, str]]
    """Additional parameters for OpenAI-compatible image generation API."""

    AUTOMATIC1111_BASE_URL: str
    """Base URL for Automatic1111 API."""

    AUTOMATIC1111_API_AUTH: Optional[Union[Dict, str]]
    """Authentication credentials for Automatic1111 API."""

    AUTOMATIC1111_PARAMS: Optional[Union[Dict, str]]
    """Additional parameters for Automatic1111 API."""

    COMFYUI_BASE_URL: str
    """Base URL for ComfyUI API."""

    COMFYUI_API_KEY: str
    """API key for ComfyUI API."""

    COMFYUI_WORKFLOW: str
    """ComfyUI workflow JSON string."""

    COMFYUI_WORKFLOW_NODES: List[Dict]
    """List of nodes in the ComfyUI workflow."""

    IMAGES_GEMINI_API_BASE_URL: str
    """Base URL for Google Gemini image generation API."""

    IMAGES_GEMINI_API_KEY: str
    """API key for Google Gemini image generation API."""

    IMAGES_GEMINI_ENDPOINT_METHOD: str
    """The method to use for Gemini image generation (e.g. 'predict', 'generateContent')."""

    ENABLE_IMAGE_EDIT: bool
    """Enable image editing features."""

    IMAGE_EDIT_ENGINE: str
    """The engine to use for image editing."""

    IMAGE_EDIT_MODEL: str
    """The model to use for image editing."""

    IMAGE_EDIT_SIZE: Optional[str]
    """The default size for edited images."""

    IMAGES_EDIT_OPENAI_API_BASE_URL: str
    """Base URL for OpenAI-compatible image editing API."""

    IMAGES_EDIT_OPENAI_API_KEY: str
    """API key for OpenAI-compatible image editing API."""

    IMAGES_EDIT_OPENAI_API_VERSION: str
    """API version for OpenAI-compatible image editing API."""

    IMAGES_EDIT_GEMINI_API_BASE_URL: str
    """Base URL for Google Gemini image editing API."""

    IMAGES_EDIT_GEMINI_API_KEY: str
    """API key for Google Gemini image editing API."""

    IMAGES_EDIT_COMFYUI_BASE_URL: str
    """Base URL for ComfyUI image editing API."""

    IMAGES_EDIT_COMFYUI_API_KEY: str
    """API key for ComfyUI image editing API."""

    IMAGES_EDIT_COMFYUI_WORKFLOW: str
    """ComfyUI workflow for image editing."""

    IMAGES_EDIT_COMFYUI_WORKFLOW_NODES: List[Dict]
    """List of nodes in the ComfyUI image editing workflow."""


class CreateImageForm(BaseModel):
    """
    Form for creating an image.
    """

    model: Optional[str] = None
    """The model to use for image generation. If not provided, the configured default model is used."""

    prompt: str
    """The prompt to generate the image from."""

    size: Optional[str] = None
    """The size of the generated image (e.g., '512x512'). If not provided, the configured default size is used."""

    n: int = 1
    """The number of images to generate."""

    negative_prompt: Optional[str] = None
    """The negative prompt to use for image generation (if supported by the engine)."""


GenerateImageForm = CreateImageForm  # Alias for backward compatibility


class EditImageForm(BaseModel):
    """
    Form for editing an image.
    """

    image: Union[str, List[str]]
    """Base64-encoded image(s) or URL(s) to edit."""

    prompt: str
    """The prompt to use for editing the image."""

    model: Optional[str] = None
    """The model to use for image editing. If not provided, the configured default model is used."""

    size: Optional[str] = None
    """The size of the edited image (e.g., '512x512'). If not provided, the configured default size is used."""

    n: Optional[int] = None
    """The number of images to generate."""

    negative_prompt: Optional[str] = None
    """The negative prompt to use for image editing (if supported by the engine)."""

