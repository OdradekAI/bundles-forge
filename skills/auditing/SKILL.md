---
name: auditing
description: "Use when reviewing a bundle-plugin for structural issues, version drift, skill quality, workflow integration, or security risks — before releasing, after changes, or after adding skills. Auto-detects scope (full project vs skill vs workflow)"
allowed-tools: Bash(bundles-forge audit-skill *) Bash(bundles-forge audit-security *) Bash(bundles-forge audit-docs *) Bash(bundles-forge audit-plugin *) Bash(bundles-forge audit-workflow *) Bash(bundles-forge checklists *) Bash(bundles-forge bump-version *) Bash(python *bundles-forge *)
---

# Auditing Bundle-Plugins

## Overview

Systematically evaluate a bundle-plugin project or a single skill across applicable quality categories — including security scanning — score each, and produce a diagnostic report. This skill is a pure diagnostic tool: it identifies and reports issues but does not orchestrate fixes.

**Core principle:** Measure and report. A scored audit gives orchestrating skills (blueprinting, optimizing, releasing) the information they need to decide what to fix. When sources contradict, apply the authority hierarchy in `references/source-of-truth-policy.md`.

**This skill includes security scanning.** No need to invoke a separate security skill — see Category 10 under Full Project Audit.

**Announce at start:** "I'm using the auditing skill to audit [this project / this skill]."

**Plugin context:** When installed as a plugin, operate on the user's project (`$CLAUDE_PROJECT_DIR` / `<target-dir>`), not the plugin's own cache. Read files from and detect scope in the target; write all outputs (reports, JSON baselines) to the workspace's `.bundles-forge/audits/`. See `references/input-normalization.md` for edge-case input types, naming conventions, and security rules. `<plugin-root>` in commands below resolves to `$CLAUDE_PLUGIN_ROOT` (Claude Code), `$CURSOR_PLUGIN_ROOT` (Cursor), or `.` (local development).

## Resolve Input & Detect Scope

The target can be a local path, a GitHub URL, or a zip file. Normalize to a local directory, then detect scope. This applies to all three audit modes.

### Input Normalization

**This is a mandatory step — do not skip it or improvise paths.** Resolve the target to a local directory before proceeding to Scope Detection or any audit Step 1.

1. **Resolve the workspace.** The workspace is `$CLAUDE_PROJECT_DIR` or `$CURSOR_PROJECT_DIR` (plugin mode), falling back to the current working directory.
2. **Normalize the target by type:**
   - **Local path** — use directly; no transformation needed.
   - **GitHub URL** — parse `<owner>` and `<repo>` from the URL. Shallow-clone to `<workspace>/.bundles-forge/repos/<owner>__<repo>/` using `--depth 1 --no-checkout`, then run `git checkout`. If the directory already exists, append a `__<YYYYMMDD>` timestamp to avoid collisions. **Do not clone to `/tmp/`, `~/`, or any path outside `.bundles-forge/repos/`.**
   - **Zip/tar.gz** — extract to `<workspace>/.bundles-forge/repos/<archive-name>/`.
3. **Create the target subdirectory** if it does not exist.
4. **On failure** (network error, 404, auth required, rate limit): tell the user what failed and suggest providing a local path or zip file instead. Do not silently skip or proceed with partial data.

See `references/input-normalization.md` for the full naming convention (version/timestamp suffixes), GitHub subdirectory URLs, and security rules.

### Scope Detection

After normalization, determine the audit scope from the resolved local path:

| Target | How to Detect | Mode |
|--------|--------------|------|
| Project root | Has `skills/` directory | **Full audit** — all 10 categories |
| Project root + workflow request | User explicitly requests workflow audit, or specifies `--focus-skills` | **Workflow audit** — 3-layer workflow checks (W1-W11) |
| Single skill directory | Contains `SKILL.md` but no `skills/` subdirectory | **Skill audit** — 4 applicable categories |
| Single SKILL.md file | Path ends in `SKILL.md` | **Skill audit** — 4 applicable categories |

**If the target is a single skill, skip to the Skill Audit section below.**
**If a workflow audit is requested, skip to the Workflow Audit section below.**

