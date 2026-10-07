# Repository instructions

This repository maintains one canonical directory per skill under `skills/`.

- Keep shared Claude Code and Codex workflows in one `SKILL.md`; use tool-neutral wording and relative resource paths.
- Preserve optional agent metadata and supporting scripts when importing or updating skills.
- Do not add duplicate platform-specific skill folders or legacy copies.
- Do not create installation symlinks or change user agent configuration unless explicitly requested.
- Do not modify generated files or add agent co-authors to commits.
- Use plain dashes rather than em dashes.
- Validate changed skills with `scripts/validate_skills.py` and run relevant script checks before publishing.
- Work on an isolated task branch and PR. Leave merging to the user.
