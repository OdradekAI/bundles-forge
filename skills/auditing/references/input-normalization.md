# Input Normalization

> **Supplementary reference** for edge-case input types, `repos/` naming conventions, and security rules. The core normalization flow (workspace resolution, common input types, failure handling) and the output directory structure are defined in each skill's Input Normalization step and `CLAUDE.md` respectively.

## Edge-Case Input Types

These input types require extra handling beyond the core flow defined inline in each skill's Input Normalization step.

| Input | Action | Read from | Reports written to |
|-------|--------|-----------|-------------------|
| GitHub subdirectory URL (`…/tree/main/skills/xxx`) | Clone repo (shallow) to `repos/`, extract the subdirectory path | Subdirectory within clone | `<workspace>/.bundles-forge/audits/` |
| GitHub release/archive URL (`.zip`/`.tar.gz`) | Download and extract to `<workspace>/.bundles-forge/repos/<owner>__<repo>/` | Extracted directory | `<workspace>/.bundles-forge/audits/` |

### repos/ Naming Convention

Directories under `.bundles-forge/repos/` follow this naming scheme:

| Source | Directory name | Example |
|--------|---------------|---------|
| GitHub URL | `<owner>__<repo>[__<version>][__<timestamp>]` | `alice__cool-plugin__v1.2.0__20260419` |
| Zip/tar.gz file | `<archive-name>[__<timestamp>]` | `cool-plugin__20260419` |

- Use double underscores (`__`) as separators
- `<version>` comes from the GitHub tag/branch if identifiable, otherwise omit
- `<timestamp>` (YYYYMMDD format) is appended when the directory already exists to avoid collisions
- No automatic cleanup — users manage `repos/` contents manually

## Security Rules

**Remote sources:** Always clone/download without executing hooks or scripts. Use `--no-checkout` + selective `git checkout`, or extract archives without running post-install scripts. The audit itself will scan for risks — don't trigger them before scanning.
