# Changelog

## [1.1.0] — 2026-05-05

First release as a Claude Code plugin (was a standalone skill before, distributed via raw `SKILL.md` copy or the `.skill` bundle file).

### Added

- `.claude-plugin/plugin.json` manifest so the skill is installable via marketplace:
  ```bash
  claude plugin marketplace add kurenn/marketplace
  claude plugin install prompt-refiner@kurenn
  ```

### Changed

- `SKILL.md` moved to `skills/prompt-refiner/SKILL.md` (plugin layout convention).
  The skill's name and behavior are unchanged.
- The legacy `prompt-refiner.skill` bundle file at repo root is retained for any
  existing tooling that consumes it directly.

### Migration from manual install

If you were copying `SKILL.md` into `~/.claude/skills/prompt-refiner/` by hand,
switch to the marketplace install path above. Or keep using the local file —
it still works. The plugin install just adds the supported, updateable path.
