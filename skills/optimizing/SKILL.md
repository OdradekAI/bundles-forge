---
name: optimizing
description: "Use when optimizing a bundle-plugin or single skill — improving descriptions, reducing tokens, fixing audit findings, restructuring workflows, adding skills to fill gaps, or iterating on user feedback"
allowed-tools: Bash(bundles-forge audit-skill *) Bash(bundles-forge audit-security *) Bash(bundles-forge audit-docs *) Bash(bundles-forge audit-plugin *) Bash(bundles-forge audit-workflow *) Bash(bundles-forge checklists *) Bash(bundles-forge bump-version *)
---

# Optimizing Bundle-Plugins

## Overview

Orchestrate targeted improvement of a bundle-plugin project or a single skill. Unlike a full audit, optimization focuses on goals: better triggering, lower token cost, tighter workflow chains, and feedback-driven skill refinement. This skill diagnoses issues, decides on improvements, and delegates content changes to `bundles-forge:authoring`.

**Core principle:** Optimize for the agent's experience. Diagnose → decide → delegate → verify.

**Skill type:** Hybrid — follow the execution flow rigidly (diagnose → decide → delegate → verify), but select targets and adapt execution strategies flexibly based on audit findings and user goals.

**Announce at start:** "I'm using the optimizing skill to improve [this project / this skill]."

## Step 1: Resolve Input & Detect Scope

The target can be a local path, a GitHub URL, or a zip file. Normalize the input to a local directory before scope detection.

### Input Normalization

| Input | Action |
|-------|--------|
| Local directory path | Use directly |
| Local SKILL.md file path | Use its parent directory |
| GitHub repo URL (`https://github.com/user/repo`) | `git clone --depth 1 --no-checkout` to temp dir, then `git checkout` |
| GitHub subdirectory URL (`…/tree/main/skills/xxx`) | Clone repo (shallow), extract the subdirectory path |
| Zip/tar.gz file path | Extract to temp directory |
| GitHub release/archive URL (`.zip`/`.tar.gz`) | Download, then extract to temp directory |

**Security rule for remote sources:** Always clone/download without executing hooks or scripts. Use `--no-checkout` + selective `git checkout`, or extract archives without running post-install scripts.

**If clone/download fails:** Tell the user what failed (network error, 404, auth required, rate limit) and suggest alternatives — provide the repo as a local path or zip file. Do not silently skip or proceed with partial data.

### Scope Detection

After normalization, determine the scope from the resolved local path:

| Target | How to Detect | Mode |
|--------|--------------|------|
| Project root | Has `skills/` directory and `package.json` | **Project optimization** — all 8 targets |
| Single skill directory | Contains `SKILL.md` but no `skills/` subdirectory | **Skill optimization** — 4 targets + feedback iteration |
| Single SKILL.md file | Path ends in `SKILL.md` | **Skill optimization** — 4 targets + feedback iteration |

**If the target is a single skill, skip to the Skill Optimization section below.**

---

## Project Optimization

### Process

1. **Identify target** — what specifically needs improvement?
2. **Measure current state** — run Script-Assisted Checks, consume audit findings
3. **Apply improvement** — delegate changes to the appropriate target below
4. **Verify** — did it actually improve? For descriptions: create test prompts, verify triggering before and after

### Target Routing

Select targets based on audit findings or user request — don't run all 8 sequentially:

| Finding / Signal | Target |
|------------------|--------|
| Q-findings (description anti-patterns, frontmatter issues) | Target 1, 2, 3 |
| W-findings (workflow integrity issues) | Target 4 |
| Platform gaps identified | Target 5 |
| Security findings (SC/AG checks) | Target 6 |
| User requests adding/replacing/reorganizing skills | Target 7 |
| Component signals (userConfig, MCP, LSP needs) | Target 8 |
| User behavioral feedback about skill quality | Feedback Iteration |

### Optimization Action Classification

After selecting a target, classify the optimization action before delegating. This determines the delegation strategy and guards against scope drift.

**Action types:**