---

## Full Project Audit

`audit-plugin` orchestrates `audit-security` (security), `audit-skill` (skill quality), `audit-workflow` (workflow integration), and `audit-docs` (documentation consistency D1-D9), then adds structure, manifest, version-sync, hook, and testing checks.

**Categories at a glance** (see `references/plugin-checklist.md` for 60+ individual checks):

| Category | Weight |
|----------|--------|
| Structure | High |
| Platform Manifests | Medium |
| Version Sync | High |
| Skill Quality | Medium |
| Cross-References | Medium |
| Workflow | High |
| Hooks | Medium |
| Testing | Medium |
| Documentation | Low |
| Security | High |

**Security Scan (Category 10):** Scans 7 attack surfaces. See `references/security-checklist.md` for the full pattern list. `security-checklist.md` is the canonical source; the table below is a quick-reference summary.

| Target | Risk Level |
|--------|-----------|
| SKILL.md content | High |
| Hook scripts | High |
| Hook configs (HTTP hooks) | High |
| OpenCode plugins | High |
| Agent prompts | Medium |
| Bundled scripts | Medium |
| MCP configs | Medium |

### Step 1 — Run Script Baseline

**Prerequisites:** Target directory resolved to a local path (via Input Normalization above) with a `skills/` directory (Full audit scope confirmed).

**Action:**

```bash
bundles-forge audit-plugin --json --output-dir .bundles-forge/audits <target-dir>
```

This collects the deterministic baseline — structure, manifests, version sync, skill quality, cross-references, hooks, documentation, and security patterns are verified with reproducible results regardless of agent behavior.

**Expected Output:** A JSON baseline file at `.bundles-forge/audits/audit_plugin-<YYYYMMDD-HHmmss>.json`. Verify the file exists and is valid JSON before proceeding to Step 2.

**Failure Handling:**
- **Exit code 0/1/2 with valid JSON file:** Proceed to Step 2. Exit 1 = warnings, exit 2 = critical findings — both are valid baselines.
- **Exit code non-0/1/2 or stdout empty:** Retry with `python "<plugin-root>/bin/bundles-forge" audit-plugin --json --output-dir .bundles-forge/audits <target-dir>`. If both fail, check Python version (requires 3.9+), report the traceback and stop.

### Step 2 — Dispatch Auditor

**Prerequisites:** JSON baseline file from Step 1 exists at `.bundles-forge/audits/`.

**Action:** Pass the JSON baseline file contents to the `auditor` agent (`agents/auditor.md`) as input context. The auditor is the single source of truth for scoring formula, report format, and qualitative assessment criteria. It adds ±2 qualitative score adjustments, narrative evaluation, and compiles a layered report using `references/plugin-report-template.md`.

Full execution details — category weights, scoring formula, report format, Go/No-Go logic — are defined in `agents/auditor.md` and supported by checklists in `references/`.

When auditing a project created by `bundles-forge:blueprinting`, the auditor may reference the design document's "Success Criteria" section (if present in `.bundles-forge/blueprints/` or project root) to evaluate whether the implementation aligns with the original project goals.

**Expected Output:** The auditor produces:
1. A scored audit report saved to `.bundles-forge/audits/<project-name>-v<version>-audit.<date>.md` — must follow the template structure in `references/plugin-report-template.md`
2. Per-skill breakdowns with Verdict, Strengths, and Key Issues
3. A Go/No-Go recommendation with qualitative adjustment rationale

**Failure Handling:**
- **Subagent dispatch unavailable:** Ask the user — "Subagents are not available. I can run the audit checks inline. Proceed inline?" If confirmed, read `agents/auditor.md` and follow its execution instructions within this conversation context, using the JSON baseline file as input. The agent file contains the complete audit protocol. The inline execution must still produce all three expected outputs listed above.
- **Auditor returns without saving report:** The report file in `.bundles-forge/audits/` is a mandatory output. If the auditor did not save it, save the report yourself following the naming convention in `agents/auditor.md`.

### Step 3 — Behavioral Verification (W10-W11)

**Prerequisites:** Step 2 complete. The audit report exists in `.bundles-forge/audits/`.

