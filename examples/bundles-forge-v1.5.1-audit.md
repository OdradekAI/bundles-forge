---
audit-date: "2026-04-10T15:55+08:00"
auditor-platform: "Cursor"
auditor-model: "claude-4.6-opus"
bundles-forge-version: "1.5.1"
source-type: "local-directory"
source-uri: "~/Odradek/bundles-forge"
os: "Windows 10 (10.0.22631)"
python: "3.12.7"
---

# Bundle-Plugin Audit: bundles-forge

## 1. Decision Brief

| Field | Value |
|-------|-------|
| **Target** | `~/Odradek/bundles-forge` |
| **Version** | `1.5.1` |
| **Commit** | `f89d457` |
| **Date** | `2026-04-10` |
| **Audit Context** | `pre-release` |
| **Platforms** | Claude Code, Cursor, Codex, OpenCode, Gemini CLI |
| **Skills** | 8 skills, 3 agents, 5 commands, 5 scripts |

### Recommendation: `CONDITIONAL GO`

**Automated baseline:** 0 critical, 9 warnings, 15 info → script recommends `CONDITIONAL GO`

**Overall score:** 9.1/10 (weighted average; see Category Breakdown)

**Qualitative adjustment:** Adjusted from 9.1 to **9.1** — agrees with baseline. All warnings are concentrated in Testing (missing test prompts and A/B eval results). Core functionality, security, and quality are excellent.

### Top Risks

| # | Risk | Impact | If Not Fixed |
|---|------|--------|-------------|
| 1 | No per-skill test prompts (T5) | 8/8 skills lack trigger/non-trigger test samples | Skill routing regressions go undetected across platform updates |
| 2 | No A/B eval results (T8) | No baseline quality measurement exists | Cannot objectively compare skill versions or detect quality drift |
| 3 | Large skill bodies without references extraction (Q12) | blueprinting (311 lines) and optimizing (331 lines) | Higher token cost on every invocation; slower context loading |

### Remediation Estimate

| Priority | Count | Estimated Effort |
|----------|-------|-----------------|
| P0 (Blocker) | 0 | — |
| P1 (High) | 0 | — |
| P2 (Medium) | 9 | ~2-3 hours (create test prompt YAML for 8 skills + initial A/B eval) |
| P3 (Low) | 15 | ~1 hour (extract references, minor doc improvements) |

---

## 2. Risk Matrix

| ID | Title | Severity | Impact Scope | Exploitability | Confidence | Status |
|----|-------|----------|-------------|----------------|------------|--------|
| TST-001 | Missing test prompts for all 8 skills | P2 | 8/8 skills affected | always triggers | ✅ | open |
| TST-002 | No A/B eval results in .bundles-forge/ | P2 | project-wide | always triggers | ✅ | open |
| SKQ-001 | blueprinting SKILL.md 311 lines without references/ | P3 | 1/8 skills | edge case | ✅ | open |
| SKQ-002 | optimizing SKILL.md 331 lines without references/ | P3 | 1/8 skills | edge case | ✅ | open |
| XRF-001 | Declared circular dependency auditing ↔ optimizing | P3 | workflow chain | rare | ✅ | accepted-risk |
| XRF-002 | Artifact ID mismatches across skill I/O contracts | P3 | 5 cross-skill links | edge case | ⚠️ | open |

---

## 3. Findings by Category

### 3.1 Structure (Score: 10/10, Weight: High)

**Summary:** Exemplary project structure. All required directories, files, and naming conventions are in place.

**Components audited:** `skills/` (8 dirs), `agents/` (3 files), `commands/` (5 files), `hooks/` (3 files), `scripts/` (5 files), project root files

No findings. All checks pass.

---

### 3.2 Platform Manifests (Score: 10/10, Weight: Medium)

**Summary:** All 5 target platforms have valid manifests with complete metadata.

