# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Package version numbers follow the Open WebUI mapping described in the README (they are not independent SemVer).

## [Unreleased]

## [9.2.0] - 2026-04-26

### Changed

- Updated target Open WebUI version from 0.8.10 to 0.9.2.
- Bumped package version to 9.2.0 following the Open-WebUI-aligned versioning scheme.

### Added

- Compatibility with Open WebUI v0.9.2 API changes across all routers.
- New router support for analytics, automations, and calendar endpoints (v0.9.2).
- New config fields: CUSTOM_API_KEY_HEADER, ENABLE_RESPONSES_API_STATEFUL, OPENID_END_SESSION_ENDPOINT, PaddleOCR-vl, and Firecrawl v2 settings.
- New OAuth session disconnect endpoint.
- New /ready readiness probe endpoint.
- Responses API support in OpenAI and Ollama routers.
- Anthropic Messages API proxy support.
- Notes access grants endpoint.

## [8.10.0] - 2026-04-15

### Changed

- Adopted Open-WebUI-aligned versioning: `client.major` / `client.minor` map to Open WebUI `0.{minor}.{patch}`; `client.patch` is for client-only fixes while targeting the same Open WebUI release. Baseline is now **8.10.0** for Open WebUI **0.8.10** (supersedes prior 1.6.x-style numbering).
- README: explicit target Open WebUI version, mapping rules, and compatibility guidance tied to that target instead of “latest”.
- `tests/conftest.py`: Docker Open WebUI image for session tests is selected from `pyproject.toml` using the same mapping.
- `AGENTS.md`: orchestrator and update workflows, clearer versioning rules, and documentation expectations.

### Added

- `tests/versioning.py` and `tests/test_versions.py` to encode and test the version mapping.
