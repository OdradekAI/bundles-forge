# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bundles Forge is a bundle-plugin engineering toolkit supporting 6 platforms: Claude Code, Cursor, Codex, OpenCode, Gemini CLI, and OpenClaw. It contains 8 skills covering the full lifecycle of bundle-plugin development (design, scaffold, author, audit, test, optimize, release). The project itself is a bundle-plugin — it uses its own patterns to build and validate itself.

**Requires Python 3.9+** (scripts use `pathlib.Path.is_relative_to` and other 3.9+ features).

## Commands

### Testing

```bash
python tests/run_all.py                            # all 4 test suites (scripts, integration, graph fixtures, unit)
python tests/test_scripts.py -v                    # auditing/releasing script tests (unittest)
python tests/test_integration.py -v                # structure, hooks, version sync, skill discovery
python -m pytest tests/test_scripts.py -v          # same, via pytest
python -m pytest tests/test_scripts.py -v -k test_project_mode_runs_without_error  # single test
```

Test suites: `test_scripts` (audit/release CLI scripts), `test_integration` (project structure, hooks, version sync, skill discovery), `test_graph_fixtures` (dependency graph fixtures), `test_unit` (unit tests). All 4 are collected by `tests/run_all.py`.

### Quality & Security

```bash
bundles-forge audit-skill [project-root]       # project-level skill quality audit (auto-detects mode)
bundles-forge audit-skill [skill-dir]          # single skill audit (4 categories)
bundles-forge audit-skill --all [project-root] # force project-level mode
bundles-forge audit-security [project-root]     # 7-surface security scan
bundles-forge audit-plugin [project-root]     # combined audit (calls audit_skill + audit_security + workflow)
bundles-forge audit-workflow [project-root]    # workflow integration audit (W1-W11)
bundles-forge audit-docs [project-root]        # documentation consistency (9 checks: D1-D9)
bundles-forge checklists [project-root]        # regenerate checklist tables from audit-checks.json registry
bundles-forge checklists --check [project-root] # detect checklist drift (exit 1 if stale)
```

Audit scripts accept `--json` for machine-readable output. Exit codes: 0 = pass, 1 = warnings, 2 = critical.

### Version Management

```bash
bundles-forge bump-version --check             # detect version drift across manifests
bundles-forge bump-version --audit             # find undeclared version strings
bundles-forge bump-version <new-version>       # bump all files declared in .version-bump.json
```

## Architecture

### Directory Layout

- `bin/` — CLI dispatcher (`bundles-forge`, `bundles-forge.cmd`) routing subcommands to scripts
- `skills/` — 8 skill directories, each containing `SKILL.md` and optional `references/` subdirectory
- `agents/` — 3 subagent definitions (inspector, auditor, evaluator) as `.md` files
- `commands/` — slash command stubs (`bundles-*.md`) that redirect to skills via `bundles-forge:<skill-name>`
- `hooks/` — session bootstrap (`session-start.py` emits lightweight skill-list prompt); `openclaw-bootstrap/` contains the OpenClaw hook-pack (HOOK.md + handler.js)
- `docs/` — guides (concepts, blueprinting, scaffolding, authoring, auditing, optimizing, releasing) with `*.zh.md` Chinese translations; checked by D7
- `skills/auditing/scripts/` — audit, security scan, documentation checks, and checklist generation (shares `_cli.py` for argparse/exit-code patterns)
- `skills/releasing/scripts/` — version bump tooling (`bump_version.py`)
- `tests/` — 4 test suites run by `run_all.py`; fixtures in `tests/fixtures/`, prompt snapshots in `tests/prompts/`
- `examples/` — worked audit report examples
- `.github/workflows/validate-plugin.yml` — CI: JSON validation, version/checklist drift, audit-skill, audit-security, audit-docs, tests (Python 3.9 + 3.12 matrix)

### Skill Architecture: Hub-and-Spoke Model

Skills are organized into two layers:

**Orchestration layer** (hub) — diagnose, decide, delegate:
- `blueprinting` — new-project pipeline: interview → scaffolding → authoring → workflow design → auditing
- `optimizing` — existing-project improvement: diagnose → delegate to authoring/scaffolding → verify via auditing
- `releasing` — release pipeline: auditing → testing → optimizing (if needed) → version bump → publish

