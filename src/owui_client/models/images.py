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
    """Additional parameters for OpenAI-compatible image generation API.

    Dict Fields:
        - `quality` (str, optional): Image quality - 'standard' or 'hd'
        - `style` (str, optional): Image style - 'vivid' or 'natural'
        - `user` (str, optional): Unique identifier representing the end-user
        - `response_format` (str, optional): Format of the response - 'url' or 'b64_json'
        - `size` (str, optional): Override size for this specific request (e.g., '1024x1024')
        - `n` (int, optional): Override number of images to generate for this request

    Additional keys may be supported depending on the OpenAI-compatible API implementation.
    """

    AUTOMATIC1111_BASE_URL: str
    """Base URL for Automatic1111 API."""

    AUTOMATIC1111_API_AUTH: Optional[Union[Dict, str]]
    """Authentication credentials for Automatic1111 API.

    Dict Fields:
        - `username` (str, required): Username for Automatic1111 API authentication
        - `password` (str, required): Password for Automatic1111 API authentication

    Can also be provided as a string in the format 'username:password'.
    When provided as a string, it will be converted to Basic Auth format.
    """

    AUTOMATIC1111_PARAMS: Optional[Union[Dict, str]]
    """Additional parameters for Automatic1111 API.

    Dict Fields:
        - `sampler_name` (str, optional): Sampler algorithm to use (e.g., 'euler', 'ddim', 'lms')
        - `scheduler` (str, optional): Scheduler type (e.g., 'normal', 'karras', 'exponential')
        - `cfg_scale` (float, optional): Classifier-free guidance scale (typically 7-15)
        - `denoising_strength` (float, optional): Denoising strength for img2img (0.0-1.0)
        - `seed` (int, optional): Random seed for reproducible results (-1 for random)
        - `subseed` (int, optional): Subseed for variation
        - `subseed_strength` (float, optional): Subseed strength (0.0-1.0)
        - `seed_resize_from_h` (int, optional): Seed resize from height
        - `seed_resize_from_w` (int, optional): Seed resize from width
        - `batch_size` (int, optional): Number of images to generate per prompt
        - `n_iter` (int, optional): Number of iterations/batches to run
        - `steps` (int, optional): Number of diffusion steps
        - `tiling` (bool, optional): Enable tiling for seamless textures
        - `restore_faces` (bool, optional): Enable face restoration
        - `enable_hr` (bool, optional): Enable high-resolution fix
        - `hr_scale` (float, optional): High-resolution scale factor
        - `hr_upscaler` (str, optional): High-resolution upscaler model
        - `hr_second_pass_steps` (int, optional): Steps for second high-res pass
        - `hr_resize_x` (int, optional): High-res resize width
        - `hr_resize_y` (int, optional): High-res resize height
        - `override_settings` (dict, optional): Additional settings to override
        - `script_name` (str, optional): Script name to use
        - `script_args` (list, optional): Arguments for the script
        - `eta` (float, optional): Eta noise multiplier for ancestral sampling
        - `s_churn` (float, optional): Stochasticity churn
        - `s_tmin` (float, optional): Minimum timestep
        - `s_tmax` (float, optional): Maximum timestep
        - `s_noise` (float, optional): Noise multiplier

    These parameters are passed directly to the Automatic1111 Stable Diffusion WebUI txt2img API.
    See https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API for full documentation.
    """

    COMFYUI_BASE_URL: str
    """Base URL for ComfyUI API."""

    COMFYUI_API_KEY: str
    """API key for ComfyUI API."""

    COMFYUI_WORKFLOW: str
    """ComfyUI workflow JSON string."""

    COMFYUI_WORKFLOW_NODES: List[Dict]
    """List of nodes in the ComfyUI workflow.

    Dict Fields:
        - `type` (str, required): Type of node (e.g., 'prompt', 'model', 'width', 'height', 'steps', 'seed')
        - `key` (str, required): Key/parameter name in the ComfyUI workflow
        - `node_ids` (list[str], required): List of node IDs that correspond to this type

    This defines the mapping between workflow parameters and their corresponding node IDs in the ComfyUI workflow.
    """

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
    """List of nodes in the ComfyUI image editing workflow.

    Dict Fields:
        - `type` (str, required): Type of node (e.g., 'image', 'prompt', 'model', 'width', 'height')
        - `key` (str, required): Parameter name/key in the ComfyUI workflow
        - `node_ids` (list[str], required): List of node IDs corresponding to this type
        - `value` (str, optional): Optional value for the node

    This defines the mapping between workflow parameters and their corresponding node IDs in the ComfyUI image editing workflow.
    """


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