| Type | When | Delegation strategy |
|------|------|---------------------|
| **FIX** | Skill has a defect — outdated instructions, broken references, ineffective steps | Repair in place. Provide the specific defect and the corrected content. The skill's core goal and scope must not change |
| **DERIVED** | Skill works but needs enhancement or specialization for a new context | Create a variant or improved version. The original remains available. Clearly state what's being enhanced and why |
| **CAPTURED** | A workflow gap exists — no skill covers a needed capability | Create a new skill from scratch. Define its responsibility boundary, triggering conditions, and workflow connections |

**Before delegating, explicitly state:**

1. **Classification with rationale:** "This is a FIX because the description anti-pattern causes false triggers" — not just "I'll fix the description"
2. **Impact analysis:** When the change touches `## Outputs`, `## Integration`, or cross-references, map all downstream skills that consume those artifacts. Include downstream updates in the same delegation scope rather than discovering breakage in the verify step
3. **Scope preservation check:** After drafting the change, verify: does the optimized skill still serve the same core goal? If the change shifts what the skill *is* (not just how well it does it), stop and reassess

### Script-Assisted Checks

Run the quality linter to identify frontmatter issues, description anti-patterns, and broken references before manual optimization:

```bash
bundles-forge audit-skill <project-root>        # markdown report
bundles-forge audit-skill --json <project-root>  # machine-readable
```

The linter automates checks Q1-Q12 and X1-X2 from the skill quality ruleset. Focus manual effort on the subjective targets below.

### Skill Health Assessment

Beyond automated linter checks, assess each skill's health across four dimensions. These are qualitative judgments, not runtime metrics — form them from audit findings, user feedback, and manual review:

| Dimension | Question to Answer | Signals |
|-----------|--------------------|---------|
| **Trigger confidence** | Can this skill be correctly triggered from realistic user prompts? | Create 3-5 test prompts and mentally simulate whether the description would match. Low confidence → Target 1 |
| **Execution clarity** | Once triggered, can an agent follow the steps without ambiguity? | Look for vague instructions, missing preconditions, implicit assumptions. Low clarity → FIX action |
| **End-to-end completeness** | Does the full flow from trigger to output have gaps? | Check for missing handoffs, undefined artifacts, steps that assume context not provided by upstream. Gaps → Target 4 or CAPTURED action |
| **Degradation signals** | Has this skill stopped working in practice? | User reports of wrong output, audit findings that recur after previous fixes, broken references to changed APIs or tools. Present → urgent FIX action |

### Workflow Gap Detection

When audit findings or health assessment reveal structural gaps — not just broken connections but missing capabilities — consider whether a new skill should be created rather than patching existing ones:

| Signal | Consider CAPTURED |
|--------|-------------------|
| W2 (unreachable skill) where the skill serves a real need but has no entry point | Create a new routing or orchestration skill |
| Workflow graph has a "dead zone" between two skills with no handoff path | Create a bridging skill to connect them |
| Users repeatedly perform multi-step manual work that no existing skill covers | Capture the pattern as a new skill |
| A skill's `## Outputs` lists artifacts that no downstream skill consumes | Either remove the dead output or create a consumer skill |

### Target 1: Skill Description Triggering

The highest-impact optimization. Descriptions are the primary mechanism for skill discovery.

**Diagnosis** — identify descriptions that summarize workflow, exceed 250 characters, are too narrow/broad, or fail to start with "Use when...".

**Decision** — draft the improved description and rationale. Use A/B eval (see below) to compare triggering accuracy before and after.

**Delegation** — invoke `bundles-forge:authoring` with a precise change spec: the old description verbatim, the new description, the rationale tied to a specific diagnosis (audit finding, health assessment dimension, or user feedback), and the action classification (FIX/DERIVED). Do not ask authoring to "improve the description" — specify the exact change.

**Guiding principle:** Use A/B eval when a change could produce regression effects — when improving one dimension might degrade another. Each eval scenario below defines its own skip conditions based on what kind of regression is possible.

### A/B Eval for Description Changes

When optimizing a description, never overwrite the original blindly. Use a copy-and-compare approach:

