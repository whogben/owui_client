from pathlib import Path
from typing import TYPE_CHECKING, Literal, Optional

from httpx import HTTPStatusError
from pydantic import BaseModel

from owui_client.models.skills import SkillForm, SkillMeta, SkillModel
from owui_client.skillfiles import discover_skill_files, parse_skill_file

if TYPE_CHECKING:
    from owui_client.client import OpenWebUI


class SkillSyncResult(BaseModel):
    """Outcome of syncing one skill file via `Shortcuts.sync_skill` or one file
    within a directory via `Shortcuts.sync_skills`.

    Attributes:
        action: What happened to this file. ``"created"`` (new skill written),
            ``"updated"`` (existing skill changed), ``"unchanged"`` (matched and
            identical, no write performed), ``"skipped"`` (file was not a valid
            skill or was a duplicate name, never sent to the server), or
            ``"failed"`` (a server error occurred while syncing this file).
        id: The Open WebUI id of the skill, when known.
        name: The display name of the skill, when known.
        path: The local file path this result refers to.
        error: For ``"skipped"``/``"failed"``, the reason or error message.
    """

    action: Literal["created", "updated", "unchanged", "skipped", "failed"]
    id: Optional[str] = None
    name: Optional[str] = None
    path: Optional[str] = None
    error: Optional[str] = None


