# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Package version numbers follow the Open WebUI mapping described in the README (they are not independent SemVer).

## [Unreleased]

## [10.2.1] - 2026-07-06

Client-only feature release (still targets Open WebUI 0.10.2).

### Added

- **Command-line interface.** The package now installs an `owui-client` console script (entry point `owui_client.cli:main`), built with Cyclopts. Connection defaults come from the `OWUI_SERVER` and `OWUI_API_KEY` environment variables (overridable with `--server` / `--api-key`); see `example.env`.
- **`sync-skill` command** and the `Shortcuts.sync_skill` workflow it exposes: idempotently syncs a local skill Markdown file (YAML frontmatter with `name` and `description`) into Open WebUI — creates if absent, updates if `content` / `name` / `description` changed, and reports `unchanged` (no write) when nothing differs, so the server's `updated_at` is not bumped. One-way; never deletes. Matching is by id or name, with a create-to-update fallback on `ID_TAKEN`.
- **`sync-skills` command** and `Shortcuts.sync_skills`: recursively sync every valid skill Markdown file under a directory (arbitrary depth — `skill/SKILL.md` or `skill.md`). Existing skills are fetched once per run; each file is created, left `unchanged` (no write), or `updated`. Non-skill files are `skipped` with a reason; duplicate skill names across files are detected and skipped; a server error on one file is recorded as `failed` and does not abort the rest. On update, the matched skill's existing `is_active` is preserved (a content change does not re-enable a skill disabled in the UI). One-way; never deletes.
- **`owui_client.skillfiles`**: pure (no-network) parser for skill Markdown files into the fields used by the client, plus `discover_skill_files` for recursively scanning a directory (with duplicate-name detection).
- New core dependencies: `cyclopts` and `pyyaml`.

## [10.2.0] - 2026-07-04

Small patch tracking Open WebUI 0.10.2. No new endpoints or models; two configuration fields were added upstream.

### Changed

- Updated target Open WebUI version from 0.10.1 to 0.10.2.
- Updated reference source (`refs/owui_source_main/`) and regenerated `refs/owui_openapi_main.json` from Open WebUI 0.10.2 (458 paths, unchanged from 0.10.1).

### Added

#### Models - New Fields

- `AdminConfig`: `ENABLE_MEMORY_SYSTEM_CONTEXT` — admin toggle for the new "Memory System Context" setting. When `False`, memory tools remain available but stored memories are not injected into the system context; when `True` (the env default) they are. Maps to the `memories.system_context.enable` config key.
- `STTConfigForm`: `OPENAI_API_REQUEST_FORMAT` (default `'multipart'`) — how audio is sent to the OpenAI-compatible speech-to-text API: `'multipart'` uploads audio as a multipart form (default), `'json'` sends it as base64-encoded JSON. Compared case-insensitively; any value other than `'json'` uses multipart.

## [10.1.0] - 2026-06-30

Upgrades the target from Open WebUI 0.9.6 to **0.10.1**. Open WebUI 0.10.0 was a large release; this client version adds support for its headline features (event webhooks, external knowledge bases, shared folders, the reworked memory system, admin OAuth configuration, terminal-server orchestration, context compaction, and the new web-search providers) and resolves all detected drift against the 0.10.1 backend.

### Changed

- Updated target Open WebUI version from 0.9.6 to 0.10.1.
- Updated reference source (`refs/owui_source_main/`) and regenerated `refs/owui_openapi_main.json` from Open WebUI 0.10.1.
- `ModelsClient.update_model_by_id()` now **preserves a model's existing access grants** when `access_grants` is omitted from the `ModelForm`. Previously (as a workaround for an OWUI 0.9.6-0.10.1 backend bug where the handler re-validates `ModelForm(...)` and 500s on `access_grants=None`) it defaulted to `[]`, which the backend interprets as "delete all grants" and would silently wipe a model's sharing grants. It now fetches the current grants and re-sends them. Passing an explicit `[]` still clears grants, and a populated list still replaces them.
- `EvaluationsClient`: migrated to the restructured 0.10.1 feedback endpoints. The old `GET /feedbacks/all` (returning `List[FeedbackResponse]`) no longer exists; the client now uses `GET /feedbacks/all/ids` and `GET /feedbacks/all/export` (the `get_all_feedbacks`-style method was removed).

### Added

#### New resource: `EventsClient` (event webhooks system)
- New `owui_client.models.events` module and `owui_client.routers.events` (`client.events`) implementing Open WebUI's 0.10.0 event-webhooks system, which replaced the legacy per-user webhook.
- Models: `EventWebhook`, `EventWebhookTarget`, `EventWebhookForm`, `EventWebhookUpdateForm`.
- Endpoints: `get_event_webhooks()` (`GET /events/webhooks`), `create_event_webhook()` (`POST`), `update_event_webhook()` (`PUT /events/webhooks/{id}`), `delete_event_webhook()` (`DELETE`).