```
1. Copy the skill to a working version (e.g. `<skill-name>-optimized/`)
2. Apply the description change to the copy only
3. Create 5+ realistic test prompts that should trigger this skill
4. Dispatch two `evaluator` agents (`agents/evaluator.md`) in parallel:
   - Evaluator A: label "original", loaded with the ORIGINAL skill → run all test prompts
   - Evaluator B: label "optimized", loaded with the OPTIMIZED skill → run all test prompts
5. Compare: which version triggered correctly on more prompts?
6. Present results to user with side-by-side comparison
7. User decides → adopt optimized version (replace original) or discard
```

**If subagent dispatch is unavailable:** Ask the user which fallback to use:
- **Sequential inline:** Read `agents/evaluator.md` and follow its execution protocol inline. Run both evaluations in sequence within this conversation. Randomize which version runs first (flip a coin) to reduce ordering bias — note the execution order in results so the user can judge accordingly
- **Skip A/B:** Apply the change directly with a simple verification pass instead of comparative evaluation

**What to compare:**
- Trigger rate: how many of the test prompts correctly activated the skill?
- False negatives: did the optimized description miss cases the original caught?
- False positives: did either version trigger on prompts meant for other skills?

**When to skip A/B eval:** If the change is purely additive (adding triggering conditions that were previously missing) and doesn't modify existing trigger phrases, a simple verification pass is sufficient.

### Target 2: Token Efficiency

> **Canonical source:** Token budgets are defined in `bundles-forge:authoring` (Token Efficiency section).

**Diagnosis** — identify skills exceeding token budgets (SKILL.md body > 500 lines, bootstrap > 200 lines), duplicated content, sections that should be in `references/`.

**Decision** — determine what to extract, merge, or cut. Map specific sections to their target location.

**Delegation** — invoke `bundles-forge:authoring` with a section-level restructuring spec: which sections to extract (source heading → target file in references/), which content to cut (quote the specific lines), and which cross-references to add. Authoring should modify only the named sections, not rewrite the entire SKILL.md.

### Target 3: Progressive Disclosure

**Diagnosis** — verify the three-level loading structure (metadata / SKILL.md body / references) is properly layered. Identify skills where the body contains content that belongs at a different level.

**Decision** — determine which sections to promote (to metadata) or demote (to references/).

**Delegation** — invoke `bundles-forge:authoring` with per-section move instructions: for each section being promoted or demoted, specify the source location, the target level, and the reason (e.g. "move lines 45-80 to references/platform-details.md because this content is only needed during platform adaptation, not on every skill load").

### Target 4: Workflow Chain Integrity

Consume the `workflow-report` from `bundles-forge:auditing` (Workflow mode) to identify and fix workflow issues. If no workflow report is available, run the workflow audit first:

```bash
bundles-forge audit-workflow <project-root>                          # full workflow audit
bundles-forge audit-workflow --focus-skills skill-a,skill-b <root>   # focused on specific skills
```

**Fix by W-check priority:**

| Finding | How to Fix |
|---------|-----------|
| W1 (undeclared cycle) | Add `<!-- cycle:a,b -->` in `## Integration` if the loop is intentional, or restructure the chain |
| W2 (unreachable skill) | Add the skill to bootstrap routing, or declare `Called by: user directly` in `## Integration` |
| W3/W4 (missing Inputs/Outputs) | Add `## Outputs` to terminal skills, `## Inputs` to referenced skills, with artifact IDs |
| W5 (artifact ID mismatch) | Align backtick artifact IDs between upstream `## Outputs` and downstream `## Inputs` |
| W9 (empty/placeholder sections) | Write meaningful semantic descriptions for each artifact in Inputs/Outputs |
| W10 (asymmetric integration) | Ensure `**Calls:**` and `**Called by:**` declarations are symmetric across connected skills |

**After fixes — Chain A/B Eval:**

Use chain evaluation to verify end-to-end handoff quality after workflow changes. Follow the same dispatch and fallback pattern as Description A/B Eval, with these differences:

1. Define a realistic end-to-end scenario (e.g. "design and scaffold a new bundle-plugin")
2. Dispatch `evaluator` with label "chain" and the ordered skill list
3. Review transition quality ratings — focus on "broken" handoffs
4. Address broken handoffs by improving `## Inputs` / `## Outputs` declarations

