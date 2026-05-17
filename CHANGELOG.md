# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Package version numbers follow the Open WebUI mapping described in the README (they are not independent SemVer).

## [Unreleased]

## [9.5.0] - 2026-05-16

### Changed

- Updated target Open WebUI version from 0.8.10 to 0.9.5.
- Updated reference source (`refs/owui_source_main/`) to Open WebUI 0.9.5 (commit 3660bc00f).
- `FunctionUserResponse` now inherits from `FunctionResponse` instead of `FunctionModel` (matches backend).
- `FunctionUserResponse.user` field type changed from `Optional[UserModel]` to `Optional[UserResponse]`.
- `retrieval.get_status()` now calls `GET /v1/retrieval/config` instead of the old `GET /v1/retrieval/` endpoint.

### Added

#### Models - New Fields

- `AdminConfig`: `ENABLE_AUTOMATIONS`, `AUTOMATION_MAX_COUNT`, `ENABLE_CALENDAR`, `AUTOMATION_MIN_INTERVAL`
- `ChatModel`: `last_read_at`, `tasks`, `summary`
- `ChatResponse`: `tasks`, `summary`
- `ChatTitleIdResponse`: `last_read_at`
- `ConfigForm` (retrieval): `PADDLEOCR_VL_TOKEN`, `PADDLEOCR_VL_BASE_URL`, `RAG_RERANKING_BATCH_SIZE`
- `FeaturesPermissions`: `calendar`, `automations`
- `NoteModel`: `is_pinned`
- `NoteItemResponse`: `is_pinned`
- `OAuthClientRegistrationForm`: `client_secret`, `oauth_server_url`
- `STTConfigForm`: `ALLOWED_EXTENSIONS`
- `SharingPermissions`: `public_chats`, `public_calendars`
- `TaskConfigForm`: `ENABLE_VOICE_MODE_PROMPT`
- `TerminalServerConnection`: `policy`, `server_type`, `policy_id`
- `TTSConfigForm`: `MISTRAL_API_BASE_URL`, `MISTRAL_API_KEY`
- `ToolServerConnection`: `info`
- `WebConfig`: `WEB_FETCH_MAX_CONTENT_LENGTH`, `BRAVE_SEARCH_CONTEXT_TOKENS`

#### Models - New Classes

- `ChatAccessGrantsForm` (chats)
- `TerminalServerPolicyForm` (configs)

#### Routers - New Endpoints

- `AuthsClient.delete_oauth_session()` - `DELETE /v1/auths/oauth/sessions/{provider}`
- `ChatsClient.update_shared_chat_access()` - `POST /v1/chats/shared/{id}/access/update`
- `ChatsClient.get_shared_chat_access()` - `GET /v1/chats/shared/{id}/access`
- `ConfigsClient.verify_terminal_server()` - `POST /v1/configs/terminal_servers/verify`
- `ConfigsClient.put_terminal_server_policy()` - `POST /v1/configs/terminal_servers/policy`
- `ConfigsClient.get_models_defaults()` - `GET /v1/configs/models/defaults`
- `EvaluationsClient.get_feedback_model_ids()` - `GET /v1/evaluations/feedbacks/models`
- `ModelsClient.unload_model()` - `POST /api/models/unload`
- `NotesClient.get_pinned_notes()` - `GET /v1/notes/pinned`
- `NotesClient.pin_note_by_id()` - `POST /v1/notes/{id}/pin`
- `OllamaClient.generate_anthropic_messages()` - `POST /ollama/v1/messages[/{url_idx}]`
- `OllamaClient.generate_responses()` - `POST /ollama/v1/responses[/{url_idx}]`
- `TasksClient.stop_tasks_by_chat_api()` - `POST /api/tasks/chat/{chat_id}/stop`

#### Routers - New Modules

- **Skills router** (`client.skills`) — 9 endpoints for skill CRUD, access management, and listing
- **Analytics router** (`client.analytics`) — 8 read-only admin endpoints for message counts, token usage, daily stats, and model overview
- **Automations router** (`client.automations`) — 8 endpoints for scheduled automation CRUD, toggle, run, and run history
- **Calendar router** (`client.calendar`) — 13 endpoints for calendar and event CRUD, RSVP, search, and default calendar management
- **Terminals router** (`client.terminals`) — 2 HTTP endpoints for listing terminal servers and proxying requests (WebSocket proxy not supported)

## [8.10.0] - 2026-04-15

### Changed

- Adopted Open-WebUI-aligned versioning: `client.major` / `client.minor` map to Open WebUI `0.{minor}.{patch}`; `client.patch` is for client-only fixes while targeting the same Open WebUI release. Baseline is now **8.10.0** for Open WebUI **0.8.10** (supersedes prior 1.6.x-style numbering).
- README: explicit target Open WebUI version, mapping rules, and compatibility guidance tied to that target instead of “latest”.
- `tests/conftest.py`: Docker Open WebUI image for session tests is selected from `pyproject.toml` using the same mapping.
- `AGENTS.md`: orchestrator and update workflows, clearer versioning rules, and documentation expectations.

### Added

- `tests/versioning.py` and `tests/test_versions.py` to encode and test the version mapping.
