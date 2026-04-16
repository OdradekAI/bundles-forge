# OpenClaw Tool Mapping

When bundles-forge skills reference Claude Code tools, substitute these OpenClaw equivalents:

| Claude Code Tool | OpenClaw Equivalent |
|-----------------|---------------------|
| `Skill` | Native skill discovery (auto-loaded from `skills/`) |
| `TodoWrite` | `todowrite` |
| `Task` (subagents) | `sessions_spawn` / `sessions_send` |
| `Read` | `read` |
| `Write` | `write` |
| `Edit` | `edit` |
| `Bash` | `exec` (alias: `bash`) |
| `WebSearch` | `web_search` |
| `WebFetch` | `web_fetch` |

Skills from the bundle's `skills/` directory are loaded automatically when the
bundle is installed via `openclaw bundles install`.
