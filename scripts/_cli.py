"""Shared CLI utilities for bundle-plugin scripts."""

import argparse
import sys
from pathlib import Path


def make_parser(description):
    """Create a standard argparse parser with project-root and --json options."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("project_root", nargs="?", default=".",
                        help="Bundle-plugin root (default: current directory)")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON instead of markdown")
    return parser


def resolve_root(path_str):
    """Resolve project root and verify it contains a skills/ directory."""
    root = Path(path_str).resolve()
    if not (root / "skills").is_dir():
        print(f"error: {root} has no skills/ directory", file=sys.stderr)
        sys.exit(1)
    return root


def exit_by_severity(summary):
    """Exit with code 2 (critical), 1 (warnings), or 0 (clean)."""
    sys.exit(2 if summary.get("critical", 0) else
             1 if summary.get("warning", 0) else 0)
