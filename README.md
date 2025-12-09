# Unofficial Open WebUI API Documentation

This is **unofficial documentation** for the Open WebUI API in general. It provides comprehensive coverage of all API endpoints, models, and their fields.

## What's Included

This documentation includes **detailed descriptions of every field of every model**, calculated automatically by examining their usage in the Open WebUI source code. The field descriptions are extracted from:

- Type annotations and Pydantic model definitions
- Docstrings and comments in the source code
- Actual usage patterns found throughout the codebase
- API response examples and validation logic

## Python Client Library

While this documentation is API-focused and language-agnostic, it is generated from the [owui-client](https://github.com/whogben/owui_client) Python library, which provides a fully typed, async interface to the Open WebUI API.

### Installation

```bash
pip install owui-client
```

### Quick Start

```python
import asyncio
from owui_client import OpenWebUI

async def main():
    client = OpenWebUI(
        api_url="http://localhost:8080/api", 
        api_key="sk-..."
    )
    
    # Get current user info
    user = await client.auths.get_session_user()
    print(f"Hello, {user.name}!")

if __name__ == "__main__":
    asyncio.run(main())
```

## Documentation Structure

- **Code Reference**: Browse all models, routers, and client classes with complete field descriptions
- **Models**: Every Pydantic model with detailed field documentation
- **Routers**: All API endpoints organized by resource type

## Note

This documentation is maintained independently and may not always reflect the latest changes in Open WebUI. For the official Open WebUI documentation, please visit the [Open WebUI repository](https://github.com/open-webui/open-webui).

## Locating Endpoints

The client structure matches the Open WebUI backend router structure exactly. If you know the API endpoint or backend path, you know the client function.

| API Group | Client Attribute | Description |
| :--- | :--- | :--- |
| **Auth & Users** | `client.auths` | Sign in/up, API keys, session management |
| | `client.users` | User management, permissions, settings |
| | `client.groups` | Group management |
| **Content** | `client.chats` | Chat history, messages, archiving |
| | `client.prompts` | Prompt management |
| | `client.files` | File uploads and management |
| | `client.knowledge`| Knowledge base operations |
| **Inference** | `client.openai` | OpenAI-compatible chat completions & config |
| | `client.ollama` | Ollama configuration & endpoints |
| | `client.images` | Image generation endpoints |
| | `client.audio` | TTS and STT endpoints |
| **System** | `client.configs` | Global system configurations |
| | `client.models` | Model management (delete, update, import) |
| | `client.tools` | Tool management |
| | `client.functions`| Function management |

*Tip: Use your IDE's autocomplete on the `client` object to explore all available resources.*