**Action:** Decide whether to run behavioral verification:
- **Run when:** Pre-release audits, or when the Workflow category (W1-W9) has warnings that suggest structural issues may affect runtime behavior.
- **Skip when:** Quick post-change checks, when evaluator dispatch is unavailable, or when static and semantic layers show no issues.

If running: dispatch `evaluator` agent (`agents/evaluator.md`) with label "chain" for each workflow chain. Append evaluator results to the audit report.

If skipping: add the following to the Behavioral Verification section of the audit report: "Not performed. Reason: `<reason>`. Scored as N/A (excluded from weighted average)."

**Expected Output:** The audit report's Behavioral Verification (W10-W11) section is filled — either with evaluation results or with an explicit N/A entry and skip reason. This section must never be left blank or omitted.

**Failure Handling:**
- **Evaluator dispatch unavailable:** Mark as N/A with reason "evaluator agents unavailable". Do not leave the section empty.
- **Evaluator returns errors:** Include the error details in the report section and score as N/A.

### Step 4 — Verify Final Report

**Prerequisites:** Steps 1-3 complete.

**Action:** Verify the audit report in `.bundles-forge/audits/` meets these criteria:
1. File exists and follows the naming convention
2. Contains Decision Brief with Go/No-Go recommendation
3. Contains all 10 category scores
4. Contains Behavioral Verification section (results or N/A)
5. Contains per-skill breakdowns

Present all findings grouped by severity (Critical / Warning / Info). The audit report is the final output — the calling context decides what to fix and how.

**Expected Output:** A complete, validated audit report file in `.bundles-forge/audits/`.

**Failure Handling:**
- **Report missing required sections:** Go back to Step 2 and re-run the auditor with explicit instructions to include the missing sections.

---

## Skill Audit (Lightweight Mode)

When the target is a single skill directory or SKILL.md file, run only the 4 categories that apply at skill scope. This is auto-detected — no special flags needed.

| Category | Checks Run | What It Catches |
|----------|-----------|----------------|
| Structure | S2, S3, S9 | Skill has own directory, contains SKILL.md, directory name matches frontmatter `name` |
| Skill Quality | Q1–Q15 | Frontmatter validity, description conventions, token budget, allowed-tools deps, section structure, conditional block reachability |
| Cross-References | X1, X2, X3 | Outgoing `project:skill-name` refs resolve, relative paths exist, referenced subdirectories exist |
| Security | SC1, SC9, SC13, AG1, AG6 | Sensitive file access, safety overrides, encoding tricks, scope constraints (IDs from `security-checklist.md`) |

**Skipped categories:** Platform Manifests, Version Sync, Hooks, Testing, Documentation — these require project-level context.

### Step 1 — Run Script Baseline

**Prerequisites:** Target resolved to a local path (via Input Normalization above) containing `SKILL.md` but no `skills/` subdirectory.

**Action:**

```bash
bundles-forge audit-skill --json --output-dir .bundles-forge/audits <skill-directory>
```

Also accepts a `SKILL.md` file path directly.

**Expected Output:** A JSON baseline file at `.bundles-forge/audits/audit_skill-<YYYYMMDD-HHmmss>.json`.

**Failure Handling:**
- **Exit code 0/1/2 with valid JSON file:** Proceed to Step 2.
- **Exit code non-0/1/2 or stdout empty:** Retry with `python "<plugin-root>/bin/bundles-forge" audit-skill --json --output-dir .bundles-forge/audits <skill-directory>`. If both fail, check Python version (requires 3.9+), report the traceback and stop.

### Step 2 — Dispatch Auditor (Skill Mode)

**Prerequisites:** JSON baseline file from Step 1 exists.

**Action:** Pass the JSON baseline to the `auditor` agent (`agents/auditor.md`) in Single Skill Audit Mode. The auditor runs the 4-category checks, produces a qualitative summary (Verdict, Strengths, Key Issues), scores each category, and compiles the report using `references/skill-report-template.md`.

**Expected Output:** A skill audit report saved to `.bundles-forge/audits/<skill-name>-v<version>-skill-audit.<date>.md` containing:
1. Decision Brief with Verdict, Strengths, Key Issues
2. Findings by Category (4 categories)
3. Skill Profile

