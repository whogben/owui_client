# Unofficial Open WebUI API Documentation and Python Client

[**📚 Full Documentation Site**](https://whogben.github.io/owui_client/)

This project provides a robust, async **Python client** for the complete [Open WebUI](https://github.com/open-webui/open-webui) API, an **`owui-client` CLI** for common workflows (such as syncing local skill files into Open WebUI), and comprehensive unofficial **documentation** for the Open WebUI API.

## Python Client

A fully typed, async Python client that mirrors the backend structure of Open WebUI, providing an auto-completable interface for every endpoint.

### Target Open WebUI Version

This package currently targets Open WebUI `0.10.2` (derived from package version `10.2.1`).

Version mapping policy:
- `client.major` -> `openwebui.minor`
- `client.minor` -> `openwebui.patch`
- `client.patch` -> client-only fixes while targeting the same Open WebUI version

Example: `10.2.1` means this package targets Open WebUI `0.10.2`.

### Installation

```bash
pip install owui-client
```

### Quick Start

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

### Locating Endpoints

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
| | `client.events` | Event webhooks (outbound webhook delivery) |

*Tip: Use your IDE's autocomplete on the `client` object to explore all available resources.*

## Command-Line Interface

Installing the package also installs an `owui-client` console script for common workflows. Connection defaults come from the `OWUI_SERVER` and `OWUI_API_KEY` environment variables (see `example.env`), overridable with `--server` / `--api-key`.

```bash
# Sync a single local skill Markdown file (YAML frontmatter with name + description)
# into Open WebUI: creates if absent, updates if changed, no-op if unchanged.
owui-client sync-skill ./skills/summarizer.md

# Recursively sync every skill file under a directory (skill/SKILL.md or skill.md).
# Valid skills are created/updated/left unchanged; non-skill files are skipped; nothing is deleted.
owui-client sync-skills ./skills
```

`sync-skill` exposes `Shortcuts.sync_skill` (one file); `sync-skills` exposes `Shortcuts.sync_skills` (a whole directory). Both are one-way, idempotent upserts that never delete.

## API Documentation

The [documentation site](https://whogben.github.io/owui_client/) provides comprehensive coverage of all API endpoints, models, and their fields. This includes **detailed descriptions of every field of every model**, calculated automatically by examining their usage in the Open WebUI source code.

The field descriptions are extracted from:

- Type annotations and Pydantic model definitions
- Docstrings and comments in the source code
- Actual usage patterns found throughout the codebase
- API response examples and validation logic

This documentation is useful even if you're not using the Python client - it serves as a complete reference for the Open WebUI API, including all valid key/values accepted by dict fields.

## Changelog

Release notes: [Changelog on the documentation site](https://whogben.github.io/owui_client/changelog/) or [`CHANGELOG.md`](https://github.com/whogben/owui_client/blob/main/CHANGELOG.md) in the repository.

## Compatibility

This client is maintained for the explicitly targeted Open WebUI version shown above. Use the package version mapping to select the client release that matches your Open WebUI deployment.
