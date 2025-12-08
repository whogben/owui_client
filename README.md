# Unofficial Open WebUI Client

[**📚 Full Documentation**](https://whogben.github.io/owui_client/)

A robust, async Python client for the complete [Open WebUI](https://github.com/open-webui/open-webui) API.

This library mirrors the backend structure of Open WebUI, providing a fully typed, auto-completable interface for every endpoint.

> **Note**: This is the initial release (v1.0.0). While it covers the complete API, there may be edge cases or recent Open WebUI changes we haven't caught yet. Please report any issues you encounter!

## Installation

```bash
pip install owui-client
```

## Quick Start

```python
import asyncio
from owui_client import OpenWebUI

async def main():
    # Connect to your Open WebUI instance
    client = OpenWebUI(
        api_url="http://localhost:8080/api", 
        api_key="sk-..."
    )

    # Example: Get current user info
    user = await client.auths.get_session_user()
    print(f"Hello, {user.name}!")

    # Example: List all models
    models = await client.models.get_models()
    for model in models.data:
        print(model.id)

if __name__ == "__main__":
    asyncio.run(main())
```

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
