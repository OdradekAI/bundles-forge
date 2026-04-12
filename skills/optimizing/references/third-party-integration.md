# Third-Party Skill Integration

Shared reference for handling third-party skills across the bundle-plugin lifecycle. Referenced by `bundles-forge:blueprinting` (Scenario C) and `bundles-forge:optimizing` (Target 7).

## Inventory Checklist

For each third-party skill, record:

| Field | What to Capture |
|-------|----------------|
| Source | Git repo URL, marketplace listing, or another bundle-plugin project |
| Structure | Standalone SKILL.md, has `references/`, has `scripts/` |
| License | MIT, Apache-2.0, proprietary, unknown |
| Version | Semver tag or commit hash at time of evaluation |
| Maintenance | Actively maintained, archived, unknown |
| Original namespace | Project name and skill cross-reference prefix |

## Compatibility Checks

| Check | What to Look For |
|-------|-----------------|
| License compatibility | Can this license coexist with the project's license? |
| Security posture | Does the skill invoke external tools, network calls, or `eval()`? |
| Staleness risk | Is the skill actively maintained? Will you need to own updates? |
| Naming conflicts | Skill name clashes with existing skills in the target project |
| Overlapping responsibilities | Duplicates or conflicts with existing skills |

Classify each skill as:
- **Ready** — can be included as-is
- **Needs adaptation** — rename, rewrite description, adjust references
- **Needs merge** — overlaps with another skill, combine into one
- **Needs import** — third-party skill requiring copy + source attribution

## Integration Intent

For each skill classified as **Needs import**, determine which intent applies:

### Intent A: Repackage as-is

Bundle the third-party skill without modification.

- Copy the SKILL.md and any `references/` or `scripts/` into the project's `skills/` directory
- Add a source attribution block at the top of the copied SKILL.md:
  ```
  <!-- Source: <original-repo-or-marketplace> | Version: <version> | License: <license> -->
  ```
- Preserve the original description and instructions unchanged
- Use case: packaging scattered third-party skills for distribution

### Intent B: Integrate into workflow

Copy and adapt the skill to fit the project's workflow.

- Copy the skill, then modify:
  - Rewrite description to reflect triggering conditions within the new project context
  - Rewrite cross-reference prefixes (`old-project:skill-name` → `new-project:skill-name`)
  - Add workflow connections: declare upstream/downstream skill dependencies in the `## Integration` section
  - Trim standalone-only instructions that don't apply in the orchestrated context
  - Add handoff guidance to/from adjacent skills in the chain
  - Classify as entry-point or internal skill
- After adaptation, invoke `bundles-forge:authoring` for quality validation
- Use case: building orchestrated workflows on top of third-party foundations

## Security Audit (Mandatory)

Regardless of integration intent, run `bundles-forge:auditing` on all copied third-party content before proceeding. Flag:

- Hook scripts that execute arbitrary commands
- `eval()` calls or dynamic code execution
- Network requests (`curl`, `wget`, `fetch`)
- File system access outside the project directory
- Encoding tricks or obfuscated content in SKILL.md files

For Intent B skills that modify hook scripts or plugin code, re-run auditing after adaptation.
