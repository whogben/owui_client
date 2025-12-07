from pydantic import BaseModel

class AddPipelineForm(BaseModel):
    """
    Form for adding a new pipeline via URL.
    """
    url: str
    """The URL of the pipeline file to download (e.g., a GitHub Raw URL)."""
    urlIdx: int
    """The index of the OpenAI API base URL configuration to use for this pipeline."""

class DeletePipelineForm(BaseModel):
    """
    Form for deleting an existing pipeline.
    """
    id: str
    """The unique identifier of the pipeline to delete."""
    urlIdx: int
    """The index of the OpenAI API base URL configuration where the pipeline resides."""

