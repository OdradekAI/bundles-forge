# Platform Reference

## Supported Platforms

| Platform | Manifest | Discovery |
|----------|----------|-----------|
| Claude Code | `.claude-plugin/plugin.json` | Convention-based |
| Cursor | `.cursor-plugin/plugin.json` | Explicit paths |
| Codex | `.codex/INSTALL.md` | Symlink to `~/.agents/skills/` |
| OpenCode | `.opencode/plugins/<name>.js` | Plugin config |
| Gemini CLI | `gemini-extension.json` | Context file |

## Platform Selection Strategies

When recommending platforms, consider these common strategies:

**Single-platform start** (recommended for most projects):
- Pick the platform the user actually uses daily
- Others can be added later via `bundles-forge:scaffolding`
- Lowest maintenance burden, fastest to ship

**Dual-platform** (when user actively uses two platforms):
- Common pair: Claude Code + Cursor
- Test both adapters before release

**Full coverage** (rare — only when distribution is the primary goal):
- Requires testing on all platforms
- Untested platform adapters create maintenance debt
- Only recommend when the user's stated goal is broad distribution