**When to use:** After modifying Inputs/Outputs sections, adding new skills to a workflow chain, or when audit findings indicate workflow integrity issues (G1-G4). Chain eval is sequential by nature (traces a pipeline), so ordering bias is not a concern.

### Target 5: Platform Coverage (project only)

Identify platforms the project doesn't yet support. For adding new platforms, invoke `bundles-forge:scaffolding`.

### Target 6: Security Remediation (project only)

Fix security findings from `bundles-forge:auditing` Category 10.

**Targets:**
- Remove unnecessary system access from hook scripts (least privilege)
- Scope OpenCode plugin capabilities to declared needs only
- Remove or justify any network calls in hooks/plugins
- Ensure agent prompts include scope constraints
- Strip encoding tricks or obfuscated content from SKILL.md files

**Process:** Run security scan first, then address findings by priority — critical before warnings, warnings before info:

```bash
bundles-forge audit-security <project-root>
```

Alternatively, invoke `bundles-forge:auditing` for a full audit that includes security (Category 10).

### Target 7: Skill & Workflow Restructuring (project only)

Structural changes to achieve user goals: adding skills, replacing skills, reorganizing workflow chains, or converting skills to subagents.

#### 7a. Adding Skills

When the project has a workflow gap or the user needs new capability:

1. **Read existing project** — list all skills, map the workflow graph (`## Integration` sections), identify the bootstrap skill's routing table
2. **Inventory new skills** — for each skill being added, record source, structure, frontmatter quality
3. **Compatibility analysis** — check naming conflicts, description style, overlapping responsibilities, cross-reference conventions against the existing project
4. **For third-party skills** — follow `references/third-party-integration.md` (inventory checklist, compatibility checks, integration intent, security audit)
5. **Design insertion** — identify where new skills connect to the existing workflow graph, map new `**Calls:**` / `**Called by:**` declarations, update bootstrap routing if needed
6. **Apply** — copy skills into `skills/`, adapt per integration intent, update existing skills' `## Integration` sections
7. **Verify** — run `bundles-forge:auditing` in Workflow mode with `--focus-skills <new-skills>` to verify workflow integrity

For Intent B (integrate into workflow) third-party skills, invoke `bundles-forge:authoring` after adaptation for content quality validation.

#### 7b. Replacing Skills

When a better alternative exists for an existing skill:

1. Analyze the replacement skill's compatibility (same checks as 7a)
2. Map all references to the old skill across the project (cross-references, Integration sections, routing table)
3. Replace and update all references
4. Verify with workflow audit

#### 7c. Reorganizing Workflows

When the execution chain needs restructuring:

1. Map the current workflow graph
2. Identify inefficiencies: unnecessary handoffs, missing shortcuts, bottleneck skills
3. Propose new chain — present to user for approval
4. Update `## Integration` sections across affected skills
5. Update bootstrap routing table
6. Verify with Chain A/B Eval (Target 4)

#### 7d. Skill-to-Agent Conversion

When a skill would work better as a read-only subagent:

Candidates for conversion:
- Execution produces verbose temporary context (search results, file contents, logs) that subsequent steps don't need
- Skills that only inspect/validate without modifying files
- Skills that produce structured reports (self-contained output)
- Skills that could run in parallel with other work (optional bonus)

Conversion steps:
1. Extract the skill's execution protocol into `agents/<role>.md`
2. Update the dispatching skill to use subagent dispatch instead of skill invocation
3. Add fallback logic (read agent file inline when subagents unavailable)
4. Remove the original skill directory if fully replaced

Post-conversion verification:
1. Dispatch `evaluator` (label "original") with test prompts to confirm the new agent correctly executes the former skill's responsibilities
2. Run `bundles-forge:auditing` to verify dispatch/fallback logic in the orchestrating skill

### Target 8: Optional Component Management (project only)

Add, adjust, or migrate optional plugin components based on evolving project needs. This target handles the gap between initial scaffolding and the components a project needs as it matures.

**Diagnosis** — identify signals that a component is needed:

