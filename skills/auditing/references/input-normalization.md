# Input Normalization

> **Canonical source** for input normalization across all skills that accept external targets.

The target can be a local path, a GitHub URL, or a zip file. Normalize to a local directory before proceeding.

| Input | Action |
|-------|--------|
| Local directory path | Use directly |
| Local SKILL.md file path | Use its parent directory |
| GitHub repo URL (`https://github.com/user/repo`) | `git clone --depth 1 --no-checkout` to temp dir, then `git checkout` (avoids running hooks) |
| GitHub subdirectory URL (`…/tree/main/skills/xxx`) | Clone repo (shallow), extract the subdirectory path |
| Zip/tar.gz file path | Extract to temp directory |
| GitHub release/archive URL (`.zip`/`.tar.gz`) | Download, then extract to temp directory |

**Security rule for remote sources:** Always clone/download without executing hooks or scripts. Use `--no-checkout` + selective `git checkout`, or extract archives without running post-install scripts. The audit itself will scan for risks — don't trigger them before scanning.

**If clone/download fails:** Tell the user what failed (network error, 404, auth required, rate limit) and suggest alternatives — provide the repo as a local path or zip file. Do not silently skip the audit or proceed with partial data.
