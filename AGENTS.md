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

### Open WebUI Frontend Source Code
Located in `owui_client/refs/owui_source_main/src` is the full Open WebUI frontend source code.
While we are not directly replicating anything from the frontend, it is often necesary to examine how the frontend uses a given model or endpoint to learn what parameter values are valid. Utilize the frontend code when you are researching to document a model or endpoint.
- `/routes/..`
- `/lib/apis..`
- `/lib/components` 

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
3.  Examine the frontend and backend code to learn exactly what an endpoint does, what valid parameter values are, and what response values are expected.
4.  Recreate the models in `owui_client/models/chats.py` - adding a documentation comment for each model, and a description for each field.
5.  Create the resource class `ChatsClient` in `owui_client/routers/chats.py` - adding a documentation comment for each endpoint method.
6.  Instantiate `self.chats = ChatsClient(self)` in `owui_client/client.py`.
7.  Create a test file `owui_client/tests/test_chats.py` and add at least one test case.

## Documentation

The original Open WebUI source code is undocumented, so it is neccesary to be a detective and research how and where a given endpoint and it's models are used, to determine what documentation to add to this client. It is critical to ground your understanding in the original source code, as there are many dict fields with undocumented key/value expectations, as well as fields that can be used in multiple ways.

The final documentation will be built from the source code using MkDocs and the following configuration:
- `show_source: true` (will add ability for end reader to quickly see related source code)
- `signature_crossrefs: true` (will add an automatic "Used by" and "Returned by" to model classes)
- `show_root_heading: false` (will prevent redundant module names appearing at start of class names)
- `members_order: source` (will maintain original field order)

Notes for all documentation:
- You can use backticks to reference one doc from another, such as "This uses `MyClass.my_method` for processing."
- You can use markdown, but use it sparingly.
- Never use emojis.
- Be CONCISE. These docstrings will be fed into AI later when it interacts with the API, so they must be short and precise - we don't want to waste tokens.

Documentation Process Always Goes Like This:
1. Locate EVERY reference and usage of the original endpoint/class in the backend source code.
2. Locate EVERY reference and usage of the original endpoint/class in the frontend source code.
3. Stop, analyze, did you find *every* reference in both frontend and backend? If not, go back and find more - we cannot risk even a single missing reference, because that reference may have an assumption about field values, or a side effect that must be documented.

### Documenting Modules

Every module must have a simple dosctring introducing it such as:

```python
"""Brief module description.

More detailed explanation if needed. Supports Markdown formatting.
"""
```

### Documenting Model Classes

Every model class must have a docstring describing it sufficient that an AI could generate a valid model (when combined with the field descriptions).

```python
class MyClass:
    """Brief class description.
    
    Longer explanation with **Markdown** support. Include any interactions between fields, like "if field X is present, field Y must have value Z". If the model has multiple uses or configurations, note these too.
    """
```

### Documenting Model Attributes

Most user-facing attribute in a model class must have a type and a docstring sufficient that an AI could generate valid values for it. The only exception is when a field is completely obvious in context, has no side effects, and can only be interpreted one way, such as `is_admin: bool` or `chat_id:str`. Otherwise, every attribute must have a docstring.

```python
class Something(BaseModel):
    someattr:sometype
    """Description, including details on any key and/or value expectations, what is valid, etc. Supports Markdown formatting."""

    someotherattr:someothertype
    """Description, including details on any key and/or value expectations, what is valid, etc. Supports Markdown formatting."""
```

This is the most difficult part of the documentation process, and requires deep understanding and analysis of the original source code - tracing where and how the models are used.
 Do not rush this, as any mistake here will have downstream consequences for all following developers. If after several attempts you are unable to fully trace and understand how a given model or field is used, stop and alert the human operator rather than continuing to work.

Note that if there are gotchas regarding the interactions between attributes, theses should be added to the model class docstring, not the separate attribute docstrings.


### Documenting Resource Classes

Every resource class must have a simple docstring introducing it such as:

```python
"""
Client for the Auths endpoints.
"""
```

### Documenting Endpoint Methods

Every endpoint method must have a docstring describing it sufficient that an AI will understand what it does, when and how to use it, and what to expect in return.

```python
def my_function(param1: str, param2: int) -> bool:
    """Brief description of what this does.
    
    More detailed explanation if needed, such as any special notes, unique uses of model fields for this particular endpoint, how it fits with other endpoints, what side effects it has, etc.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        SomeError: When something bad happens
    
    Examples: (only included it relevant):
    ```python
    < some use example code >
    ```

    """
```

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
- **No Pre-Implementations**: Do not implement endpoints and models until they are required. For example, when starting a new set of endpoints on a new router, do not implement all models from those endpoints in advance. Implement each model, one by one, only as it is required to support the current endpoint being worked on.
- **Update Documentation**: Whenever we make changes to an endpoint, or model, or discover new unexpected test failures - revise the documentation, doing fresh research into the source code as it may have changed. It is imperative that the documentation is accurate and up to date.