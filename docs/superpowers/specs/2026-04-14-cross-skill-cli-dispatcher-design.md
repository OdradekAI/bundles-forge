# Cross-Skill CLI Dispatcher Design

Date: 2026-04-14

## Problem

SKILL.md files reference cross-skill scripts with plugin-root-relative paths like `python skills/auditing/scripts/audit_skill.py <project-root>`. After marketplace installation, the plugin lives in `~/.claude/plugins/cache/...`, but the Bash tool runs in the user's project directory. These relative paths cannot resolve.

~30+ shell command references, 4 `allowed-tools` declarations, and ~10 reference doc citations are affected.

## Decision

Create a unified CLI dispatcher in `bin/bundles-forge` that routes subcommands to the correct script. All SKILL.md references switch from direct script paths to the dispatcher.

Rationale: A single entry point is more DRY than 6+ individual `bin/` wrappers (Approach A), avoids per-platform variable name differences (`CLAUDE_PLUGIN_ROOT` vs `CURSOR_PLUGIN_ROOT`), and is extensible — adding a new script requires one line in the command table.

## Architecture

### New Files

```
bin/
  bundles-forge          # Unix/macOS entry point (Python, shebang)
  bundles-forge.cmd      # Windows wrapper
```

### Dispatcher (`bin/bundles-forge`)

Responsibilities (minimal):
1. Command routing — subcommand to script path mapping table
2. `subprocess.call` dispatch — forward args, propagate exit code
3. Help text on `-h` / `--help` / no args

Does NOT:
- Parse or validate arguments (target scripts handle their own CLI)
- Format output (pass-through stdout/stderr)
- Manage versions

Uses `subprocess.call` rather than `runpy`/`exec` because:
- `__file__` semantics are correct (separate process)
- Exit codes propagate naturally
- No sys.path contamination risk
- Target scripts that import sibling modules (`_cli.py`, `_parsing.py`) or cross-skill modules (`bump_version.py`) work unchanged

### Command Table

| Subcommand | Target Script |
|---|---|
| `audit-skill` | `skills/auditing/scripts/audit_skill.py` |
| `audit-security` | `skills/auditing/scripts/audit_security.py` |
| `audit-docs` | `skills/auditing/scripts/audit_docs.py` |
| `audit-plugin` | `skills/auditing/scripts/audit_plugin.py` |
| `audit-workflow` | `skills/auditing/scripts/audit_workflow.py` |
| `checklists` | `skills/auditing/scripts/generate_checklists.py` |
| `bump-version` | `skills/releasing/scripts/bump_version.py` |

### Replacement Rules

| Location | Old Pattern | New Pattern |
|---|---|---|
| SKILL.md body | `python skills/auditing/scripts/X.py` | `bundles-forge <subcommand>` |
| SKILL.md body | `python skills/releasing/scripts/X.py` | `bundles-forge <subcommand>` |
| allowed-tools | `Python(skills/auditing/scripts/X.py *)` | `Bash(bundles-forge <subcommand> *)` |
| allowed-tools | `Python(skills/releasing/scripts/X.py *)` | `Bash(bundles-forge <subcommand> *)` |
| Reference docs | Same as SKILL.md body | Same as SKILL.md body |
| CLAUDE.md | Same as SKILL.md body | Same as SKILL.md body |

### What Does NOT Change

- Python-to-Python imports (`audit_plugin.py` importing `bump_version` via sys.path) — filesystem-level, runs inside the plugin directory
- Internal modules (`_cli.py`, `_parsing.py`) — same reason
- `hooks/session-start.py` path logic — already uses `__file__` self-location
- `bundles-forge:<skill-name>` skill invocation references — skill dispatch, not script paths
- SKILL.md references to `references/` files (e.g. `skills/scaffolding/references/external-integration.md`) — read by Claude's Read tool, not executed via Bash

### Affected Files

**SKILL.md frontmatter (allowed-tools, 5 files):**
- `skills/auditing/SKILL.md`
- `skills/authoring/SKILL.md`
- `skills/optimizing/SKILL.md`
- `skills/scaffolding/SKILL.md`
- `skills/releasing/SKILL.md`

**SKILL.md body + reference docs (~30 references, 12 files):**
- `skills/auditing/SKILL.md`
- `skills/authoring/SKILL.md`
- `skills/authoring/references/quality-checklist.md`
- `skills/optimizing/SKILL.md`
- `skills/scaffolding/SKILL.md`
- `skills/scaffolding/references/project-anatomy.md`
- `skills/scaffolding/references/external-integration.md`
- `skills/releasing/SKILL.md`
- `skills/auditing/references/skill-checklist.md`
- `skills/auditing/references/plugin-checklist.md`
- `skills/auditing/references/workflow-checklist.md`
- `CLAUDE.md`

## Multi-Platform Adapter Strategy

| Platform | `bin/` PATH injection | Adapter action |
|---|---|---|
| Claude Code | Automatic | None |
| Cursor | Verify; fallback to SessionStart PATH injection | `hooks-cursor.json` update |
| Codex | None | Install docs / adapter |
| OpenCode | None | `plugin.js` update |
| Gemini CLI | None | `gemini-extension.json` / install docs |

This phase focuses on Claude Code. Other platforms get adapter updates in follow-up iterations.

## Scope

**In scope:**
- Create `bin/bundles-forge` dispatcher + `bin/bundles-forge.cmd` Windows wrapper
- Replace all `python skills/...` references in SKILL.md files, reference docs, and CLAUDE.md
- Update all `allowed-tools` declarations

**Out of scope (follow-up):**
- Cursor/Codex/OpenCode/Gemini CLI platform adapters
- `session-start.py` PLUGIN_ROOT unification
- New scripts or features