**Execution layer** (spoke) — single-responsibility workers:
- `scaffolding` — generate project structure, platform adaptation, inspector self-check
- `authoring` — write/improve SKILL.md and agents/*.md content
- `auditing` — pure diagnostics: check, score, report (does not orchestrate fixes)
- `testing` — dynamic verification: local install, hook smoke tests, component discovery

**Meta-skill:** `using-bundles-forge` — lightweight session bootstrap (skill list prompt) and on-demand routing context.

Pipeline stages: `blueprinting` → `optimizing` → `releasing`. Each orchestrator dispatches executors as needed. Users can also invoke any executor directly for standalone tasks.

### Session Bootstrap

The `hooks/session-start.py` script runs on SessionStart (matcher: `startup|clear|compact`, excluding `resume` since resumed sessions retain context). It emits a lightweight one-line prompt listing available skills. The full routing context (`using-bundles-forge/SKILL.md`) is loaded on demand via the platform's Skill tool. Platform detection is three-way: `CURSOR_PLUGIN_ROOT` → Cursor format (`additional_context`), `CLAUDE_PLUGIN_ROOT` → Claude Code format (`hookSpecificOutput`), neither → plain text fallback. Written in Python for cross-platform compatibility (Windows/Mac/Linux).

The `hooks/hooks.json` includes a `SessionStart` hook (lightweight bootstrap via `hooks/session-start.py`). The `hooks/hooks-cursor.json` provides the Cursor-specific configuration (same script, Cursor's camelCase event names). The `hooks/openclaw-bootstrap/` directory is an OpenClaw hook-pack (`HOOK.md` + `handler.js`) that fires on `command:new` and `command:reset` events.

### Agent Dispatch

Skills dispatch read-only subagents (disallowed from editing files) as diagnostic tools. Subagents write reports to `.bundles-forge/`:
- `inspector` — validates scaffolded structure and platform adaptation (dispatched by `scaffolding`)
- `auditor` — runs 10-category audit (dispatched by `auditing`)
- `evaluator` — A/B skill evaluation and chain verification (dispatched by `optimizing` and `auditing`)

**Design pattern:** Each agent file in `agents/` is a self-contained executor — it holds the complete execution protocol (what to check, how to score, how to report). Skills handle scope detection, dispatch, result composition, and fallback. When subagents are unavailable, skills fall back to reading the agent file inline. This ensures a single source of truth with zero duplication between skills and agents.

### Platform Manifests

Version is synchronized across these files (declared in `.version-bump.json`):

| Platform | Manifest | Version-synced |
|----------|----------|:--------------:|
| (root) | `package.json` | Yes |
| Claude Code | `.claude-plugin/plugin.json` | Yes |
| Claude Code | `.claude-plugin/marketplace.json` | Yes |
| Cursor | `.cursor-plugin/plugin.json` | Yes |
| Codex | `.codex/INSTALL.md` | No (install guide) |
| OpenCode | `.opencode/plugins/bundles-forge.js` | No (plugin loader) |
| Gemini CLI | `gemini-extension.json` | Yes |
| OpenClaw | (uses `.claude-plugin/plugin.json`) | Yes (shared) |

## Key Conventions

- **Skill naming:** lowercase with hyphens; directory name must match frontmatter `name` field
- **Descriptions:** must start with "Use when..." and describe triggering conditions, not workflow steps
- **Descriptions:** stay under 250 characters; total frontmatter under 1024 characters
- **Heavy reference content:** extract to `references/` subdirectory (threshold: 100+ lines)
- **Cross-references:** use `bundles-forge:<skill-name>` format
- **Version bumps:** never edit version numbers manually — use `bump_version.py`
- **Pre-commit:** run `bundles-forge bump-version --check` to detect version drift
- **Pre-commit:** run `bundles-forge checklists --check` to detect checklist drift
- **Pre-release:** run `bundles-forge:auditing` for full quality + security check
- **Pre-release:** run `bundles-forge audit-docs` to verify documentation consistency (9 checks: D1-D9)
- **Source of truth:** Skills are first-class citizens — see `skills/auditing/references/source-of-truth-policy.md` for the full hierarchy and contradiction resolution protocol
- **Documentation:** every guide in `docs/` has a `.zh.md` Chinese translation that must stay in sync; checked by audit-docs (D7-D9)
- **Adding scripts:** new CLI scripts under `skills/auditing/scripts/` should import `_cli.py` for shared argparse setup, `BundlesForgeError`, and `exit_by_severity()` patterns

## Security Rules

- No network calls (`curl`, `wget`) in hook scripts
- No references to sensitive files (`.env`, `.ssh/`) in SKILL.md instructions
- No `eval()` or `child_process` in plugin code
