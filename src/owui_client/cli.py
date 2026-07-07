"""Command-line interface for owui_client.

A thin Cyclopts-based CLI exposing convenience workflows (e.g. syncing a local
skill file to a remote Open WebUI instance). This module contains no business
logic: it binds CLI flags and environment variables to the async client /
shortcuts layer and prints human-readable results.

Connection defaults come from environment variables:

- ``OWUI_SERVER``: base API URL (default ``http://127.0.0.1:8080/api``).
- ``OWUI_API_KEY``: bearer API key (no default; required by most servers).

Both can be overridden on the command line via ``--server`` / ``--api-key``.
"""

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated, Optional

from cyclopts import App, Parameter

from owui_client import __version__
from owui_client.client import OpenWebUI
from owui_client.shortcuts import SkillSyncResult


app = App(
    name="owui-client",
    version=__version__,
    help="Command-line tools for the owui-client (Open WebUI async client).",
)


@asynccontextmanager
async def _connect(server: str, api_key: Optional[str]):
    """Open an `OpenWebUI` client for the duration of a command.

    `OpenWebUI` is not itself an async context manager, so this wraps it to
    guarantee the underlying httpx transport is closed when the command exits.

    Args:
        server: Base API URL.
        api_key: Bearer API key (may be None).

    Yields:
        A configured `OpenWebUI` client instance.
    """
    client = OpenWebUI(api_url=server, api_key=api_key)
    try:
        yield client
    finally:
        await client._client.aclose()


def _format_skill_result_line(result: SkillSyncResult) -> str:
    """Render one `SkillSyncResult` as a single human-readable line.

    Output shape: ``"{action}: {name} ({id}) {path}"`` with the parenthetical id
    and/or path omitted when absent, and a trailing ``"[{error}]"`` for skipped
    or failed results.
    """
    name = ""
    if result.name and result.id:
        name = f"{result.name} ({result.id})"
    elif result.name:
        name = result.name
    elif result.id:
        name = result.id

    middle = " ".join(p for p in (name, result.path) if p)
    line = f"{result.action}: {middle}" if middle else result.action
    if result.error:
        line += f" [{result.error}]"
    return line


@app.command(name="sync-skill")
async def sync_skill(
    path: Path,
    *,
    server: Annotated[
        str,
        Parameter(
            env_var="OWUI_SERVER",
            help="Open WebUI API base URL (e.g. http://127.0.0.1:8080/api).",
        ),
    ] = "http://127.0.0.1:8080/api",
    api_key: Annotated[
        Optional[str],
        Parameter(
            env_var="OWUI_API_KEY",
            help="Open WebUI API key (bearer token).",
        ),
    ] = None,
) -> None:
    """Sync a local skill Markdown file to the Open WebUI server.

    Creates the skill if it does not exist, updates it if its content/name/
    description changed, and reports ``unchanged`` (with no write) when nothing
    differs. See `Shortcuts.sync_skill` for the full semantics.
    """
    async with _connect(server, api_key) as client:
        result = await client.shortcuts.sync_skill(path)

    print(_format_skill_result_line(result))


@app.command(name="sync-skills")
async def sync_skills(
    dir_path: Path,
    *,
    server: Annotated[
        str,
        Parameter(
            env_var="OWUI_SERVER",
            help="Open WebUI API base URL (e.g. http://127.0.0.1:8080/api).",
        ),
    ] = "http://127.0.0.1:8080/api",
    api_key: Annotated[
        Optional[str],
        Parameter(
            env_var="OWUI_API_KEY",
            help="Open WebUI API key (bearer token).",
        ),
    ] = None,
) -> None:
    """Recursively sync every skill Markdown file under a directory.

    Walks `dir_path` at arbitrary depth, syncing each valid skill file with the
    same create / unchanged / update semantics as `sync-skill` (see
    `Shortcuts.sync_skill`). Non-skill files are skipped, a server error on one
    file does not abort the rest, and nothing is ever deleted.
    """
    async with _connect(server, api_key) as client:
        results = await client.shortcuts.sync_skills(dir_path)

    for result in results:
        print(_format_skill_result_line(result))

    counts: dict[str, int] = {}
    for result in results:
        counts[result.action] = counts.get(result.action, 0) + 1
    summary = ", ".join(f"{action}={n}" for action, n in sorted(counts.items())) or "none"
    total = len(results)
    print(f"summary: {summary} ({total} file{'s' if total != 1 else ''})")


def main() -> None:
    """Entry point for the console script / ``python -m owui_client.cli``."""
    app()


if __name__ == "__main__":
    main()
