# Optimization Decision Trees

Reference tables for routing audit findings to optimization targets, classifying actions, diagnosing skill health, and identifying component needs.

## Target Routing

Select targets based on audit findings or user request — don't run all 6 sequentially:

| Finding / Signal | Target |
|------------------|--------|
| Q-findings (description anti-patterns, frontmatter issues) | Target 1, 2 |
| W-findings (workflow integrity issues) | Target 3 |
| Platform gaps identified | Invoke `bundles-forge:scaffolding` directly |
| Security findings (SC/AG checks) | Target 4 |
| User requests adding/replacing/reorganizing skills | Target 5 |
| Component signals (userConfig, MCP, LSP needs) | Target 6 |
| User behavioral feedback about skill quality | Feedback Iteration |

## Optimization Action Classification

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

## Skill Health Assessment

Beyond automated linter checks, assess each skill's health across four dimensions. These are qualitative judgments, not runtime metrics — form them from audit findings, user feedback, and manual review:

| Dimension | Question to Answer | Signals |
|-----------|--------------------|---------|
| **Trigger confidence** | Can this skill be correctly triggered from realistic user prompts? | Create 3-5 test prompts and mentally simulate whether the description would match. Low confidence → Target 1 |
| **Execution clarity** | Once triggered, can an agent follow the steps without ambiguity? | Look for vague instructions, missing preconditions, implicit assumptions. Low clarity → FIX action |
| **End-to-end completeness** | Does the full flow from trigger to output have gaps? | Check for missing handoffs, undefined artifacts, steps that assume context not provided by upstream. Gaps → Target 3 or CAPTURED action |
| **Degradation signals** | Has this skill stopped working in practice? | User reports of wrong output, audit findings that recur after previous fixes, broken references to changed APIs or tools. Present → urgent FIX action |

## Workflow Gap Detection

When audit findings or health assessment reveal structural gaps — not just broken connections but missing capabilities:

| Signal | Consider CAPTURED |
|--------|-------------------|
| W2 (unreachable skill) where the skill serves a real need but has no entry point | Create a new routing or orchestration skill |
| Workflow graph has a "dead zone" between two skills with no handoff path | Create a bridging skill to connect them |
| Users repeatedly perform multi-step manual work that no existing skill covers | Capture the pattern as a new skill |
| A skill's `## Outputs` lists artifacts that no downstream skill consumes | Either remove the dead output or create a consumer skill |

## W-Check Fix Priority

| Finding | How to Fix |
|---------|-----------|
| W1 (undeclared cycle) | Add `<!-- cycle:a,b -->` in `## Integration` if the loop is intentional, or restructure the chain |
| W2 (unreachable skill) | Add the skill to bootstrap routing, or declare `Called by: user directly` in `## Integration` |
| W3/W4 (missing Inputs/Outputs) | Add `## Outputs` to terminal skills, `## Inputs` to referenced skills, with artifact IDs |
| W5 (artifact ID mismatch) | Align backtick artifact IDs between upstream `## Outputs` and downstream `## Inputs` |
| W9 (empty/placeholder sections) | Write meaningful semantic descriptions for each artifact in Inputs/Outputs |
| W10 (asymmetric integration) | Ensure `**Calls:**` and `**Called by:**` declarations are symmetric across connected skills |

## Optional Component Signals

| Signal | Component | Action |
|--------|-----------|--------|
| Skills hardcode API keys/endpoints as `${VAR}` env vars | `userConfig` | Migrate to `userConfig` for automatic user prompting |
| Audit finds MCP servers without `userConfig`-backed auth | `userConfig` | Add `userConfig` fields with `sensitive: true` |
| Skills reference external SaaS APIs with no integration | `.mcp.json` or `bin/` | Add MCP server or CLI — consult decision tree |
| Skills involve language-specific code intelligence | `.lsp.json` | Add LSP server config |
| Users request custom output formats | `output-styles/` | Add output style definitions |
| Plugin MCP server has npm dependencies | `${CLAUDE_PLUGIN_DATA}` | Add SessionStart dependency install hook |
| Plugin uses `../` paths or writes to `${CLAUDE_PLUGIN_ROOT}` | Path migration | Fix to use relative `./` paths and `${CLAUDE_PLUGIN_DATA}` |
