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
    - Versioning is compatibility-driven and follows the Open WebUI version we built/tested against:
        - `client.major` tracks `openwebui.minor`
        - `client.minor` tracks `openwebui.patch`
        - `client.patch` tracks client-only fixes/improvements made while targeting that same Open WebUI version
    - Example mapping:
        - Open WebUI `0.8.12` => client baseline `8.12.0`
        - A subsequent client fix while still targeting Open WebUI `0.8.12` => `8.12.1`
    - Do not auto-bump major/minor independently of the targeted Open WebUI version. Major/minor should change only when the targeted Open WebUI minor/patch changes.
    - When changing package version and/or target Open WebUI version, update `README.md` so the `Target Open WebUI Version` section explicitly states the currently targeted Open WebUI version and matching client version example.
    - When changing package version for a release, add a dated `## [version] - YYYY-MM-DD` section to `CHANGELOG.md` (see **Changelog** below).
    - Any version change is a release — always finish it by running **Release Readiness (Before Publishing)**.

### Changelog

- **Source of truth**: `CHANGELOG.md` at the repository root, in the spirit of [Keep a Changelog](https://keepachangelog.com/) (`[Unreleased]` plus one `## [version] - date` section per release).
- **Categories**: Use **Added**, **Changed**, **Fixed**, **Removed**, and **Deprecated** when they apply; skip empty sections.
- **Docs site**: The published changelog page is generated at MkDocs build time from `CHANGELOG.md` (`scripts/gen_ref_pages.py`); do not edit a separate copy for the site.
- **PyPI**: The `Changelog` URL in `pyproject.toml` points at the docs page; keep that in sync if the docs base URL ever changes.
- **GitHub Releases**: Optional but nice: when tagging a release, paste the same section into the GitHub release notes.

## Workflows

### Orchestrator Instructions

If you are the orchestrator/top-level agent (and only if you are the orchestrator/top-level agent):

1.  **Single Focus Subagents**:
    - Task each sub-agent with one focus only, so they will not mix context between tasks/goals.
    - When in doubt, task more sub-agents rather than fewer:
      It is better all sub-agents succeed easily, than some get overwhelmed.
    - Example: Instead of tasking a sub-agent to "run all tests and fix all problems",
      task a sub-agent to "run all tests and report issues",
      then look at the results, and task a sub-agent with "fix issue x",
      then another sub agent with "fix related issues y and z",
      then another sub agent with "run all tests"
2.  **Cleanup Pass after Buildouts / Major Debugging:**
    - If debugging gets extensive, task a sub-agent with a cleanup and polish pass to:
        - Remove unused branches / code that is no longer needed
        - Cleanup any temporary prints or comments from debugging
3.  **Review Pass at End**
    - After cleanup and tests are good, initiate review mode, using a review sub-agent to
      examine all changes since our last commit and surface any issues.
    - If issues are surfaced:
        - task sub-agents with investigating, issue by issue, to
            - confirm the issue's presence
            - study if the issue warrants solving (or if its a non issue because of how code flows in practice, etc)
        - Decide what issues to solve, and task sub-agents with solving them
        - Repeat this review step from beginning with a fresh review sub-agent.

### Updating for Latest Open WebUI

When the task is to update the client to support the latest Open WebUI version:
1.  Determine the latest current version of Open WebUI, and update our `package.toml` according to the pattern.
2.  Operate in this alphebtized loop, each time through:
    A. Task a sub-agent to run tests and report issues
        - If tests are failing, continue the alphabetized loop
        - If tests are all passing, move on to the next numbered step
    B. Select the next single issue (or closely related set of issues) to be resolved
    C. Task a sub-agent to resolve the issue
3.  Be flexible - sub agent can fail, you may need to task sub-agents to do research, and then gather additional context to task sub-agents that succeed.
4.  Before declaring the update done, run through **Release Readiness (Before Publishing)** below — do not wait to be asked.

### Release Readiness (Before Publishing)

"Publish-ready" means the artifacts, not just the source. A version bump or upgrade task is **not complete** until ALL of the following are done — run this checklist automatically at the end of any release/upgrade task, do not wait for the operator to ask for each step:

1.  **Version sync (all 5 points must agree):**
    - `pyproject.toml` `[project].version`
    - `src/owui_client/__init__.py` `__version__`
    - `README.md` (Target Open WebUI Version section mentions both the client version and the target OWUI version)
    - `CHANGELOG.md` has a `## [<version>] - YYYY-MM-DD` section
    - `refs/owui_source_main/package.json` is at the target Open WebUI version
    - `tests/test_versions.py` enforces these — run it and confirm green.
2.  **Tests green:** full `pytest tests/` passes with only the expected env-only `xfail`s (no new failures, no new unexpected `xpass`).
3.  **Zero drift:** `python scripts/check_drift.py` reports no drift.
4.  **Rebuild the docs site:** `mkdocs build --strict` succeeds with no warnings, and the built `docs/` is staged/committed (the docs site is checked into the repo, not built at publish time). Confirm the built pages reference the new version.
5.  **Clear and rebuild `dist/`** (it is gitignored, so it is NOT touched by commits and goes stale silently — this step is mandatory every release):
    ```bash
    source <root>/.venv/bin/activate
    rm -rf dist/*
    python -m build        # produces wheel + sdist in dist/
    ```
6.  **Verify the built artifacts** (don't assume the build is correct):
    - `dist/` contains exactly one `owui_client-<version>-py3-none-any.whl` and one `owui_client-<version>.tar.gz`, both at the new version.
    - Wheel `METADATA` reports the new version and the package name `owui-client`.
    - Spot-check the wheel contains any new modules added this release.
    - Install the wheel into a throwaway target and confirm `owui_client.__version__` == new version, the client imports, and any new resource (e.g. `client.events`) is wired.
7.  **Review pass:** a read-only reviewer has examined the diff against the backend source (and, for an upgrade, diffed the whole backend release range to confirm nothing was missed). Address or explicitly accept every finding.
8.  **Clean tree:** `git status` is clean (the commit is the release commit), `dist/` is gitignored (not committed), no stray containers/throwaway scripts left behind.

Only after all of the above is the release "good to go". The operator should then be able to publish with:
```bash
git push && git tag v<version> && git push origin v<version>
twine upload dist/owui_client-<version>-*
```

### Adding Endpoints

When adding support for a new set of endpoints (e.g., "Chats"):
1.  Locate the router in `owui_client/refs/.../routers/chats.py`.
2.  Locate the models in `owui_client/refs/.../models/chats.py` (or where they are defined).
3.  Examine the frontend and backend code to learn exactly what an endpoint does, what valid parameter values are, and what response values are expected.
4.  Recreate the models in `owui_client/models/chats.py` - adding a documentation comment for each model, and a description for each field.
5.  Create the resource class `ChatsClient` in `owui_client/routers/chats.py` - adding a documentation comment for each endpoint method.
6.  Instantiate `self.chats = ChatsClient(self)` in `owui_client/client.py`.
7.  Create a test file `owui_client/tests/test_chats.py` and add at least one test case.

## Documentation

The original Open WebUI API is incompletely documented, so it is neccesary to be a detective and research how and where a given endpoint and it's models are used, to determine what documentation to add to this client. It is critical to ground your understanding in the original source code, as there are many dict fields with undocumented key/value expectations, as well as fields that can be used in multiple ways.

Documentation is built using mkdocs using the configuration at `owui_client/mkdocs.yml`.

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

## Documenting Dictionary Attributes

Dictionary attributes accept arbitrary key-value pairs at runtime, making them unusable without documentation. Every public dictionary attribute MUST have a `Dict Fields:` section in its docstring. This is enforced by the test suite.

### Pattern 1: Inline Field Documentation

Document all keys when the dictionary structure is defined by your API:

\`\`\`python
metadata: dict[str, Any]
"""Configuration metadata for the request.

Dict Fields:
    - `temperature` (float, optional): Sampling temperature between 0.0 and 2.0
    - `max_tokens` (int, required): Maximum number of tokens to generate
    - `model` (str, required): Model identifier like 'gpt-4' or 'claude-3'
    - `stream` (bool, optional): Enable streaming responses, defaults to False
"""
\`\`\`

**Format requirements:**
- Use `Dict Fields:` as the section header
- **No blank line** between `Dict Fields:` and first field
- Start each field with `-` (dash) for markdown bullet list
- Indent with 4 spaces, then dash, then space
- Wrap field names in backticks: \`field_name\`
- List type in parentheses: `(float, optional)` or `(str, required)`

### Pattern 2: External Reference Documentation

Document the reference when the dictionary is passed to another API:

```python
openai_params: dict[str, Any]
"""Parameters passed directly to the OpenAI API.

Dict Fields:
    This dictionary is forwarded to the OpenAI Chat Completion API without
    modification. See [OpenAI API Reference](https://platform.openai.com/docs)
    for valid keys and their descriptions.
"""
```

Or for internal references:

```python
filter_config: dict[str, Any]
"""Filter configuration options.

Dict Fields:
    Valid keys defined by FilterOptions model in backend. See
    owui_client/refs/owui_source_main/backend/open_webui/models/filters.py
"""
```

### Research Process

Research the **REFERENCE Open WebUI source code** in `owui_client/refs/` (NOT our client code):

1. **Backend reference** (`owui_client/refs/owui_source_main/backend/open_webui/`)
   - Find where attribute is used in routers and models
   - Check what keys are set, read, or validated

2. **Frontend reference** (`owui_client/refs/owui_source_main/src/`)
   - Find TypeScript interfaces or component usage
   - Look in `/lib/apis` and `/routes` directories

3. **Document findings**
   - List every key discovered in reference source
   - Mark required/optional based on usage patterns
   - Note any special behaviors or gotchas

If you cannot find complete information, document what you found and note gaps:

```python
settings: dict[str, Any]
"""User settings dictionary.

Dict Fields:
    theme (str, optional): UI theme - 'light' or 'dark'
    language (str, optional): Language code like 'en', 'es'
    
    Additional keys may exist. Backend validation not found in reference code.
"""
```

### Enforcement

The test suite checks all dictionary attributes for `Dict Fields:` sections. Tests fail if any dict attribute lacks this documentation. Every model update must include proper dict documentation.


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