**Components audited:** `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `.codex/INSTALL.md`, `.opencode/plugins/bundles-forge.js`, `gemini-extension.json`

No findings. All checks pass.

Manifest details:
- **Claude Code** — valid JSON, all metadata fields populated
- **Cursor** — valid JSON, `skills` → `./skills/`, `agents` → `./agents/`, `hooks` → `./hooks/hooks-cursor.json` — all paths resolve
- **Codex** — Markdown install instructions (not JSON by design)
- **OpenCode** — valid ESM module, correct `skills` path resolution via `path.resolve`
- **Gemini CLI** — valid JSON, `contextFileName` points to existing `GEMINI.md`

---

### 3.3 Version Sync (Score: 10/10, Weight: High)

**Summary:** All declared version files are in perfect sync at `1.5.1`. No undeclared version strings found.

**Components audited:** `.version-bump.json`, `package.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.cursor-plugin/plugin.json`, `gemini-extension.json`

No findings. All checks pass.

Evidence:
```
All declared files are in sync at 1.5.1
No undeclared files contain the version string. All clear.
```

---

### 3.4 Skill Quality (Score: 10/10, Weight: Medium)

**Summary:** All 8 skills have valid frontmatter, proper "Use when…" descriptions, and well-structured content. Two skills exceed the reference-extraction threshold.

**Components audited:** 8 SKILL.md files

#### [SKQ-001] blueprinting exceeds reference extraction threshold
- **Severity:** P3 | **Impact:** 1/8 skills, higher token cost | **Confidence:** ✅
- **Location:** `skills/blueprinting/SKILL.md` (311 lines)
- **Trigger:** SKILL.md body exceeds 300 lines with no `references/` directory
- **Actual Impact:** Increased token consumption on every invocation
- **Remediation:** Extract interview templates or scenario sections to `references/`

#### [SKQ-002] optimizing exceeds reference extraction threshold
- **Severity:** P3 | **Impact:** 1/8 skills, higher token cost | **Confidence:** ✅
- **Location:** `skills/optimizing/SKILL.md` (331 lines)
- **Trigger:** SKILL.md body exceeds 300 lines with no `references/` directory
- **Actual Impact:** Increased token consumption on every invocation
- **Remediation:** Extract A/B evaluation protocol or chain-eval sections to `references/`

---

### 3.5 Cross-References (Score: 10/10, Weight: Medium)

**Summary:** All `bundles-forge:<skill-name>` references resolve correctly. Declared circular dependency (auditing ↔ optimizing) is properly annotated.

**Components audited:** 8 SKILL.md files, cross-reference graph

#### [XRF-001] Declared circular dependency: auditing ↔ optimizing
- **Severity:** P3 | **Impact:** workflow chain | **Confidence:** ✅
- **Location:** `skills/auditing/SKILL.md` (Integration section), `skills/optimizing/SKILL.md`
- **Trigger:** `<!-- cycle:auditing,optimizing -->` annotation present
- **Actual Impact:** None — this is a deliberate feedback loop, properly declared
- **Remediation:** None needed (accepted risk)

#### [XRF-002] Artifact ID mismatches in cross-skill I/O contracts
- **Severity:** P3 | **Impact:** 5 cross-skill edges | **Confidence:** ⚠️
- **Location:** Multiple skills' `## Inputs` / `## Outputs` sections
- **Trigger:** Output artifact IDs from one skill don't lexically match input IDs of the consuming skill (e.g. scaffolding outputs `scaffold-output` but auditing expects `project-directory`)
- **Actual Impact:** Minor — agents resolve by context, not strict ID matching. Documentation clarity could improve.
- **Remediation:** Align artifact ID naming across I/O contracts for documentation consistency

---

### 3.6 Hooks (Score: 10/10, Weight: Medium)

**Summary:** Hook scripts follow the legitimate baseline pattern. Platform detection works correctly for both Claude Code and Cursor.

**Components audited:** `hooks/session-start` (38 lines), `hooks/run-hook.cmd` (44 lines), `hooks/hooks-cursor.json`

No findings. All checks pass.

Hook baseline verification:
- `session-start`: resolves plugin root → reads `skills/using-bundles-forge/SKILL.md` → JSON-escapes (backslash, quotes, newline, CR, tab) → emits platform-appropriate JSON (`additional_context` for Cursor, `hookSpecificOutput` for Claude Code) → exits 1 with stderr if SKILL.md missing
- `run-hook.cmd`: polyglot cmd/bash dispatcher — validates hook name, resolves path, tries Git Bash, safe exit patterns

---

### 3.7 Testing (Score: 1/10, Weight: Medium)

**Summary:** Test infrastructure exists and covers structural, bootstrap, and version sync verification. However, per-skill test prompts and A/B evaluation results are entirely missing.

**Components audited:** `tests/` directory (6 files)

