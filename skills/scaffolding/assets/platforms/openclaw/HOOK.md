---
name: <project-name>-bootstrap
description: "Injects <project-name> skill routing context on session start"
metadata:
  { "openclaw": { "emoji": "🔨", "events": ["command:new", "command:reset"], "requires": { "bins": ["node"] } } }
---

# Bootstrap

Reads `skills/using-<project-name>/SKILL.md` and pushes the full skill routing
context into the new session.