**Failure Handling:**
- **Subagent dispatch unavailable:** Ask the user — "Subagents are not available. I can run the skill audit checks inline. Proceed?" If confirmed, read `agents/auditor.md` (Single Skill Audit Mode section) and follow its instructions inline. The inline execution must still produce all expected outputs.
- **Auditor returns without saving report:** Save the report yourself following the naming convention.

### Step 3 — Verify Final Report

**Prerequisites:** Step 2 complete.

**Action:** Verify the skill audit report exists in `.bundles-forge/audits/` and contains Decision Brief, 4 category findings, and Skill Profile.

**Expected Output:** A complete skill audit report file.

**Failure Handling:**
- **Report missing sections:** Re-run Step 2 with explicit instructions to include missing sections.

### Third-Party Skill Scanning

When auditing a skill from an external source (marketplace, git, shared file):

1. Clone/download the skill **without executing** any hooks or scripts
2. Run the skill audit on the downloaded content
3. Pay special attention to Security checks — third-party skills are the primary threat vector
4. Review all critical/warning findings with the user before installation
5. Never auto-install a skill that has unresolved critical security findings

---

## Workflow Audit

When the user explicitly requests a workflow audit, or when the Full audit's Cross-References category (X1-X3) or Workflow category (W1-W11) has warnings, run a dedicated workflow audit. This evaluates how skills connect, hand off artifacts, and compose into coherent chains.

**When to Trigger:**
- User explicitly requests "audit the workflow" or "check workflow integration"
- After adding skills to an existing project
- After modifying Integration sections, Inputs/Outputs, or adding new skills to a chain
- When the Full audit's Workflow category shows warnings — suggest: "Workflow issues detected. Run a focused workflow audit with `--focus-skills` for detailed diagnostics."

### Step 1 — Run Script Baseline

**Prerequisites:** Target directory resolved to a local path (via Input Normalization above). User has optionally specified `--focus-skills`.

**Action:**

```bash
bundles-forge audit-workflow --json --output-dir .bundles-forge/audits <target-dir>
# or with focus:
bundles-forge audit-workflow --json --output-dir .bundles-forge/audits --focus-skills skill-a,skill-b <target-dir>
```

Script mode covers W1-W9 (static + semantic layers). W10-W11 (behavioral layer) requires evaluator agent dispatch and is scored as N/A in script output.

**Expected Output:** A JSON baseline file at `.bundles-forge/audits/audit_workflow-<YYYYMMDD-HHmmss>.json`.

**Failure Handling:**
- **Exit code 0/1/2 with valid JSON file:** Proceed to Step 2.
- **Exit code non-0/1/2 or stdout empty:** Retry with `python "<plugin-root>/bin/bundles-forge" audit-workflow --json --output-dir .bundles-forge/audits <target-dir>`. If both fail, check Python version (requires 3.9+), report the traceback and stop.

### Step 2 — Dispatch Auditor (Workflow Mode)

**Prerequisites:** JSON baseline file from Step 1 exists.

**Action:** Pass the JSON baseline to the `auditor` agent (`agents/auditor.md`) in Workflow Audit Mode. The auditor handles W1-W9 (Static Structure + Semantic Interface) across three layers defined in `references/workflow-checklist.md`. Full workflow audit protocol, focus mode, and report format are in `agents/auditor.md` (Workflow Audit Mode section).

**Expected Output:** A workflow audit report saved to `.bundles-forge/audits/<project-name>-v<version>-workflow-audit.<date>.md` using `references/workflow-report-template.md`, containing:
1. Decision Brief with Go/No-Go recommendation
2. Findings by Layer (Static, Semantic, Behavioral)
3. Skill Integration Map

**Failure Handling:**
- **Subagent dispatch unavailable:** Ask the user — "Subagents are not available. I can run the workflow checks inline. Proceed?" If confirmed, read `agents/auditor.md` (Workflow Audit Mode section) and follow its instructions inline. Must still produce all expected outputs.
- **Auditor returns without saving report:** Save the report yourself following the naming convention.

