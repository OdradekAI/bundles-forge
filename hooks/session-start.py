#!/usr/bin/env python3
"""SessionStart hook for bundles-forge plugin.

Emits a lightweight one-line prompt informing the agent that bundles-forge
skills are available. The full routing context (using-bundles-forge/SKILL.md)
is loaded on demand via the platform's Skill tool when any bundles-forge
command is first invoked.

Platform detection:
  CURSOR_PLUGIN_ROOT   → Cursor format (additional_context)
  CLAUDE_PLUGIN_ROOT   → Claude Code format (hookSpecificOutput)
  neither              → plain text fallback
"""

import json
import os
import sys


PROMPT = (
    "bundles-forge loaded. "
    "Available skills: blueprinting, scaffolding, authoring, auditing, "
    "optimizing, releasing, testing. "
    "Use bundles-forge:<skill-name> to invoke."
)


def main():
    if os.environ.get("CURSOR_PLUGIN_ROOT"):
        output = json.dumps({"additional_context": PROMPT})
    elif os.environ.get("CLAUDE_PLUGIN_ROOT"):
        output = json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": PROMPT,
            }
        })
    else:
        output = PROMPT

    print(output)
    sys.exit(0)


if __name__ == "__main__":
    main()
