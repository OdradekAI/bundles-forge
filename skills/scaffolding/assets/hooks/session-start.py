#!/usr/bin/env python3
"""SessionStart hook for <project-name> plugin.

Emits a lightweight one-line prompt informing the agent that skills are
available. The full routing context (using-<project-name>/SKILL.md) is
loaded on demand via the platform's Skill tool when any command is first
invoked.

Platform detection:
  CURSOR_PLUGIN_ROOT  → Cursor format (additional_context)
  CLAUDE_PLUGIN_ROOT  → Claude Code format (hookSpecificOutput)
  neither             → plain text fallback
"""

import json
import os
import sys
from pathlib import Path


def discover_skills(plugin_root):
    """List skill directory names under skills/."""
    skills_dir = plugin_root / "skills"
    if not skills_dir.is_dir():
        return []
    return sorted(
        d.name for d in skills_dir.iterdir()
        if d.is_dir() and (d / "SKILL.md").is_file()
    )


def main():
    script_dir = Path(__file__).resolve().parent
    plugin_root = script_dir.parent
    project_name = "<project-name>"

    skills = discover_skills(plugin_root)
    skill_list = ", ".join(skills) if skills else "(no skills found)"

    prompt = (
        f"{project_name} loaded. "
        f"Available skills: {skill_list}. "
        f"Use {project_name}:<skill-name> to invoke."
    )

    if os.environ.get("CURSOR_PLUGIN_ROOT"):
        output = json.dumps({"additional_context": prompt})
    elif os.environ.get("CLAUDE_PLUGIN_ROOT"):
        output = json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": prompt,
            }
        })
    else:
        output = prompt

    print(output)
    sys.exit(0)


if __name__ == "__main__":
    main()