### Step 3 — Behavioral Verification (W10-W11)

**Prerequisites:** Step 2 complete. The workflow report exists.

**Action:** Decide whether to run behavioral verification:
- **Run when:** Pre-release audits, or when W1-W9 has warnings suggesting runtime behavior issues.
- **Skip when:** Quick checks, evaluator dispatch unavailable, or static+semantic layers clean.

If running: dispatch `evaluator` agent (`agents/evaluator.md`) with label "chain" for each workflow chain involving focus skills. Use the chain list and focus skills from the auditor's report. Append results to the workflow report.

If skipping: add to the Behavioral Verification section: "Not performed. Reason: `<reason>`. Scored as N/A (excluded from weighted average)."

**Why two phases:** Subagents cannot dispatch other subagents, so the evaluator must be dispatched from this skill (main conversation), not from within the auditor.

**Expected Output:** The workflow report's Behavioral Verification (W10-W11) section is filled — either with evaluation results or an explicit N/A entry. This section must never be left blank or omitted.

**Failure Handling:**
- **Evaluator dispatch unavailable:** Mark as N/A with reason "evaluator agents unavailable".
- **Evaluator errors:** Include error details and score as N/A.

### Step 4 — Verify Final Report

**Prerequisites:** Steps 1-3 complete.

**Action:** Verify the workflow report in `.bundles-forge/audits/` contains Decision Brief, all three layer findings (with Behavioral Verification filled), and Skill Integration Map.

Present workflow findings grouped by severity. The `workflow-report` is consumed by the calling context for targeted fixes.

**Expected Output:** A complete workflow audit report file.

**Failure Handling:**
- **Report missing sections:** Re-run Step 2 with explicit instructions to include missing sections.

---

## Security-Only Mode

When the user explicitly requests a security-only scan, run only Category 10 (Security) via `bundles-forge audit-security`. Skip Categories 1-9. Report in the same format but with only the Security category scored. This provides a quick security check without the overhead of a full 10-category audit.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping version sync check | Always run `bundles-forge bump-version --check` (full audit) |
| Not checking description anti-patterns | Descriptions that summarize workflow cause agents to shortcut |
| Ignoring cross-reference resolution | Broken `project:skill-name` refs = broken workflow chains |
| Running full 10-category audit on a single skill | Let scope auto-detection handle it — 6 categories don't apply |
| Skipping workflow audit after adding third-party skills | New skills need workflow integration validation — use `--focus-skills` |
| Skipping security because "I wrote it myself" | Accidental vulnerabilities are common — always scan |
| Only scanning SKILL.md, ignoring hooks | Hooks are the highest-risk executable code (full audit) |
| Treating script output as the final report | Script output is a baseline — always dispatch auditor or read `agents/auditor.md` inline to produce the full report |
| Bypassing `--json` failure without diagnosis | If `--json` returns empty output or unexpected exit code, retry with the direct Python call before falling back to non-JSON mode |
| Not persisting JSON baseline to disk | Always use `--output-dir .bundles-forge/audits` to ensure intermediate results are saved regardless of agent behavior |
| Skipping W10-W11 without marking N/A in report | If Behavioral Verification is skipped, the report must contain the section with "N/A" and the skip reason |

## Inputs

- `project-directory` (required) — bundle-plugin project root, single skill directory, or SKILL.md file path (local, GitHub URL, or archive)

## Outputs

- `audit-report` — scored report with findings across 10 categories (full project), written to `.bundles-forge/audits/` by the auditor agent. Contains per-skill breakdowns
- `skill-report` (skill mode) — 4-category scored report (Structure, Quality, Cross-Refs, Security) for a single skill, written to `.bundles-forge/audits/`
- `workflow-report` (workflow mode) — workflow-specific report with W1-W11 findings across static/semantic/behavioral layers, written to `.bundles-forge/audits/`

## Integration

**Called by:**
- **bundles-forge:blueprinting** — Phase 4: initial quality check on new projects
- **bundles-forge:optimizing** — post-change verification after applying optimizations
- **bundles-forge:releasing** — pre-release quality and security check
- User directly — standalone audit of any project or skill