| Signal | Component | Action |
|--------|-----------|--------|
| Skills hardcode API keys/endpoints as `${VAR}` env vars | `userConfig` | Migrate to `userConfig` for automatic user prompting |
| Audit finds MCP servers without `userConfig`-backed auth | `userConfig` | Add `userConfig` fields with `sensitive: true` |
| Skills reference external SaaS APIs with no integration | `.mcp.json` or `bin/` | Add MCP server or CLI — consult decision tree |
| Skills involve language-specific code intelligence | `.lsp.json` | Add LSP server config |
| Users request custom output formats | `output-styles/` | Add output style definitions |
| Plugin MCP server has npm dependencies | `${CLAUDE_PLUGIN_DATA}` | Add SessionStart dependency install hook |
| Plugin uses `../` paths or writes to `${CLAUDE_PLUGIN_ROOT}` | Path migration | Fix to use relative `./` paths and `${CLAUDE_PLUGIN_DATA}` |

**Decision** — read `skills/scaffolding/references/external-integration.md` for the full decision tree (CLI vs MCP, userConfig schema, PLUGIN_DATA patterns, LSP fields, output-styles format, settings.json scope).

**Execution** — invoke `bundles-forge:scaffolding` using its "Adding Optional Components" flow. Scaffolding handles file generation, manifest updates, and inspector validation.

**Verification** — after scaffolding completes, run `bundles-forge:auditing` to confirm structural integrity and security compliance (especially for new MCP servers and userConfig sensitive values).

---

## Skill Optimization (Lightweight Mode)

When the target is a single skill, run only the targets that apply at skill scope. This is auto-detected — no special flags needed.

### Applicable Targets

| Target | Applicable | What to Do |
|--------|-----------|------------|
| 1. Description Triggering | **Full** | Evaluate and improve the description's triggering accuracy |
| 2. Token Efficiency | **Full** | Check SKILL.md line count, references extraction |
| 3. Progressive Disclosure | **Full** | Verify the 3-level loading structure |
| 4. Workflow Chain Integrity | **Partial** | Fix this skill's W9/W10 findings (Inputs/Outputs clarity, integration symmetry) |
| 5. Platform Coverage | **Skip** | Project-level concern |
| 6. Security Remediation | **Partial** | Fix security issues within this skill's content |
| 7. Skill & Workflow Restructuring | **Skip** | Project-level concern |
| 8. Optional Component Management | **Skip** | Project-level concern |
| Feedback Iteration | **Full** | Process user feedback with 3-question validation |

### Skill Process

1. **Read target skill** — consume `skill-report` if available (or extract per-skill findings from `audit-report`)
2. **Determine goal** — engineering optimization or feedback iteration?
3. **Engineering path:** diagnose applicable targets (1-4, partial 6)
4. **Feedback path:** run the Feedback Iteration process (below)
5. **Delegate** content changes to `bundles-forge:authoring`
6. **Verify** — run `bundles-forge:auditing` (skill mode) for post-change verification

### Script Shortcuts

```bash
bundles-forge audit-skill <skill-directory>     # quality checks on single skill
```

---

## Feedback Iteration

Process user feedback about a specific skill's behavior or output quality. This is a cross-cutting concern — available in both project and skill optimization modes. Use this when a user reports that a skill triggered but produced wrong results, skipped steps, or needs better wording.

### Classify the Feedback

| Signal | Action |
|--------|--------|
| "This skill triggered but produced wrong results" | Feedback iteration (below) |
| "The steps in this skill are in the wrong order" | Feedback iteration (below) |
| "Description format doesn't follow conventions" | Use optimization targets 1-3 |
| "Token budget exceeded across the project" | Use optimization targets 2-3 (project mode) |

### The Feedback Process

```
Receive feedback
  → Identify target skill
  → If external skill: fork with `forked-` prefix before modifying
  → Read skill, understand core goal
  → Validate each feedback item (goal alignment, necessity, side effects)
  → Present improvement plan to user
  → USER CONFIRMS ← gate
  → Copy skill to working version (<skill-name>-optimized/)
  → Delegate changes to bundles-forge:authoring on the copy
  → A/B eval: subagent A (original) vs subagent B (optimized) with same input
  → Present comparison to user
  → User adopts → replace original; User rejects → discard copy
  → Run bundles-forge:auditing for post-change verification
```

