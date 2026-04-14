# Cross-Skill CLI Dispatcher Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace all hardcoded `python skills/X/scripts/Y.py` paths with a unified `bundles-forge <subcommand>` CLI dispatcher in `bin/`, so cross-skill script calls work after marketplace installation.

**Architecture:** A single `bin/bundles-forge` Python script routes subcommands to target scripts via `subprocess.call`, propagating exit codes and stdout/stderr unchanged. A `bin/bundles-forge.cmd` wrapper provides Windows compatibility. All SKILL.md files, reference docs, and CLAUDE.md switch from direct script paths to the dispatcher.

**Tech Stack:** Python 3.9+ (matches existing project requirement), subprocess, pathlib.

---

## File Structure

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `bin/bundles-forge` | CLI dispatcher — routes subcommands to scripts |
| Create | `bin/bundles-forge.cmd` | Windows wrapper for the dispatcher |
| Modify | `skills/auditing/SKILL.md` | Update allowed-tools + body references |
| Modify | `skills/authoring/SKILL.md` | Update allowed-tools + body references |
| Modify | `skills/optimizing/SKILL.md` | Update allowed-tools + body references |
| Modify | `skills/scaffolding/SKILL.md` | Update allowed-tools + body references |
| Modify | `skills/releasing/SKILL.md` | Update allowed-tools + body references |
| Modify | `skills/authoring/references/quality-checklist.md` | Update script path references |
| Modify | `skills/scaffolding/references/project-anatomy.md` | Update script path references |
| Modify | `skills/scaffolding/references/external-integration.md` | Update script path references |
| Modify | `skills/auditing/references/skill-checklist.md` | Update script path references |
| Modify | `skills/auditing/references/plugin-checklist.md` | Update script path references |
| Modify | `skills/auditing/references/workflow-checklist.md` | Update script path references |
| Modify | `CLAUDE.md` | Update Commands section + Key Conventions |

---

### Task 1: Create the CLI Dispatcher

**Files:**
- Create: `bin/bundles-forge`

- [ ] **Step 1: Create `bin/` directory and write the dispatcher**

