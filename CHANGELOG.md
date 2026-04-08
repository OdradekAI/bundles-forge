# Changelog

## [Unreleased]

## [1.3.2] - 2026-04-09

### Added

- **Minimal/Intelligent dual-mode** in `designing` and `scaffolding` — minimal mode for quick skill packaging (just skills + manifest), intelligent mode for full multi-platform projects with hooks, bootstrap, and version infrastructure.
- **Third-party skill handling** in `designing` — inventory, compatibility analysis, integration intent (repackage vs integrate), and mandatory security audit for imported content.
- **Skill visibility classification** — entry-point skills get matching commands in `commands/`, internal skills are invoked only by other skills in the workflow chain.
- **Advanced components** in `designing` and `scaffolding` — conditional support for `bin/`, `.mcp.json`, `.lsp.json`, `output-styles/`, and `settings.json`.
- **Optional/Advanced components reference** in `scaffolding/references/project-anatomy.md` — documentation for plugin executables, MCP/LSP servers, output styles, settings, userConfig, environment variables, and caching behavior.
- **Commands** for `optimizing` (`optimize-project.md`) and `releasing` (`release-project.md`) entry-point skills.
- **GitHub Release creation** in `releasing` skill — `gh release create` step after tag push, with fallback to GitHub web UI.

### Changed

- **`using-bundles-forge` routing table** — split into "User Entry Points" (designing, auditing, optimizing, releasing) and "Workflow Skills" (scaffolding, writing-skill, adapting-platforms).
- **`scaffolding` description** — rewritten to reflect dual-mode support.
- **`designing` design document template** — now includes mode, visibility column, advanced components, and third-party sources table.

### Removed

- **`commands/scaffold-project.md`** — scaffolding reclassified as workflow skill (invoked by designing, not directly by users).

### Fixed

- **`.gitignore`** — added `__pycache__/` pattern and removed committed `.pyc` files.
- **`.gitignore`** — added missing trailing newline.

## [1.3.1] - 2026-04-08

### Removed

- **Copilot CLI platform support** — removed from all documentation, hooks, manifests, and SKILL.md files. Copilot CLI has no plugin/extension system; this was fictional. Platform count reduced from 6 to 5.
- **`scanning-security` skill** — merged into `auditing` as Category 9 (Security Scan). Security checklist moved to `auditing/references/security-checklist.md`.
- **`iterating-feedback` skill** — merged into `optimizing` as the Feedback Iteration sub-process.
- **`managing-versions` skill** — merged into `releasing` as the Version Management Infrastructure section.
- **`security-scanner` agent** — functionality absorbed by `project-auditor` agent.
- **`package.json` `main` and `type` fields** — misleading for a multi-platform markdown-based project.
- **`hooks.json` `matcher` field** — unnecessary for `SessionStart` hooks per Claude Code docs.

### Changed

- **Skill consolidation: 11 → 8 skills** — three skills absorbed into their natural parents, reducing cognitive load and improving agent routing accuracy.
- **`auditing` skill** — now includes full 5-target security scanning inline, with termination rule (max one re-audit cycle).
- **`optimizing` skill** — now includes feedback iteration workflow with 3-question validation framework.
- **`releasing` skill** — now includes version management infrastructure (`.version-bump.json`, `bump-version.sh` usage).
- **`hooks/session-start`** — simplified platform detection (removed `COPILOT_CLI` branch).
- **`using-bundles-forge` routing table** — updated to 8 skills with revised descriptions and priority order.
- Updated all cross-references: `bundles-forge:scanning-security` → `bundles-forge:auditing`, `bundles-forge:iterating-feedback` → `bundles-forge:optimizing`, `bundles-forge:managing-versions` → `bundles-forge:releasing`.
- Updated README.md and README.zh.md — lifecycle diagram, skill tables, agent list, command mappings.
- Updated `CLAUDE.md` — 5 platforms, 8 skills.
- Updated `AGENTS.md` — expanded from one-line pointer to full quick reference with skill list.
- Updated `project-auditor` agent — now references both quality and security checklists.
- Updated `tests/test-skill-discovery.sh` — expects 8 skills.

### Added

- **"Why Bundles?" section** in both READMEs — concrete explanation of when and why to use the bundles pattern.
- **Python test suite** (`tests/test_scripts.py`) — 12 cross-platform tests covering `lint-skills.py`, `scan-security.py`, `audit-project.py`, and cross-reference integrity.
- **Cycle termination conditions** in `auditing` and `optimizing` to prevent infinite audit-optimize loops.

## [1.3.0] - 2026-04-08

### Changed

- Renamed project from `skill-forge` to `bundles-forge`
- Replaced `skill-project` / `skill-projects` terminology with `bundles` throughout
- Renamed all 11 skill directories:
  - `auditing-skill-projects` → `auditing`
  - `designing-skill-projects` → `designing`
  - `optimizing-skill-projects` → `optimizing`
  - `releasing-skill-projects` → `releasing`
  - `scaffolding-skill-projects` → `scaffolding`
  - `adapting-skill-platforms` → `adapting-platforms`
  - `iterating-skill-feedback` → `iterating-feedback`
  - `managing-skill-versions` → `managing-versions`
  - `scanning-skill-security` → `scanning-security`
  - `writing-skill-content` → `writing-skill`
  - `using-skill-forge` → `using-bundles-forge`
- Renamed OpenCode plugin file to `bundles-forge.js`
- Renamed command `/use-skill-forge` → `/use-bundles-forge`
- Updated all repository URLs to `odradekai/bundles-forge`
- Replaced all `skill-forge:` cross-reference prefixes with `bundles-forge:`
- Updated all cross-reference skill names to match new directory names

## [1.2.0] - 2026-04-07

### Added

- New skill: `iterating-skill-feedback` for receiving user feedback about skills, validating suggestions against core goals, forking external skills with identifiers, and automatic post-change auditing
- Scope clarification between `optimizing-skill-projects` (project engineering) and `iterating-skill-feedback` (single-skill effectiveness)

### Changed

- Updated `auditing-skill-projects` integration: added Suggests relationship to `iterating-skill-feedback`
- Updated `optimizing-skill-projects` integration: added Cross-refers relationship to `iterating-skill-feedback`
- Updated `using-skill-forge` routing table, skill priority, and red flags to include the new skill
- Updated workflow diagrams in README to show audit branching into both optimizing and iterating paths

## [1.1.0] - 2026-04-07

### Changed

- Renamed project from `skill-engineering-guide` to `skill-forge`
- Renamed bootstrap skill directory `using-skill-engineering-guide` → `using-skill-forge`
- Renamed OpenCode plugin file to `skill-forge.js`
- Updated all repository URLs to `odradekai/skill-forge`
- Replaced all `seg:` cross-reference prefixes with `skill-forge:`
- Renamed command `/use-seg` → `/use-skill-forge`

### Removed

- Removed project abbreviation `seg` — all references now use the full name `skill-forge`

## [1.0.0] - 2026-04-06

### Added

- Initial release as a structured skill-project
- Refactored from single-skill folder to full plugin architecture following superpowers conventions
- Multi-platform support: Claude Code, Cursor, Codex, OpenCode, Copilot CLI, Gemini CLI
- Platform manifests for all 6 supported platforms
- Session bootstrap hooks with Windows polyglot support
- Version synchronization infrastructure (`.version-bump.json` + `bump-version.sh`)
- **skill-engineering-guide** skill: project scaffolding, auditing, optimization, and platform adaptation