#### Routers - New Endpoints
- `KnowledgeClient`: full **External Knowledge Bases / Connections** feature (11 endpoints) — `get/create/get/update/delete_external_knowledge_connection`, `test_external_knowledge_connection`, `test_external_knowledge_source`, `test_external_knowledge_retrieval`, `create_external_knowledge`, `create_external_knowledge_source`, `update_external_knowledge_source` (under `/external/connections`, `/external/source`, `/external/knowledge`).
- `FoldersClient`: shared-folders feature — `get_shared_folders()` (`GET /shared`), `update_folder_access_by_id()` (`POST /{id}/access/update`), `get_shared_folder_chats()` (`GET /{id}/shared/chats`).
- `MemoriesClient`: reworked memory system — `list_memory_paths()` (`POST /paths`), `read_memory_path()` (`POST /path`).
- `AuthsClient`: admin OAuth configuration — `get_oauth_config()` / `update_oauth_config()` (`GET`/`POST /admin/config/oauth`).
- `ConfigsClient`: `get_config_namespace()` (`GET /namespace/{namespace}`), `put_terminal_server_lifecycle()` (`POST /terminal_servers/lifecycle`), `refresh_terminal_server_terminals()` (`POST /terminal_servers/refresh`).
- `ChatsClient`: `get_archived_count()` (`GET /archived/count`), `unshare_all()` (`DELETE /share/all`), `compact()` (`POST /{id}/compact`, automatic context compaction).
- `UsersClient`: `get_default_user_permission_defaults()` (`GET /default/permissions/defaults`).
- `FilesClient`: `count_files()` (`GET /count`).
- `ModelsClient`: `get_base_model_tags()` (`GET /base/tags`).

#### Models - New Classes
- events: `EventWebhook`, `EventWebhookTarget`, `EventWebhookForm`, `EventWebhookUpdateForm`
- knowledge: `ExternalKnowledgeConnectionForm`, `ExternalKnowledgeSourceForm`, `ExternalKnowledgeCreateForm`, `ExternalKnowledgeSourceCreateForm`, `ExternalKnowledgeSourceUpdateForm`, `ExternalKnowledgeSourceTestForm`, `ExternalKnowledgeRetrieveTestForm`, `ExternalKnowledgeConnectionListResponse`
- folders: `SharedFolderResponse`, `FolderAccessGrantsForm`
- memories: `ListMemoryPathsForm`, `ReadMemoryPathForm`
- auths: `OAuthConfigForm`
- configs: `TerminalServerLifecycleForm`, `TerminalServerRefreshForm`
- chats: `CompactChatForm`
- folders: `FolderModel` gained an `access_grants` field (the backend already returns it on `get_folder_by_id` / `update_folder_access_by_id`; previously it was silently dropped during parsing, so the shared-folders feature could write grants but not read them back)

#### Models - New Fields
- `TaskConfigForm`: `AUTOCOMPLETE_GENERATION_PROMPT_TEMPLATE`
- `ToolMeta`: `has_user_valves`
- `ModelAnalyticsEntry`: `unique_users`, `unique_chats`
- `WorkspacePermissions`: `skills_import`, `skills_export`
- `ChatPermissions`: `import_` (JSON key `import`; serialized via field alias)
- `FeaturesPermissions`: `webhooks`
- `WebConfig` (retrieval): `ENABLE_WEB_SEARCH_CONFIRMATION`, `WEB_SEARCH_CONFIRMATION_CONTENT`, `SERPHOUSE_API_KEY`, `SERPHOUSE_DOMAIN`, `MICROSOFT_WEB_IQ_API_KEY`, `MICROSOFT_WEB_IQ_API_BASE_URL`, `MICROSOFT_WEB_IQ_LANGUAGE`
- `ConfigForm` (retrieval): `EXTERNAL_DOCUMENT_LOADER_HEADERS`, `MISTRAL_OCR_USE_BASE64`, `RAG_TOKENIZER_MODEL`
- `ChatTitleIdResponse`: `snippet`
- `MemoryModel` / `AddMemoryForm` / `MemoryUpdateModel`: `type` (`"user"`/`"context"`), `path`, (`MemoryModel` only) `meta`
- `OAuthClientRegistrationForm`: `oauth_scope`

### Fixed

- `tests/test_tasks.py` `test_tasks_config` / `test_title_generation`: now send `AUTOCOMPLETE_GENERATION_PROMPT_TEMPLATE` (required by the 0.10.1 backend); previously 422.
- `tests/test_root.py` `test_webhook_url`: removed (the legacy `/api/webhook` endpoints were removed in OWUI 0.10.0 and replaced by the event-webhooks system).
- Removed obsolete `xfail` markers that targeted 0.9.6 backend bugs now fixed upstream: `test_ollama.test_ollama_models`, `test_evaluations.test_feedback_lifecycle`, `test_models.test_model_lifecycle` — all now pass against 0.10.1.
- `UsersClient.update_default_user_permissions()` now serializes permissions with `by_alias=True`, so the `ChatPermissions.import_` field is sent under its JSON key `import` (matching the backend's storage key). Previously it relied on the backend's `populate_by_name` to accept `import_`; the round-trip is now covered by a test.
- `KnowledgeClient.get_pending_knowledge_files()` (pre-existing latent bug) used `model=list`, which corrupted list-of-dicts responses into lists of dict keys. Fixed to `list[dict]`.

### Removed

- `RootClient.get_webhook_url()` and `update_webhook_url()`, plus `models.root.UrlForm` — the underlying `/api/webhook` endpoints were removed in Open WebUI 0.10.0. Use the new `EventsClient` instead.
- `EvaluationsClient.get_all_feedbacks()` — the `GET /feedbacks/all` endpoint was removed in 0.10.1; use `get_all_feedback_ids()` / `export_all_feedbacks()`.

### Known Issues (OWUI 0.10.1 Backend / Test Environment)

These tests are marked `xfail` due to upstream behavior unrelated to the client:
- `tests/test_utils.py::test_markdown` — the `/v1/utils/markdown` endpoint was removed in Open WebUI 0.9.6 and remains absent through 0.10.2. The client method and `MarkdownForm` model are retained for forward compatibility but return 404/405 against current backends.
- `tests/test_openai.py::test_speech` — `/audio/speech` hardcodes `https://api.openai.com/v1`, so it cannot be exercised against the mock inference provider in tests.

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