class Shortcuts:
    """
    A collection of convenience methods (shortcuts) that combine multiple API calls
    into single, easy-to-use workflows.

    Access these via `client.shortcuts`.
    """

    def __init__(self, client: "OpenWebUI"):
        self.client = client

    async def _reconcile_skill(
        self,
        path: str | Path,
        form: SkillForm,
        by_id: dict[str, SkillModel],
        by_name: dict[str, SkillModel],
    ) -> SkillSyncResult:
        """Reconcile one parsed skill form against existing server skills.

        Shared by `Shortcuts.sync_skill` (single file) and `Shortcuts.sync_skills`
        (whole directory). Implements the idempotent create / unchanged / update
        logic:

        - **No match** by id or name: creates the skill. If the server rejects the
          create with an ``ID_TAKEN`` (HTTP 400) error — meaning another skill
          owns that id but was not returned by export — falls back to updating by
          id.
        - **Match, unchanged**: content, name, and description all equal the
          existing skill. Returns ``"unchanged"`` and performs NO write.
        - **Match, changed**: updates the matched skill by id.

        Never deletes or modifies access grants; ``access_grants`` is omitted on
        writes so existing grants are preserved. On update, the matched skill's
        existing ``is_active`` is preserved (a content change does not re-enable
        a skill disabled in the UI).

        Args:
            path: Local file path (recorded on the returned result).
            form: The `SkillForm` to sync.
            by_id: Existing server skills keyed by id.
            by_name: Existing server skills keyed by name.

        Returns:
            `SkillSyncResult` for this file.
        """
        match = by_id.get(form.id) or by_name.get(form.name)

        if match is None:
            try:
                await self.client.skills.create_new_skill(form)
            except HTTPStatusError as e:
                if _is_id_taken(e):
                    await self.client.skills.update_skill_by_id(form.id, form)
                else:
                    raise
            return SkillSyncResult(
                action="created", path=str(path), id=form.id, name=form.name
            )

        if (
            match.content == form.content
            and match.name == form.name
            and match.description == form.description
        ):
            return SkillSyncResult(
                action="unchanged", path=str(path), id=match.id, name=match.name
            )

        # Preserve the server's is_active so a content change does not silently
        # re-enable a skill the operator disabled in the UI (is_active is True
        # only on the create path, where the skill is genuinely new).
        form.is_active = match.is_active
        await self.client.skills.update_skill_by_id(match.id, form)
        return SkillSyncResult(
            action="updated", path=str(path), id=match.id, name=match.name
        )

    async def sync_skill(self, path: str | Path) -> SkillSyncResult:
        """Idempotently sync a local skill Markdown file to Open WebUI.

        Parses the file (see `owui_client.skillfiles`), then reconciles it
        against existing skills returned by `SkillsClient.export_skills`:

        - **No match** (by id or by name): creates the skill. If the server
          rejects the create with an ``ID_TAKEN`` (HTTP 400) error — indicating
          another skill already owns that id but was not returned by export —
          falls back to updating the skill by id.
        - **Match, unchanged**: content, name, and description all equal the
          existing skill. Returns ``"unchanged"`` and performs NO write, so the
          server's ``updated_at`` is not bumped.
        - **Match, changed**: updates the matched skill by id.

        Never deletes, toggles, or modifies access grants. When updating,
        ``access_grants`` is omitted (``None`` + ``exclude_none``) so existing
        grants on the server are preserved.

        Args:
            path: Path to a Markdown skill file with YAML frontmatter
                (non-empty ``name`` and ``description``).

        Returns:
            `SkillSyncResult`: The action taken plus the skill's id and name.

        Raises:
            `InvalidSkillFileError`: If the file has no/invalid frontmatter or is
                missing a required field (propagated from `parse_skill_file`).
            httpx.HTTPStatusError: On any other server error (re-raised).

        Examples:
            ```python
            result = await client.shortcuts.sync_skill("skills/summarizer.md")
            print(result.action, result.id)
            ```
        """
        parsed = parse_skill_file(path)

        form = SkillForm(
            id=parsed.id,
            name=parsed.name,
            description=parsed.description,
            content=parsed.content,
            meta=SkillMeta(tags=[]),
            is_active=True,
            access_grants=None,
        )

        existing = await self.client.skills.export_skills()
        by_id = {skill.id: skill for skill in existing}
        by_name = {skill.name: skill for skill in existing}

        return await self._reconcile_skill(path, form, by_id, by_name)

    async def sync_skills(self, dir_path: str | Path) -> list[SkillSyncResult]:
        """Recursively sync every valid skill file under a directory.

        Discovers all ``.md`` files under `dir_path` (arbitrary depth) via
        `discover_skill_files`, then reconciles each valid skill against the
        server using the same create / unchanged / update logic as
        `Shortcuts.sync_skill`. Existing skills are fetched once via
        `SkillsClient.export_skills`.

        - Files that are not valid skills, or that collide on a duplicate
          normalized id, are reported as ``"skipped"`` and never sent to the
          server.
        - A server error on one file is recorded as ``"failed"`` and does not
          abort the rest of the directory.
        - Nothing is ever deleted, toggled, or access-changed.

        Args:
            dir_path: Directory to scan recursively.

        Returns:
            A list of `SkillSyncResult` (one per ``.md`` file), sorted by path.

        Raises:
            `InvalidSkillFileError`: If `dir_path` does not exist or is not a
                directory (propagated from `discover_skill_files`).
        """
        discovered = discover_skill_files(dir_path)

        results: list[SkillSyncResult] = [
            SkillSyncResult(action="skipped", path=str(d.path), error=d.skip_reason)
            for d in discovered
            if d.parsed is None
        ]
        to_sync = [d for d in discovered if d.parsed is not None]

        by_id: dict[str, SkillModel] = {}
        by_name: dict[str, SkillModel] = {}
        if to_sync:
            existing = await self.client.skills.export_skills()
            by_id = {skill.id: skill for skill in existing}
            by_name = {skill.name: skill for skill in existing}

        for d in to_sync:
            parsed = d.parsed
            form = SkillForm(
                id=parsed.id,
                name=parsed.name,
                description=parsed.description,
                content=parsed.content,
                meta=SkillMeta(tags=[]),
                is_active=True,
                access_grants=None,
            )
            try:
                results.append(
                    await self._reconcile_skill(d.path, form, by_id, by_name)
                )
            except HTTPStatusError as e:
                results.append(
                    SkillSyncResult(
                        action="failed",
                        path=str(d.path),
                        id=form.id,
                        name=form.name,
                        error=str(e),
                    )
                )

        results.sort(key=lambda r: r.path or "")
        return results


def _is_id_taken(error: HTTPStatusError) -> bool:
    """Best-effort detection of the backend's ``ID_TAKEN`` conflict.

    The Open WebUI skills router replies with HTTP 400 and a detail of
    ``"Uh-oh! This id is already registered..."`` when a create collides with an
    existing id. `OWUIClientBase._request` appends that detail to the exception
    args, so we inspect both the args and the raw response body.

    Args:
        error: An httpx HTTPStatusError raised by the client.

    Returns:
        True if the error plausibly indicates an id collision worth retrying as
        an update.
    """
    if error.response.status_code != 400:
        return False
    haystack = " ".join(str(arg) for arg in error.args) + " " + (error.response.text or "")
    return "ID_TAKEN" in haystack or "already registered" in haystack