**Validation framework** — for each feedback item, ask three questions:
1. **Goal alignment:** Does this serve the skill's core goal, or push it toward a different purpose?
2. **Necessity:** Without this change, does the skill have an actual defect (vs. a style preference)?
3. **Side effects:** Could this introduce complexity creep, scope expansion, or regression?

### A/B Eval for Feedback Changes

Follow the same dispatch and fallback pattern as Description A/B Eval (Target 1), with these differences:

- **Test scenario:** Use the specific scenario from the user's feedback (the input that produced wrong results), not synthetic test prompts
- **What to compare:** Output quality and behavioral correctness, not triggering accuracy
- **When to skip:** If the feedback is about structural issues (missing section, wrong heading level, broken reference) rather than behavioral differences, a simple verification pass is sufficient

**Rules:**
- Never apply feedback without user confirmation of the improvement plan
- For external skills, always fork first (prefix with `forked-`, add provenance header)
- After all changes, invoke `bundles-forge:auditing` for post-change verification — one audit pass only (auditing reports; optimizing decides)

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Optimizing everything at once | Pick one target, measure, improve, verify |
| Adding MUST/ALWAYS/NEVER instead of explaining why | Explain the reasoning — agents respond to understanding |
| Splitting skills too aggressively | Only split when there's a genuine responsibility boundary |
| Ignoring token budget for bootstrap | Bootstrap loads every session — every word counts |
| Applying feedback without validation | Every item goes through the 3-question framework |
| Expanding skill scope during any optimization | Optimization should improve how well a skill fulfills its goal, not shift what the goal is. Verify after every change: does this skill still do the same thing? |
| Running all 8 targets on a single skill | Let scope auto-detection handle it — targets 5-8 don't fully apply |
| Rewriting entire SKILL.md instead of surgical edits | Specify section-level changes in delegation. A FIX to one heading should not trigger a full rewrite — minimize diff surface to reduce regression risk |
| Adding third-party skills without security audit | Always run `bundles-forge:auditing` — see `references/third-party-integration.md` |
| Adding skills without updating Integration sections | Every new connection needs symmetric `Calls` / `Called by` declarations |

## Inputs

- `audit-report` (optional) — findings from `bundles-forge:auditing` (full project mode). Contains per-skill breakdowns — when optimizing a single skill from a full audit, extract the relevant skill's findings from the Per-Skill Breakdown section
- `skill-report` (optional) — findings from `bundles-forge:auditing` (skill mode). More precise input for Skill Optimization — 4-category scored report targeting a single skill
- `workflow-report` (optional) — workflow-specific findings (W1-W11) from `bundles-forge:auditing` (workflow mode), consumed by Target 4
- `user-feedback` (optional) — behavioral feedback about skill quality, triggering issues, or wrong output

## Outputs

- `optimized-skill` — improved SKILL.md content with better descriptions, reduced tokens, or fixed workflow references
- `eval-report` (optional) — optimization record written to `.bundles-forge/`, structured as:
  - **Action type:** FIX, DERIVED, or CAPTURED
  - **Change summary:** one sentence describing what changed and why
  - **Diagnosis basis:** which health dimension, audit finding, or user feedback triggered this optimization
  - **Before/after comparison:** A/B eval results, or verification pass outcome if A/B was skipped

## Integration

**Called by:**
- **bundles-forge:releasing** — fix quality findings during release pipeline
- User directly — standalone optimization of any project or skill

**Calls:**
- **bundles-forge:authoring** — all content changes (descriptions, token optimization, restructuring, third-party adaptation)
  - Artifact: `optimized-skill` → `optimization-spec` (indirect — optimizing formulates the spec, authoring receives it as targeted change instructions)
- **bundles-forge:scaffolding** — Target 5 (platform coverage) for adding new platforms; Target 8 (optional components) for adding MCP/LSP/userConfig/output-styles
  - Artifact: `optimized-skill` → `project-directory` (indirect — scaffolding operates on the project directory, not the optimization output)
- **bundles-forge:auditing** — post-change verification (one pass, no loops)
  - Artifact: `optimized-skill` → `project-directory` (indirect — auditing targets the project containing the optimized skill)

**Pairs with:**
- **bundles-forge:releasing** — after optimization, versions may need sync