#### [TST-001] No test prompts for any skill
- **Severity:** P2 | **Impact:** 8/8 skills lack trigger accuracy testing | **Confidence:** ✅
- **Location:** `tests/prompts/` (directory does not exist)
- **Trigger:** T5 check — each skill should have `tests/prompts/<skill-name>.yml`
- **Actual Impact:** Cannot validate that skills trigger on correct inputs and reject incorrect ones; routing regressions invisible
- **Remediation:** Create `tests/prompts/` with YAML files containing should-trigger and should-not-trigger samples per skill
- **Evidence:**
  ```
  [T5] No test prompts for skill 'auditing'
  [T5] No test prompts for skill 'authoring'
  [T5] No test prompts for skill 'blueprinting'
  [T5] No test prompts for skill 'optimizing'
  [T5] No test prompts for skill 'porting'
  [T5] No test prompts for skill 'releasing'
  [T5] No test prompts for skill 'scaffolding'
  [T5] No test prompts for skill 'using-bundles-forge'
  ```

#### [TST-002] No A/B evaluation results
- **Severity:** P2 | **Impact:** project-wide quality baseline absent | **Confidence:** ✅
- **Location:** `.bundles-forge/` (no eval artifacts found)
- **Trigger:** T8 check — most recent A/B eval result should exist
- **Actual Impact:** No objective quality measurement baseline; cannot compare skill versions or detect quality drift
- **Remediation:** Run `bundles-forge:optimizing` with A/B eval protocol to establish baseline

---

### 3.8 Documentation (Score: 10/10, Weight: Low)

**Summary:** Comprehensive documentation with README, CLAUDE.md contributor guidelines, AGENTS.md quick reference, and per-platform install coverage.

**Components audited:** `README.md`, `CLAUDE.md`, `AGENTS.md`, `.codex/INSTALL.md`, `GEMINI.md`

No findings. All checks pass.

---

### 3.9 Security (Score: 10/10, Weight: High)

**Summary:** Zero security findings across all 26 scanned files. No data exfiltration, destructive operations, safety overrides, encoding tricks, or network calls detected.

**Components audited:** 26 files — 8 skill contents + 4 reference markdowns, 3 agent prompts, 3 hook scripts, 5 bundled scripts, 1 OpenCode plugin, 2 scaffolding assets

No findings. All checks pass.

Evidence:
```
Files scanned: 26
Risk summary: 0 critical, 0 warnings, 0 info
```

---

## 4. Methodology

### Scope

| Dimension | Covered |
|-----------|---------|
| **Directories** | `skills/`, `agents/`, `commands/`, `hooks/`, `scripts/`, platform manifests, project root |
| **Check categories** | 9 categories, 50+ individual checks |
| **Total files scanned** | 26 (security) + all project files (structure/quality) |

### Out of Scope

- Runtime behavior of skills (agent execution, prompt-response quality)
- Platform-specific installation end-to-end testing
- Dependencies of dependencies (transitive analysis)

### Tools

| Tool | Purpose |
|------|---------|
| `audit_project.py` | Orchestrated full 9-category audit |
| `scan_security.py` | Security pattern scanning (26 files) |
| `lint_skills.py` | Skill quality linting (8 skills) |
| `bump_version.py --check` | Version drift detection |
| `bump_version.py --audit` | Undeclared version string scan |

### Limitations

- `scan_security.py` uses regex — false positives possible on negated contexts; may miss obfuscated patterns
- `lint_skills.py` uses a lightweight YAML parser — complex YAML edge cases may be missed
- Token estimation uses heuristic rates (prose ~1.3×words, code ~chars/3.5, tables ~chars/3.0); actual counts vary by model

---

## 5. Appendix

### A. Per-Skill Breakdown

#### auditing
**Verdict:** Production-grade audit skill with clear scope detection, 9-category coverage, security-only mode, and well-aligned subagent dispatch.
**Strengths:**
- Comprehensive input normalization (local, GitHub, zip)
- Dual-mode (full project vs single skill) with auto-detection
- Deep integration with reference checklists and report templates

**Key Issues:** None.

| Category | Score |
|----------|-------|
| Structure | 10/10 |
| Skill Quality | 10/10 |
| Cross-References | 10/10 |
| Security | 10/10 |

#### authoring
**Verdict:** Clear, opinionated SKILL.md authoring guide grounded in observed agent behavior, with strong anti-pattern documentation.
**Strengths:**
- "Use when…" description rationale with concrete anti-pattern examples
- Optional frontmatter field table with clear guidance
- Well-defined Integration handoffs

**Key Issues:** None.

| Category | Score |
|----------|-------|
| Structure | 10/10 |
| Skill Quality | 10/10 |
| Cross-References | 10/10 |
| Security | 10/10 |

#### blueprinting
**Verdict:** Thorough planning skill covering new projects, splits, and composition, with third-party and security gates.
**Strengths:**
- Scenario A/B/C structure covers all project initiation patterns
- Minimal vs intelligent mode for progressive complexity
- Concrete design-document template with platform table

