# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Package version numbers follow the Open WebUI mapping described in the README (they are not independent SemVer).

## [Unreleased]

## [8.12.0] - 2026-04-15

### Added

- Added `SkillsClient` with 9 endpoints for workspace skills management
- Added `AnalyticsClient` with 8 endpoints for admin analytics
- Added `ScimClient` with 15 endpoints for SCIM 2.0 provisioning
- Added `TerminalsClient` with HTTP proxy endpoints for terminal servers
- Added `ApiKeyModel`, `NoteResponse`, `UserStatusModel`, `UserRoleUpdateForm` models
- Added `ModelAccessResponse`/`ModelAccessListResponse` with write_access support
- Added `ToolAccessResponse` with write_access support
- Added `FileForm`, `FileUpdateForm`, `FileListResponse` models
- Added `ChannelFileModel`, `ChatFileModel`, `SharedChatResponse` models
- Added `GroupMemberModel`, `GroupListResponse` models
- Added `KnowledgeFileModel`, `KnowledgeListResponse` models
- Added `OAuthSessionResponse`, `KnowledgeListResponse` models
- Added `get_file_content_by_name`, `get_user_info_by_id` endpoints
- Added `get_knowledge_files_by_id`, `get_config` (retrieval) endpoints
- Added `get_models_defaults`, `verify_terminal_server`, `put_terminal_server_policy` config endpoints
- Added `generate_anthropic_messages` Ollama endpoint
- Added page parameter to `list_files` and `get_notes`
- Added skip/limit parameters to `search_files`
- Added order_by/direction/page parameters to `search_users`

### Changed

- `get_models` returns `ModelAccessListResponse`, `get_model_by_id` returns `ModelAccessResponse`
- `get_tool_list` and `get_tool_by_id` return `ToolAccessResponse`
- `get_note_by_id` returns `NoteResponse` with `write_access`
- `update_user_by_id` returns `Optional[UserModel]`
- `FunctionUserResponse` now inherits from `FunctionResponse` instead of `FunctionModel`

### Removed

- Removed 13 stale `access_control` fields from models (no longer in backend)
- Removed stale `has_user_valves`, `api_key`, `oauth_sub` fields

### Fixed

- Fixed `FileModelResponse.updated_at` and `meta` to be Optional
- Fixed `prompt_history.py` snapshot Dict Fields documentation
- Fixed typo in configs.py documentation

## [8.10.0] - 2026-04-15

### Changed

- Adopted Open-WebUI-aligned versioning: `client.major` / `client.minor` map to Open WebUI `0.{minor}.{patch}`; `client.patch` is for client-only fixes while targeting the same Open WebUI release. Baseline is now **8.10.0** for Open WebUI **0.8.10** (supersedes prior 1.6.x-style numbering).
- README: explicit target Open WebUI version, mapping rules, and compatibility guidance tied to that target instead of “latest”.
- `tests/conftest.py`: Docker Open WebUI image for session tests is selected from `pyproject.toml` using the same mapping.
- `AGENTS.md`: orchestrator and update workflows, clearer versioning rules, and documentation expectations.

### Added

- `tests/versioning.py` and `tests/test_versions.py` to encode and test the version mapping.