```python
#!/usr/bin/env python3
"""bundles-forge CLI - unified cross-skill script dispatcher.

Routes subcommands to the correct script inside the plugin.
Uses subprocess.call to preserve __file__ semantics, exit codes,
and stdout/stderr pass-through.

Usage:
    bundles-forge <command> [args...]
    bundles-forge -h | --help
"""
import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent

COMMANDS = {
    "audit-skill":    _ROOT / "skills" / "auditing" / "scripts" / "audit_skill.py",
    "audit-security": _ROOT / "skills" / "auditing" / "scripts" / "audit_security.py",
    "audit-docs":     _ROOT / "skills" / "auditing" / "scripts" / "audit_docs.py",
    "audit-plugin":   _ROOT / "skills" / "auditing" / "scripts" / "audit_plugin.py",
    "audit-workflow": _ROOT / "skills" / "auditing" / "scripts" / "audit_workflow.py",
    "checklists":     _ROOT / "skills" / "auditing" / "scripts" / "generate_checklists.py",
    "bump-version":   _ROOT / "skills" / "releasing" / "scripts" / "bump_version.py",
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: bundles-forge <command> [args...]")
        print()
        print("Commands:")
        for name in COMMANDS:
            print(f"  {name}")
        sys.exit(0)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    script = COMMANDS.get(cmd)
    if script is None:
        print(f"bundles-forge: unknown command '{cmd}'", file=sys.stderr)
        print(f"Available: {', '.join(COMMANDS)}", file=sys.stderr)
        sys.exit(1)

    if not script.exists():
        print(f"bundles-forge: script not found: {script}", file=sys.stderr)
        sys.exit(1)

    sys.exit(subprocess.call([sys.executable, str(script)] + args))


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Make it executable**

Run: `chmod +x bin/bundles-forge`

- [ ] **Step 3: Verify the dispatcher works**

Run: `python bin/bundles-forge --help`
Expected: help text listing all 7 commands, exit code 0.

Run: `python bin/bundles-forge audit-skill bin/bundles-forge`
Expected: audit output for the bin/ directory (likely with findings since it's not a skill), exit code 0 or 1.

Run: `python bin/bundles-forge unknown-cmd`
Expected: stderr message "bundles-forge: unknown command 'unknown-cmd'", exit code 1.

- [ ] **Step 4: Commit**

```bash
git add bin/bundles-forge
git commit -m "feat: add bin/bundles-forge CLI dispatcher for cross-skill scripts"
```

---

### Task 2: Create the Windows Wrapper

**Files:**
- Create: `bin/bundles-forge.cmd`

- [ ] **Step 1: Write the Windows batch wrapper**

```
@echo off
python "%~dp0bundles-forge" %*
```

- [ ] **Step 2: Verify on Windows**

Run: `bin\bundles-forge.cmd --help`
Expected: same help text as Task 1 Step 3.

- [ ] **Step 3: Commit**

```bash
git add bin/bundles-forge.cmd
git commit -m "feat: add Windows wrapper for bundles-forge CLI"
```

---

### Task 3: Update SKILL.md allowed-tools Declarations

**Files:**
- Modify: `skills/auditing/SKILL.md:4`
- Modify: `skills/authoring/SKILL.md:4`
- Modify: `skills/optimizing/SKILL.md:4`
- Modify: `skills/scaffolding/SKILL.md:4`
- Modify: `skills/releasing/SKILL.md:4`

- [ ] **Step 1: Update `skills/auditing/SKILL.md` line 4**

Old:
```yaml
allowed-tools: Bash(python skills/auditing/scripts/*)
```

New:
```yaml
allowed-tools: Bash(bundles-forge audit-skill *) Bash(bundles-forge audit-security *) Bash(bundles-forge audit-docs *) Bash(bundles-forge audit-plugin *) Bash(bundles-forge audit-workflow *) Bash(bundles-forge checklists *) Bash(bundles-forge bump-version *)
```

- [ ] **Step 2: Update `skills/authoring/SKILL.md` line 4**

Old:
```yaml
allowed-tools: Python(skills/auditing/scripts/audit_skill.py *)
```

New:
```yaml
allowed-tools: Bash(bundles-forge audit-skill *)
```

- [ ] **Step 3: Update `skills/optimizing/SKILL.md` line 4**

Old:
```yaml
allowed-tools: Python(skills/auditing/scripts/*)
```

New:
```yaml
allowed-tools: Bash(bundles-forge audit-skill *) Bash(bundles-forge audit-security *) Bash(bundles-forge audit-docs *) Bash(bundles-forge audit-plugin *) Bash(bundles-forge audit-workflow *) Bash(bundles-forge checklists *) Bash(bundles-forge bump-version *)
```

- [ ] **Step 4: Update `skills/scaffolding/SKILL.md` line 4**

Old:
```yaml
allowed-tools: Python(skills/releasing/scripts/bump_version.py *)
```

New:
```yaml
allowed-tools: Bash(bundles-forge bump-version *)
```

- [ ] **Step 5: Update `skills/releasing/SKILL.md` line 4**

Old:
```yaml
allowed-tools: Python(skills/releasing/scripts/bump_version.py *) Python(skills/auditing/scripts/audit_plugin.py *) Python(skills/auditing/scripts/audit_docs.py *)
```

New:
```yaml
allowed-tools: Bash(bundles-forge bump-version *) Bash(bundles-forge audit-plugin *) Bash(bundles-forge audit-docs *)
```

- [ ] **Step 6: Commit**

```bash
git add skills/auditing/SKILL.md skills/authoring/SKILL.md skills/optimizing/SKILL.md skills/scaffolding/SKILL.md skills/releasing/SKILL.md
git commit -m "refactor: update SKILL.md allowed-tools to use bundles-forge CLI"
```

---

### Task 4: Update SKILL.md Body References

**Files:**
- Modify: `skills/auditing/SKILL.md` (lines 59-60, 67, 136-138, 171-173, 201)
- Modify: `skills/authoring/SKILL.md` (lines 111, 130)
- Modify: `skills/optimizing/SKILL.md` (lines 80-81, 148-149, 192, 309)
- Modify: `skills/scaffolding/SKILL.md` (lines 121, 133, 141, 165)
- Modify: `skills/releasing/SKILL.md` (lines 64-65, 70, 135, 171-173)

- [ ] **Step 1: Update `skills/auditing/SKILL.md`**

Replace all occurrences using these exact patterns:

| Line | Old | New |
|------|-----|-----|
| 59 | `python skills/auditing/scripts/audit_plugin.py <project-root>` | `bundles-forge audit-plugin <project-root>` |
| 60 | `python skills/auditing/scripts/audit_plugin.py --json <project-root>` | `bundles-forge audit-plugin --json <project-root>` |
| 67 | `python skills/auditing/scripts/audit_plugin.py --json <project-root>` | `bundles-forge audit-plugin --json <project-root>` |
| 136 | `python skills/auditing/scripts/audit_skill.py <skill-directory>` | `bundles-forge audit-skill <skill-directory>` |
| 137 | `python skills/auditing/scripts/audit_skill.py <path>/SKILL.md` | `bundles-forge audit-skill <path>/SKILL.md` |
| 138 | `python skills/auditing/scripts/audit_skill.py --json <skill-directory>` | `bundles-forge audit-skill --json <skill-directory>` |
| 171 | `python skills/auditing/scripts/audit_workflow.py <project-root>` | `bundles-forge audit-workflow <project-root>` |
| 172 | `python skills/auditing/scripts/audit_workflow.py --focus-skills skill-a,skill-b <root>` | `bundles-forge audit-workflow --focus-skills skill-a,skill-b <root>` |
| 173 | `python skills/auditing/scripts/audit_workflow.py --json <project-root>` | `bundles-forge audit-workflow --json <project-root>` |
| 201 | `python skills/releasing/scripts/bump_version.py --check` | `bundles-forge bump-version --check` |

- [ ] **Step 2: Update `skills/authoring/SKILL.md`**

| Line | Old | New |
|------|-----|-----|
| 111 | `python skills/auditing/scripts/audit_skill.py <skill-directory>` | `bundles-forge audit-skill <skill-directory>` |
| 130 | `audit_skill.py` (in prose, Common Mistakes table) | `bundles-forge audit-skill` |

- [ ] **Step 3: Update `skills/optimizing/SKILL.md`**

| Line | Old | New |
|------|-----|-----|
| 80 | `python skills/auditing/scripts/audit_skill.py <project-root>` | `bundles-forge audit-skill <project-root>` |
| 81 | `python skills/auditing/scripts/audit_skill.py --json <project-root>` | `bundles-forge audit-skill --json <project-root>` |
| 148 | `python skills/auditing/scripts/audit_workflow.py <project-root>` | `bundles-forge audit-workflow <project-root>` |
| 149 | `python skills/auditing/scripts/audit_workflow.py --focus-skills skill-a,skill-b <root>` | `bundles-forge audit-workflow --focus-skills skill-a,skill-b <root>` |
| 192 | `python skills/auditing/scripts/audit_security.py <project-root>` | `bundles-forge audit-security <project-root>` |
| 309 | `python skills/auditing/scripts/audit_skill.py <skill-directory>` | `bundles-forge audit-skill <skill-directory>` |

- [ ] **Step 4: Update `skills/scaffolding/SKILL.md`**

| Line | Old | New |
|------|-----|-----|
| 121 | `python skills/releasing/scripts/bump_version.py --check` | `bundles-forge bump-version --check` |
| 133 | `python skills/releasing/scripts/bump_version.py --check` | `bundles-forge bump-version --check` |
| 141 | `python skills/releasing/scripts/bump_version.py --check` | `bundles-forge bump-version --check` |
| 165 | `python skills/auditing/scripts/audit_skill.py <project-root>` | `bundles-forge audit-skill <project-root>` |

- [ ] **Step 5: Update `skills/releasing/SKILL.md`**

| Line | Old | New |
|------|-----|-----|
| 64 | `python skills/releasing/scripts/bump_version.py <project-root> --check` | `bundles-forge bump-version <project-root> --check` |
| 65 | `python skills/auditing/scripts/audit_docs.py <project-root>` | `bundles-forge audit-docs <project-root>` |
| 70 | `python skills/auditing/scripts/audit_plugin.py <project-root>` | `bundles-forge audit-plugin <project-root>` |
| 135 | `python skills/releasing/scripts/bump_version.py <project-root> <new-version>` | `bundles-forge bump-version <project-root> <new-version>` |
| 171 | `python skills/releasing/scripts/bump_version.py <project-root> --check` | `bundles-forge bump-version <project-root> --check` |
| 172 | `python skills/releasing/scripts/bump_version.py <project-root> --audit` | `bundles-forge bump-version <project-root> --audit` |
| 173 | `python skills/auditing/scripts/audit_docs.py <project-root>` | `bundles-forge audit-docs <project-root>` |

- [ ] **Step 6: Commit**

```bash
git add skills/auditing/SKILL.md skills/authoring/SKILL.md skills/optimizing/SKILL.md skills/scaffolding/SKILL.md skills/releasing/SKILL.md
git commit -m "refactor: update SKILL.md body references to use bundles-forge CLI"
```

---

### Task 5: Update Reference Docs

**Files:**
- Modify: `skills/authoring/references/quality-checklist.md` (lines 1, 47-49)
- Modify: `skills/scaffolding/references/project-anatomy.md` (lines 281-283)
- Modify: `skills/scaffolding/references/external-integration.md` (lines 25-26)
- Modify: `skills/auditing/references/skill-checklist.md` (line 94)
- Modify: `skills/auditing/references/plugin-checklist.md` (lines 93-94, 100)
- Modify: `skills/auditing/references/workflow-checklist.md` (line 45)

- [ ] **Step 1: Update `skills/authoring/references/quality-checklist.md`**

Line 1 — change the description sentence:
Old: `skills/auditing/scripts/audit_skill.py` automates these checks.
New: `bundles-forge audit-skill` automates these checks.

Lines 47-49 — replace the code block:
```bash
bundles-forge audit-skill <skill-directory>          # single skill
bundles-forge audit-skill <project-root>             # all skills
bundles-forge audit-skill --json <project-root>      # machine-readable
```

- [ ] **Step 2: Update `skills/scaffolding/references/project-anatomy.md`**

Lines 281-283 — replace:
Old:
```
- `python skills/releasing/scripts/bump_version.py <version>` — update all declared files
- `python skills/releasing/scripts/bump_version.py --check` — detect drift between files
- `python skills/releasing/scripts/bump_version.py --audit` — check + scan repo for undeclared version strings
```

New:
```
- `bundles-forge bump-version <version>` — update all declared files
- `bundles-forge bump-version --check` — detect drift between files
- `bundles-forge bump-version --audit` — check + scan repo for undeclared version strings
```

- [ ] **Step 3: Update `skills/scaffolding/references/external-integration.md`**

Line 25 — change table cell:
Old: `python skills/auditing/scripts/audit_skill.py`
New: `bundles-forge audit-skill`

Line 26 — change table cell:
Old: `python skills/releasing/scripts/bump_version.py`
New: `bundles-forge bump-version`

- [ ] **Step 4: Update `skills/auditing/references/skill-checklist.md`**

Line 94 — change the instruction:
Old: `Run \`python skills/auditing/scripts/audit_skill.py <skill-directory>\` — results include X1-X3 findings`
New: `Run \`bundles-forge audit-skill <skill-directory>\` — results include X1-X3 findings`

- [ ] **Step 5: Update `skills/auditing/references/plugin-checklist.md`**

Line 93 — change table cell:
Old: `python skills/releasing/scripts/bump_version.py --check` exits 0
New: `bundles-forge bump-version --check` exits 0

Line 94 — change table cell:
Old: `python skills/releasing/scripts/bump_version.py --audit` finds no undeclared version strings
New: `bundles-forge bump-version --audit` finds no undeclared version strings

Line 100 — change code block:
```bash
bundles-forge bump-version --check
```

- [ ] **Step 6: Update `skills/auditing/references/workflow-checklist.md`**

Line 45 — change code block:
```bash
bundles-forge audit-skill --json <project-root>
```

- [ ] **Step 7: Commit**

```bash
git add skills/authoring/references/quality-checklist.md skills/scaffolding/references/project-anatomy.md skills/scaffolding/references/external-integration.md skills/auditing/references/skill-checklist.md skills/auditing/references/plugin-checklist.md skills/auditing/references/workflow-checklist.md
git commit -m "refactor: update reference docs to use bundles-forge CLI"
```

---

### Task 6: Update CLAUDE.md

**Files:**
- Modify: `CLAUDE.md` (lines 26-35, 42-44, 109-112)

- [ ] **Step 1: Update the Quality & Security section (lines 26-35)**

Old:
```bash
python skills/auditing/scripts/audit_skill.py [project-root]       # project-level skill quality audit (auto-detects mode)
python skills/auditing/scripts/audit_skill.py [skill-dir]          # single skill audit (4 categories)
python skills/auditing/scripts/audit_skill.py --all [project-root] # force project-level mode
python skills/auditing/scripts/audit_security.py [project-root]     # 7-surface security scan
python skills/auditing/scripts/audit_plugin.py [project-root]     # combined audit (calls audit_skill + audit_security + workflow)
python skills/auditing/scripts/audit_workflow.py [project-root]    # workflow integration audit (W1-W11)
python skills/auditing/scripts/audit_docs.py [project-root]        # documentation consistency (9 checks: D1-D9)
python skills/auditing/scripts/generate_checklists.py [project-root]        # regenerate checklist tables from audit-checks.json registry
python skills/auditing/scripts/generate_checklists.py --check [project-root] # detect checklist drift (exit 1 if stale)
```

New:
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

- [ ] **Step 2: Update the Version Management section (lines 42-44)**

Old:
```bash
python skills/releasing/scripts/bump_version.py --check             # detect version drift across manifests
python skills/releasing/scripts/bump_version.py --audit             # find undeclared version strings
python skills/releasing/scripts/bump_version.py <new-version>       # bump all files declared in .version-bump.json
```

New:
```bash
bundles-forge bump-version --check             # detect version drift across manifests
bundles-forge bump-version --audit             # find undeclared version strings
bundles-forge bump-version <new-version>       # bump all files declared in .version-bump.json
```

- [ ] **Step 3: Update Key Conventions (lines 109-112)**

Line 109 — change:
Old: `**Pre-commit:** run \`python skills/releasing/scripts/bump_version.py --check\` to detect version drift`
New: `**Pre-commit:** run \`bundles-forge bump-version --check\` to detect version drift`

Line 110 — change:
Old: `**Pre-commit:** run \`python skills/auditing/scripts/generate_checklists.py --check\` to detect checklist drift`
New: `**Pre-commit:** run \`bundles-forge checklists --check\` to detect checklist drift`

Line 112 — change:
Old: `**Pre-release:** run \`python skills/auditing/scripts/audit_docs.py\` to verify documentation consistency (9 checks: D1-D9)`
New: `**Pre-release:** run \`bundles-forge audit-docs\` to verify documentation consistency (9 checks: D1-D9)`

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "refactor: update CLAUDE.md commands to use bundles-forge CLI"
```

---

### Task 7: Verify Everything Works

**Files:**
- No new changes

- [ ] **Step 1: Run existing test suite**

Run: `python tests/run_all.py`
Expected: all tests pass (same as before — no tests reference the old paths in executable context).

- [ ] **Step 2: Run the dispatcher against the project itself**

Run: `python bin/bundles-forge audit-skill --json .`
Expected: JSON output with skill quality findings, exit code 0 or 1.

Run: `python bin/bundles-forge bump-version --check`
Expected: version sync check output, exit code 0.

Run: `python bin/bundles-forge audit-docs .`
Expected: documentation consistency check output, exit code 0.

- [ ] **Step 3: Grep for any remaining old-style references**

Run: `grep -rn "python skills/auditing/scripts/" skills/ CLAUDE.md --include="*.md"`
Expected: zero matches (all replaced).

Run: `grep -rn "python skills/releasing/scripts/" skills/ CLAUDE.md --include="*.md"`
Expected: zero matches (all replaced).

- [ ] **Step 4: Commit (if any fixes were needed)**

If grep found stray references, fix them and commit. Otherwise skip this step.

---

## Self-Review

### Spec Coverage

| Spec Requirement | Task |
|---|---|
| Create `bin/bundles-forge` dispatcher | Task 1 |
| Create `bin/bundles-forge.cmd` Windows wrapper | Task 2 |
| Replace `allowed-tools` declarations (5 SKILL.md) | Task 3 |
| Replace body references in SKILL.md files | Task 4 |
| Replace references in reference docs (6 files) | Task 5 |
| Replace references in CLAUDE.md | Task 6 |
| Verification | Task 7 |
| Python-to-Python imports unchanged | Out of scope (correct) |
| `bundles-forge:<skill-name>` invocations unchanged | Out of scope (correct) |

### Placeholder Scan

No TBD, TODO, or vague instructions. All steps contain exact file paths, exact old/new strings, and exact commands.

### Type Consistency

All subcommand names are consistent across Tasks 3-6: `audit-skill`, `audit-security`, `audit-docs`, `audit-plugin`, `audit-workflow`, `checklists`, `bump-version`. The dispatcher's `COMMANDS` table in Task 1 matches the subcommand names used everywhere else.
