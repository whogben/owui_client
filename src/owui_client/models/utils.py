from pydantic import BaseModel

class CodeForm(BaseModel):
    """
    Form for code related operations.
    """

    code: str
    """
    The code content to be formatted or executed.
    """

class MarkdownForm(BaseModel):
    """
    Form for markdown to HTML conversion.
    """

    md: str
    """
    The markdown content to convert to HTML.
    """

# ChatForm in utils.py matches ChatTitleMessagesForm structure but is unused in the endpoint signature in the backend.
# The backend uses ChatTitleMessagesForm for the /pdf endpoint.
# We will define ChatForm here anyway to mirror the backend file content if needed, 
# but we'll rely on ChatTitleMessagesForm from models.chats for the endpoint.
class ChatForm(BaseModel):
    """
    Form structure for chat data, mirroring the backend definition.

    Note: The actual PDF endpoint uses `ChatTitleMessagesForm` from `models.chats`,
    but this class exists in the backend `utils.py` router file.
    """

    title: str
    """
    The title of the chat.
    """

    messages: list[dict]
    """
    The list of messages in the chat.
    """