**Key Issues:**
- SKILL.md at 311 lines exceeds the 300-line reference-extraction threshold (SKQ-001)

| Category | Score |
|----------|-------|
| Structure | 10/10 |
| Skill Quality | 9/10 |
| Cross-References | 10/10 |
| Security | 10/10 |

#### optimizing
**Verdict:** Strong audit counterpart with measurable improvement loops, A/B evaluation protocol, and chain evaluation.
**Strengths:**
- Scope mirrors auditing for seamless handoff
- A/B and chain evaluation protocols with objective scoring
- Clear "when to skip A/B" decision rules

**Key Issues:**
- SKILL.md at 331 lines exceeds the 300-line reference-extraction threshold (SKQ-002)

| Category | Score |
|----------|-------|
| Structure | 10/10 |
| Skill Quality | 9/10 |
| Cross-References | 10/10 |
| Security | 10/10 |

#### porting
**Verdict:** Focused, practical multi-platform adapter with clear platform comparison and removal checklist.
**Strengths:**
- Platform comparison table covers all 5 targets
- Removal checklist prevents orphaned platform artifacts
- Ties cleanly to auditing and releasing

**Key Issues:** None.

| Category | Score |
|----------|-------|
| Structure | 10/10 |
| Skill Quality | 10/10 |
| Cross-References | 10/10 |
| Security | 10/10 |

#### releasing
**Verdict:** End-to-end release pipeline with version tooling, audit gates, and `gh release create` flow.
**Strengths:**
- Pipeline diagram provides clear visual flow
- Semantic versioning decision table
- Hotfix path for emergency releases

**Key Issues:** None.

| Category | Score |
|----------|-------|
| Structure | 10/10 |
| Skill Quality | 10/10 |
| Cross-References | 10/10 |
| Security | 10/10 |

#### scaffolding
**Verdict:** Well-layered generator spec with minimal/intelligent modes, post-scaffold checklist, and inspector dispatch.
**Strengths:**
- Layer tables align with blueprinting design document
- Inspector/inline fallback for post-scaffold verification
- Template assets included in `assets/` directory

**Key Issues:** None.

| Category | Score |
|----------|-------|
| Structure | 10/10 |
| Skill Quality | 10/10 |
| Cross-References | 10/10 |
| Security | 10/10 |

#### using-bundles-forge
**Verdict:** Effective bootstrap skill with priority rules, routing table, red flags, and subagent guard.
**Strengths:**
- `<SUBAGENT-STOP>` gate prevents unauthorized subagent scope expansion
- Explicit exception rules for auditing/optimizing on single skills
- Compact at 121 lines — low token cost for every session

**Key Issues:** None.

| Category | Score |
|----------|-------|
| Structure | 10/10 |
| Skill Quality | 10/10 |
| Cross-References | 10/10 |
| Security | 10/10 |

### B. Component Inventory

| Component Type | Name | Path | Lines |
|---------------|------|------|-------|
| Skill | auditing | `skills/auditing/SKILL.md` | 255 |
| Skill | authoring | `skills/authoring/SKILL.md` | 232 |
| Skill | blueprinting | `skills/blueprinting/SKILL.md` | 311 |
| Skill | optimizing | `skills/optimizing/SKILL.md` | 331 |
| Skill | porting | `skills/porting/SKILL.md` | 123 |
| Skill | releasing | `skills/releasing/SKILL.md` | 239 |
| Skill | scaffolding | `skills/scaffolding/SKILL.md` | 170 |
| Skill | using-bundles-forge | `skills/using-bundles-forge/SKILL.md` | 121 |
| Agent | auditor | `agents/auditor.md` | 72 |
| Agent | evaluator | `agents/evaluator.md` | 133 |
| Agent | inspector | `agents/inspector.md` | 52 |
| Script | _cli | `scripts/_cli.py` | 31 |
| Script | audit_project | `scripts/audit_project.py` | 508 |
| Script | bump_version | `scripts/bump_version.py` | 273 |
| Script | lint_skills | `scripts/lint_skills.py` | 691 |
| Script | scan_security | `scripts/scan_security.py` | 345 |
| Hook | session-start | `hooks/session-start` | 38 |
| Hook | run-hook.cmd | `hooks/run-hook.cmd` | 44 |
| Hook | hooks-cursor.json | `hooks/hooks-cursor.json` | — |
| Manifest | Claude Code | `.claude-plugin/plugin.json` | 20 |
| Manifest | Cursor | `.cursor-plugin/plugin.json` | 25 |
| Manifest | Codex | `.codex/INSTALL.md` | 44 |
| Manifest | OpenCode | `.opencode/plugins/bundles-forge.js` | 74 |
| Manifest | Gemini CLI | `gemini-extension.json` | 13 |

