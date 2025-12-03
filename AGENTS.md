# Entire Project Instructions

This project aims to create a robust async Python client for the Open WebUI API that mirrors the backend structure of the main Open WebUI project.

## References
Access these references when looking up details of Open WebUI.

### API Reference
Located at `owui_client/refs/owui_openapi_main.json` is the full Open WebUI API spec.
Use this to lookup the descriptions of specific endpoints.
Unfortunately, there is no details on the possible parameters or returns in the Open API spec,
so it is incomplete, so you must look up the details in the backend source code to know
what parameters they accept, and what response fields they may return.

### Open WebUI Backend Source Code
Located in `owui_client/refs/owui_source_main/backend/open_webui` is the full Open WebUI backend source code.
Within that directory focus on:
- `/main.py` top level routers and entry point for the Open WebUI FastAPI app.
- `/routers/..` lower level routers describing specific endpoints/
- `/models/..` additional information and models providing details on the parameters and fields.

Always inspect the backend and locate both the models and the endpoint definitions before
working on related content - this ensures that your information is up to date, as Open WebUI changes often.


## VENV AND ENV
There is a .env file at the root of the project - you can't read it for security, but trust it is there!
There is also a .venv at the root of the project: Always use this .venv, never use system python.


## Architecture & Organization Rules

1.  **Mirror Backend Structure**:
    - The client structure must exactly match the Open WebUI backend source structure located in `owui_client/refs/owui_source_main/backend/open_webui`.
    - **Models**: If a Pydantic model is defined in `backend/open_webui/models/auths.py`, its client counterpart must reside in `owui_client/models/auths.py`.
    - **Routers/Resources**: If an endpoint is defined in `backend/open_webui/routers/auths.py`, the client resource class (e.g., `AuthsClient`) must reside in `owui_client/routers/auths.py`.

2.  **Client Assembly**:
    - `owui_client/client.py`: This is the main entry point. It defines the `OpenWebUI` class, which inherits from `OWUIClientBase`.
    - This main class is composed of sub-clients (Resources) that represent each router.
    - Example: `self.auths = AuthsClient(self)` inside `OpenWebUI.__init__`.

3.  **Base Classes**:
    - `OWUIClientBase` (in `owui_client/client_base.py`): Handles the low-level `_request` logic, authentication, and error parsing.
    - `ResourceBase` (in `owui_client/client_base.py`): The parent class for all router resources (e.g., `AuthsClient`). It delegates requests back to the main client.

4.  **Strict Naming**:
    - Maintain the same file names and roughly the same class/variable names as the backend to ensure easy navigation and updates.

5.  **Version Management**:
    - The version number is defined in `owui_client/pyproject.toml`.
    - It is also available at runtime via `owui_client.__version__` (defined in `owui_client/src/owui_client/__init__.py`).
    - **CRITICAL**: These two versions must ALWAYS be kept in sync. When bumping the version in `pyproject.toml`, you must also update `__init__.py`.

## Workflow

When adding support for a new set of endpoints (e.g., "Chats"):
1.  Locate the router in `owui_client/refs/.../routers/chats.py`.
2.  Locate the models in `owui_client/refs/.../models/chats.py` (or where they are defined).
3.  Recreate the models in `owui_client/models/chats.py`.
4.  Create the resource class `ChatsClient` in `owui_client/routers/chats.py`.
5.  Instantiate `self.chats = ChatsClient(self)` in `owui_client/client.py`.
6.  Create a test file `owui_client/tests/test_chats.py` and add at least one test case.

## Testing
We maintain a robust test suite in `owui_client/tests`. Remember to run the tests with the venv.

### Rules
1.  **Mirror Structure**: Create a corresponding test file for each major client module.
    - `owui_client/routers/auths.py` -> `owui_client/tests/test_auths.py`
2.  **Endpoint Coverage**: Every endpoint implemented in the client MUST have at least one test case in the corresponding test file.
3.  **Use Fixtures**: Use the `client` fixture (provided by `conftest.py`) which automatically handles the Docker container lifecycle. Do not spin up the server manually in individual tests.

### Testing with Mock Inference Provider
To test features that require an LLM connection (like Chat completions, Tool calling, etc.) without using real credentials:
1.  Use the `mock_openai_server` fixture in your test. This spins up a local HTTP server mimicking OpenAI.
2.  Configure the Open WebUI instance to use this mock server via `OpenAIClient`.
    ```python
    from owui_client.models.openai import OpenAIConfigForm

    async def test_with_mock_llm(client, mock_openai_server):
        # Configure OWUI to point to the mock server (running on host)
        new_config = OpenAIConfigForm(
            ENABLE_OPENAI_API=True,
            OPENAI_API_BASE_URLS=[mock_openai_server],
            OPENAI_API_KEYS=["sk-mock-key"],
            OPENAI_API_CONFIGS={"0": {"enable": True}}
        )
        await client.openai.update_config(new_config)
        
        # Now you can test endpoints that require LLM inference
    ```
3.  The mock server is available at `mock_openai_server` (which resolves to `http://host.docker.internal:PORT/v1` for the Docker container).

## Development Strategy
- **Progressive Implementation**: We are building endpoints progressively. Do not add new endpoints or routers unless explicitly requested. Start with the requested functionality and expand only when directed.
- **No Pre-Implementaitons**: Do not implement endpoints and models until they are required. For example, when starting a new set of endpoints on a new router, do not implement all models from those endpoints in advance. Implement each model, one by one, only as it is required to support the current endpoint being worked on.
