from typing import Optional
from pydantic import BaseModel

class TaskConfigForm(BaseModel):
    """
    Configuration form for task-related settings (e.g. title generation, tags, autocomplete).
    """

    TASK_MODEL: Optional[str]
    """The model ID to use for performing tasks. If not specified, a default model may be used."""

    TASK_MODEL_EXTERNAL: Optional[str]
    """The external model ID to use for performing tasks, if configured."""

    ENABLE_TITLE_GENERATION: bool
    """Whether to enable automatic title generation for chats."""

    TITLE_GENERATION_PROMPT_TEMPLATE: str
    """The prompt template used for generating chat titles."""

    IMAGE_PROMPT_GENERATION_PROMPT_TEMPLATE: str
    """The prompt template used for generating image prompts."""

    ENABLE_AUTOCOMPLETE_GENERATION: bool
    """Whether to enable text autocompletion generation."""

    AUTOCOMPLETE_GENERATION_INPUT_MAX_LENGTH: int
    """The maximum length of the input text context to consider for autocompletion."""

    TAGS_GENERATION_PROMPT_TEMPLATE: str
    """The prompt template used for generating chat tags."""

    FOLLOW_UP_GENERATION_PROMPT_TEMPLATE: str
    """The prompt template used for generating follow-up questions/suggestions."""

    ENABLE_FOLLOW_UP_GENERATION: bool
    """Whether to enable the generation of follow-up questions."""

    ENABLE_TAGS_GENERATION: bool
    """Whether to enable the generation of tags for chats."""

    ENABLE_SEARCH_QUERY_GENERATION: bool
    """Whether to enable the generation of search queries (for web search)."""

    ENABLE_RETRIEVAL_QUERY_GENERATION: bool
    """Whether to enable the generation of retrieval queries (for RAG)."""

    QUERY_GENERATION_PROMPT_TEMPLATE: str
    """The prompt template used for generating queries (search or retrieval)."""

    TOOLS_FUNCTION_CALLING_PROMPT_TEMPLATE: str
    """The prompt template used for tool/function calling."""

    VOICE_MODE_PROMPT_TEMPLATE: Optional[str]
    """The prompt template used for voice mode interactions."""

