---
name: openclaw-bootstrap
description: "Injects bundles-forge skill routing context on session start"
metadata:
  { "openclaw": { "emoji": "🔨", "events": ["command:new", "command:reset"], "requires": { "bins": ["node"] } } }
---

# OpenClaw Bootstrap

Reads `skills/using-bundles-forge/SKILL.md` and pushes the full skill routing
context into the new session so the agent knows which bundles-forge skills are
available and how to invoke them.

Fires on `command:new` and `command:reset` — mirrors the Claude Code
`SessionStart` hook behaviour (startup, clear).
