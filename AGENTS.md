# PROJECT KNOWLEDGE BASE

**Generated:** 2026-04-17
**Commit:** 8c2e762
**Branch:** main

## OVERVIEW

Bundle-plugin engineering toolkit (Python 3.9+, Node.js packaging). 8 skills in hub-and-spoke architecture: 3 orchestrators dispatch 4 executors. Supports 6 platforms. Dogfoods its own patterns.

## STRUCTURE

```
bundles-forge/
├── bin/               # CLI dispatcher → routes subcommands to skills/*/scripts/
├── skills/            # 8 skills, each with SKILL.md + optional references/
│   ├── auditing/      #   scripts/ (7 Python scripts), references/ (11 files)
│   └── scaffolding/   #   assets/ (6 platform templates + root/hooks/scripts)
├── agents/            # 3 read-only subagents: inspector, auditor, evaluator
├── hooks/             # session-start (Bash) + run-hook.cmd (polyglot) + openclaw-bootstrap/
├── docs/              # 10 guide pairs (EN + .zh.md), checked by audit-docs D7-D9
├── tests/             # 6 suites via run_all.py; fixtures/ + prompts/ per skill
├── examples/          # Worked audit report examples
├── .github/workflows/ # validate-plugin.yml (Python 3.9+3.12 matrix)
└── package.json       # v1.7.8 — version synced via .version-bump.json
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Add audit check | `skills/auditing/references/audit-checks.json` | Registry of all S1-PC7 checks; scripts read this |
| Fix audit script | `skills/auditing/scripts/` | Shared `_cli.py` for argparse/exit codes; `_graph.py` for workflow DAG |
| Add platform support | `skills/scaffolding/assets/platforms/<name>/` | Template files per platform (plugin.json, hooks.json, AGENTS.md, etc.) |
| Version management | `skills/releasing/scripts/bump_version.py` | Driven by `.version-bump.json`; never edit versions manually |
| Session bootstrap | `hooks/session-start` + `hooks/run-hook.cmd` | 3-way platform detection (CURSOR_PLUGIN_ROOT, CLAUDE_PLUGIN_ROOT, COPILOT_CLI/fallback) |
| Security patterns | `skills/auditing/references/security-checklist.md` | 7 surfaces: skill content, hook scripts, HTTP hooks, OpenCode, agents, bundled scripts, MCP |
| Test a skill | `tests/prompts/<skill-name>.yml` | YAML prompt samples for should-trigger/should-not-trigger |
| Add a test fixture | `tests/fixtures/<scenario>/` | Simulate plugin states (artifact-mismatch, circular-deps, etc.) |
| Documentation sync | `docs/*.md` ↔ `docs/*.zh.md` | Every guide has a Chinese translation; D7-D9 checks consistency |
| CLI subcommand | `bin/bundles-forge` | Dispatcher; add new subcommand to COMMANDS dict |

## CONVENTIONS

- **Skill naming:** kebab-case; dir name = frontmatter `name` field
- **Descriptions:** start "Use when...", triggering conditions only, <250 chars; frontmatter <1024 chars
- **Heavy content:** extract to `references/` (threshold: 100+ lines)
- **Cross-references:** `bundles-forge:<skill-name>` format
- **Source of truth hierarchy:** SKILL.md > agent files > docs/ > README — see `skills/auditing/references/source-of-truth-policy.md`
- **New scripts:** import `_cli.py` for `BundlesForgeError`, `make_parser()`, `exit_by_severity()`
- **Version bumps:** never manual — `bundles-forge bump-version <ver>` updates all manifests in `.version-bump.json`

## ANTI-PATTERNS (THIS PROJECT)

- **NEVER** edit version strings manually across manifests — always use `bump_version.py`
- **NEVER** add `eval()`, `child_process`, network calls (`curl`/`wget`) in hook scripts or plugin code
- **NEVER** reference `.env`, `.ssh/`, credentials in SKILL.md instructions
- **NEVER** skip `bundles-forge bump-version --check` and `checklists --check` before committing
- **NEVER** release without running `bundles-forge:auditing` + `bundles-forge audit-docs`
- **DO NOT** use `as any`, `@ts-ignore` — not applicable here (Python-only codebase), but equivalent: no bare `except:` or silenced errors
- **DO NOT** write tests that delete fixtures to "pass"

## UNIQUE STYLES

- **Hub-and-spoke skill model:** orchestrators (`blueprinting`, `optimizing`, `releasing`) dispatch executors (`scaffolding`, `authoring`, `auditing`, `testing`); never the reverse
- **Skill-agent boundary:** skills handle orchestration (scope detection, dispatch); agents handle execution (checks, scoring). No duplication — agent file is single source of truth for execution details
- **Inline fallback:** when subagents unavailable, skills read agent files inline rather than re-implementing logic
- **10-category audit:** structure, manifests, version sync, skill quality, cross-refs, workflow, hooks, testing, docs, security — all from `audit-checks.json`
- **3-layer workflow audit:** static (DAG), semantic (Inputs/Outputs/Integration), behavioral (evaluator agent)
- **Bilingual docs:** every `docs/*.md` has `docs/*.zh.md` — D7-D9 validates consistency

## COMMANDS

```bash
# Quality & Security
bundles-forge audit-skill .                  # skill quality (4 categories)
bundles-forge audit-security .               # 7-surface security scan
bundles-forge audit-plugin .                 # combined (10 categories)
bundles-forge audit-workflow .               # W1-W11 workflow integrity
bundles-forge audit-docs .                   # D1-D9 documentation consistency
bundles-forge checklists --check .           # detect checklist drift

# Version Management
bundles-forge bump-version --check           # detect version drift
bundles-forge bump-version --audit           # find undeclared version strings
bundles-forge bump-version <new-version>     # bump all manifests

# Testing
python tests/run_all.py                      # all 6 suites
python -m pytest tests/test_scripts.py -v    # single suite
```

## NOTES

- `.repos/` contains cloned reference repositories — not part of the plugin, exclude from audits
- `skills/scaffolding/assets/` is a template directory — files here are copied to new projects, not used directly
- CI matrix: Python 3.9 + 3.12 on ubuntu-latest; 3.12 on windows-latest
- Exit codes: 0 = pass, 1 = warnings, 2 = critical (audit scripts)
- The `using-bundles-forge` meta-skill is loaded via session-start hook, not by user request
