#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON="${PYTHON:-$(command -v python3 2>/dev/null || command -v python 2>/dev/null)}"
exec "$PYTHON" "$SCRIPT_DIR/skills/releasing/scripts/bump_version.py" "$@"
