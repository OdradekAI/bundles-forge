# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bundles Forge is a bundle-plugin engineering toolkit supporting 5 platforms: Claude Code, Cursor, Codex, OpenCode, and Gemini CLI. It contains 7 skills covering the full lifecycle of bundle-plugin development (design, scaffold, author, audit, optimize, release). The project itself is a bundle-plugin — it uses its own patterns to build and validate itself.

## Commands

### Testing

```bash
bash tests/run-all.sh                              # all test suites (shell + Python)
bash tests/test-bootstrap-injection.sh             # session-start hook output
bash tests/test-skill-discovery.sh                 # skill frontmatter validation
bash tests/test-version-sync.sh                    # version consistency across manifests
python tests/test_scripts.py -v                    # Python script tests (unittest)
python -m pytest tests/test_scripts.py -v          # same, via pytest
python -m pytest tests/test_scripts.py -v -k test_lint_runs_without_error  # single test
```

### Quality & Security

```bash
python scripts/lint_skills.py [project-root]       # skill frontmatter/quality lint
python scripts/scan_security.py [project-root]     # 7-surface security scan
python scripts/audit_project.py [project-root]     # combined audit (calls lint + scan + workflow)
python scripts/audit_skill.py [skill-dir]          # single skill audit (4 categories)
python scripts/audit_workflow.py [project-root]    # workflow integration audit (W1-W11)
python scripts/check_docs.py [project-root]        # documentation consistency (7 checks: D1-D7)
python scripts/generate_checklists.py [project-root]        # regenerate checklist tables from audit-checks.json registry
python scripts/generate_checklists.py --check [project-root] # detect checklist drift (exit 1 if stale)
```

All scripts accept `--json` for machine-readable output. Exit codes: 0 = pass, 1 = warnings, 2 = critical.

### Version Management

```bash
python scripts/bump_version.py --check             # detect version drift across manifests
python scripts/bump_version.py --audit             # find undeclared version strings
python scripts/bump_version.py <new-version>       # bump all files declared in .version-bump.json
```

## Architecture

### Directory Layout

- `skills/` — 7 skill directories, each containing `SKILL.md` and optional `references/` subdirectory
- `agents/` — 3 subagent definitions (inspector, auditor, evaluator) as `.md` files
- `commands/` — slash command stubs (`bundles-*.md`) that redirect to skills via `bundles-forge:<skill-name>`
- `hooks/` — session bootstrap: `session-start` reads `using-bundles-forge/SKILL.md` and injects it as platform-appropriate JSON context. `run-hook.cmd` is a polyglot wrapper (Windows cmd + bash)
- `docs/` — guides (concepts, blueprinting, auditing, optimizing, releasing) with `*.zh.md` Chinese translations; checked by D7
- `scripts/` — Python tooling sharing `_cli.py` for common argparse/exit-code patterns

### Skill Architecture: Hub-and-Spoke Model

Skills are organized into two layers:

**Orchestration layer** (hub) — diagnose, decide, delegate:
- `blueprinting` — new-project pipeline: interview → scaffolding → authoring → workflow design → auditing
- `optimizing` — existing-project improvement: diagnose → delegate to authoring/scaffolding → verify via auditing
- `releasing` — release pipeline: auditing → optimizing (if needed) → version bump → publish

**Execution layer** (spoke) — single-responsibility workers:
- `scaffolding` — generate project structure, platform adaptation, inspector self-check
- `authoring` — write/improve SKILL.md and agents/*.md content
- `auditing` — pure diagnostics: check, score, report (does not orchestrate fixes)

Pipeline stages: `blueprinting` → `optimizing` → `releasing`. Each orchestrator dispatches executors as needed. Users can also invoke any executor directly for standalone tasks.

### Session Bootstrap

The `hooks/session-start` script runs on SessionStart (matcher: `startup|clear|compact`, excluding `resume` since resumed sessions retain context). It reads the `using-bundles-forge` meta-skill and emits JSON context. Platform detection is three-way: `CURSOR_PLUGIN_ROOT` → Cursor format (`additional_context`), `CLAUDE_PLUGIN_ROOT` → Claude Code format (`hookSpecificOutput`), neither → plain text fallback. On read failure, the script warns to stderr and exits 0 (no-op).

The `hooks/hooks.json` includes a top-level `description` (shown in Claude Code's `/hooks` menu) and per-handler `timeout: 10` to prevent slow hooks from blocking session start.

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
| Claude Code | `.claude-plugin/plugin.json` | Yes |
| Cursor | `.cursor-plugin/plugin.json` | Yes |
| Codex | `.codex/INSTALL.md` | No (install guide) |
| OpenCode | `.opencode/plugins/bundles-forge.js` | No (plugin loader) |
| Gemini CLI | `gemini-extension.json` | Yes |

## Key Conventions

- **Skill naming:** lowercase with hyphens; directory name must match frontmatter `name` field
- **Descriptions:** must start with "Use when..." and describe triggering conditions, not workflow steps
- **Descriptions:** stay under 250 characters; total frontmatter under 1024 characters
- **Heavy reference content:** extract to `references/` subdirectory (threshold: 100+ lines)
- **Cross-references:** use `bundles-forge:<skill-name>` format
- **Version bumps:** never edit version numbers manually — use `bump_version.py`
- **Pre-commit:** run `python scripts/bump_version.py --check` to detect version drift
- **Pre-commit:** run `python scripts/generate_checklists.py --check` to detect checklist drift
- **Pre-release:** run `bundles-forge:auditing` for full quality + security check
- **Pre-release:** run `python scripts/check_docs.py` to verify documentation consistency

## Security Rules

- No network calls (`curl`, `wget`) in hook scripts
- No references to sensitive files (`.env`, `.ssh/`) in SKILL.md instructions
- No `eval()` or `child_process` in plugin code
