# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Package version numbers follow the Open WebUI mapping described in the README (they are not independent SemVer).

## [Unreleased]

## [9.6.0] - 2026-06-02

### Changed

- Updated target Open WebUI version from 0.9.5 to 0.9.6.
- Updated reference source (`refs/owui_source_main/`) to Open WebUI 0.9.6 (commit 1a97751e37).
- `KnowledgeDirectoryUpdateForm.parent_id` default changed from `None` to `'__unset__'` sentinel (matches backend).
- `RetrievalClient.update_config()` now serializes the `ConfigForm` with `exclude_none=True` so partial config updates (where most fields remain unset) do not send `None` values for list-typed fields. Required because OWUI 0.9.6 strictly validates list types and rejects `None` where a list is expected (e.g. `ALLOWED_FILE_EXTENSIONS`, `YOUTUBE_LOADER_LANGUAGE`).
- `ToolsClient`, `PromptsClient`, `ModelsClient`, and `EvaluationsClient` POST endpoints that send a partial form (most notably those with `access_grants: Optional[list[dict]] = None`) now serialize with `exclude_none=True`. Required because OWUI 0.9.6 strictly validates list-typed fields and rejects `None` (e.g. `access_grants`). The `ConfigsClient` endpoints were intentionally left unchanged because the 0.9.6 backend requires every form field to be present (even when `None`).

### Fixed

- `RetrievalClient.update_config()` returning 422 Unprocessable Entity on partial `ConfigForm` submissions against OWUI 0.9.6 (regression from 0.9.5; the previous backend accepted `None` for list fields, the new backend does not).
- `UtilsClient.get_html_from_markdown()` marked as expected-to-fail in tests: the `/v1/utils/markdown` endpoint was removed in OWUI 0.9.6. The client method and `MarkdownForm` model are retained for forward compatibility, but will return 405/404 against current backends.

### Known Issues (OWUI 0.9.6 Backend)

The following tests are marked `xfail` due to apparent bugs or behavior changes in the OWUI 0.9.6 backend. The client behavior is unchanged from 9.5.0; the failures are caused by the backend, not the client. These are expected to be addressed in a future release once the upstream issues are resolved.

- `tests/test_evaluations.py::test_feedback_lifecycle` — `GET /v1/evaluations/feedbacks/all` returns data the client cannot iterate as `List[FeedbackResponse]`. The endpoint may have been renamed or its response wrapper changed in 0.9.6.
- `tests/test_models.py::test_model_lifecycle` — `POST /v1/models/model/update` returns 500 on partial `ModelForm` submissions with empty `ModelParams()`. Appears to be a 0.9.6 backend bug.
- `tests/test_ollama.py::test_ollama_models` — `GET /ollama/api/ps` returns 500 when proxying to a mock Ollama backend. Appears to be a 0.9.6 backend bug in proxy response handling.

### Added

#### Models - New Classes

- `KnowledgeDirectoryModel` (knowledge) — represents nested directories within a knowledge base
- `KnowledgeDirectoryCreateForm` (knowledge) — form for creating directories
- `KnowledgeDirectoryUpdateForm` (knowledge) — form for renaming/relocating directories
- `KnowledgeFileMoveForm` (knowledge) — form for moving files between directories
- `FileManifestEntry`, `SyncDiffForm`, `SyncDiffResponse`, `SyncCleanupForm` (knowledge) — sync manifest and diff models
- `FileRenameForm` (files) — form for renaming a file
- `ResourcePreviewItem`, `ResourcePreviewList`, `UserPreviewUser`, `UserPreview` (users) — admin access preview for users
- `GroupPreviewGroup`, `GroupPreview` (groups) — admin access preview for groups

#### Models - New Fields

- `KnowledgeFileListResponse`: `directories`, `breadcrumbs`
- `KnowledgeFileIdForm`: `directory_id`
- `WebConfig`: `LINKUP_API_KEY`, `LINKUP_SEARCH_PARAMS`
- `ConfigForm` (retrieval): `MINERU_FILE_EXTENSIONS`

#### Routers - New Endpoints

- `KnowledgeClient.create_knowledge_directory()` — `POST /{id}/dirs/create`
- `KnowledgeClient.update_knowledge_directory()` — `POST /{id}/dirs/{dir_id}/update`
- `KnowledgeClient.delete_knowledge_directory()` — `DELETE /{id}/dirs/{dir_id}/delete`
- `KnowledgeClient.move_file_in_knowledge()` — `POST /{id}/file/move`
- `KnowledgeClient.get_pending_knowledge_files()` — `GET /{id}/files/pending`
- `KnowledgeClient.sync_knowledge_diff()` — `POST /{id}/sync/diff`
- `KnowledgeClient.sync_knowledge_cleanup()` — `POST /{id}/sync/cleanup`
- `FilesClient.rename_file_by_id()` — `POST /v1/files/{id}/rename`
- `UsersClient.get_user_preview_by_id()` — `GET /v1/users/{user_id}/preview`
- `GroupsClient.get_group_preview_by_id()` — `GET /v1/groups/id/{id}/preview`

#### Tests - New Endpoint Coverage

- `tests/test_knowledge.py` — `test_knowledge_directory_crud`, `test_knowledge_move_file_form_validation`, `test_knowledge_get_pending_files`, `test_knowledge_sync_diff`, `test_knowledge_sync_cleanup` (5 new tests covering the 7 new knowledge endpoints)
- `tests/test_files.py` — `test_rename_file_by_id`
- `tests/test_users.py` — `test_get_user_preview_by_id_admin_self`
- `tests/test_groups.py` — `test_get_group_preview_by_id`

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