### C. Script Outputs

<details><summary>audit_project.py output</summary>

```
## Bundle-Plugin Audit: bundles-forge

### Status: WARN — Overall Score: 9.1/10

### Warnings (should fix)
- [T5] (testing) No test prompts for skill 'auditing'
- [T5] (testing) No test prompts for skill 'authoring'
- [T5] (testing) No test prompts for skill 'blueprinting'
- [T5] (testing) No test prompts for skill 'optimizing'
- [T5] (testing) No test prompts for skill 'porting'
- [T5] (testing) No test prompts for skill 'releasing'
- [T5] (testing) No test prompts for skill 'scaffolding'
- [T5] (testing) No test prompts for skill 'using-bundles-forge'
- [T8] (testing) No A/B eval results found in .bundles-forge/

### Info (consider)
- [G1] Circular dependency: auditing -> optimizing -> auditing (declared feedback loop)
- [G5] No matching artifact IDs between 'optimizing' outputs and 'auditing' inputs
- [G5] No matching artifact IDs between 'porting' outputs and 'auditing' inputs
- [G5] No matching artifact IDs between 'releasing' outputs and 'optimizing' inputs
- [G5] No matching artifact IDs between 'releasing' outputs and 'auditing' inputs
- [G5] No matching artifact IDs between 'scaffolding' outputs and 'auditing' inputs
- [Q12] blueprinting: SKILL.md has 300+ lines but no references/ files
- [Q12] optimizing: SKILL.md has 300+ lines but no references/ files

### Category Breakdown

| Category | Weight | Score | Critical | Warning | Info |
|----------|--------|-------|----------|---------|------|
| structure | 3 | 10/10 | 0 | 0 | 0 |
| manifests | 2 | 10/10 | 0 | 0 | 0 |
| version_sync | 3 | 10/10 | 0 | 0 | 0 |
| skill_quality | 2 | 10/10 | 0 | 0 | 9 |
| cross_references | 2 | 10/10 | 0 | 0 | 6 |
| hooks | 2 | 10/10 | 0 | 0 | 0 |
| testing | 2 | 1/10 | 0 | 9 | 0 |
| documentation | 1 | 10/10 | 0 | 0 | 0 |
| security | 3 | 10/10 | 0 | 0 | 0 |
```

</details>

<details><summary>scan_security.py output</summary>

```
## Security Scan: bundles-forge

Files scanned: 26
Risk summary: 0 critical, 0 warnings, 0 info

All 26 files clean — no security findings.
```

</details>

<details><summary>lint_skills.py output</summary>

```
## Skill Quality Lint

Skills checked: 8
Results: 0 critical, 0 warnings, 9 info

### Info
- [Q12] blueprinting: SKILL.md has 300+ lines but no references/ files
- [Q12] optimizing: SKILL.md has 300+ lines but no references/ files

### Per-Skill Summary

| Skill | Critical | Warnings | Info |
|-------|----------|----------|------|
| auditing | 0 | 0 | 0 |
| authoring | 0 | 0 | 0 |
| blueprinting | 0 | 0 | 1 |
| optimizing | 0 | 0 | 1 |
| porting | 0 | 0 | 0 |
| releasing | 0 | 0 | 0 |
| scaffolding | 0 | 0 | 0 |
| using-bundles-forge | 0 | 0 | 0 |
```

</details>

<details><summary>bump_version.py --check output</summary>

```
Version check:

  package.json (version)                         1.5.1
  .claude-plugin/plugin.json (version)           1.5.1
  .claude-plugin/marketplace.json (plugins.0.version)  1.5.1
  .cursor-plugin/plugin.json (version)           1.5.1
  gemini-extension.json (version)                1.5.1

All declared files are in sync at 1.5.1
```

</details>

<details><summary>bump_version.py --audit output</summary>

```
Version check:

  package.json (version)                         1.5.1
  .claude-plugin/plugin.json (version)           1.5.1
  .claude-plugin/marketplace.json (plugins.0.version)  1.5.1
  .cursor-plugin/plugin.json (version)           1.5.1
  gemini-extension.json (version)                1.5.1

All declared files are in sync at 1.5.1

Audit: scanning repo for version string '1.5.1'...

No undeclared files contain the version string. All clear.
```

</details>
