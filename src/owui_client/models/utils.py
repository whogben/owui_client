from pydantic import BaseModel

class CodeForm(BaseModel):
    code: str

class MarkdownForm(BaseModel):
    md: str

# ChatForm in utils.py matches ChatTitleMessagesForm structure but is unused in the endpoint signature in the backend.
# The backend uses ChatTitleMessagesForm for the /pdf endpoint.
# We will define ChatForm here anyway to mirror the backend file content if needed, 
# but we'll rely on ChatTitleMessagesForm from models.chats for the endpoint.
class ChatForm(BaseModel):
    title: str
    messages: list[dict]

