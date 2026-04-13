#!/usr/bin/env python3
"""
Cross-platform tests for the Python scripts in skills/auditing/scripts/
and skills/releasing/scripts/.

Run: python tests/test_scripts.py
Or:  python -m pytest tests/test_scripts.py -v
"""

import json
import os
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AUDITING_SCRIPTS = REPO_ROOT / "skills" / "auditing" / "scripts"
RELEASING_SCRIPTS = REPO_ROOT / "skills" / "releasing" / "scripts"
SKILLS_DIR = REPO_ROOT / "skills"
HOOKS_DIR = REPO_ROOT / "hooks"

def _bash_works():
    """Check that bash is genuinely usable (not just a broken WSL stub)."""
    bash = shutil.which("bash")
    if not bash:
        return False
    try:
        r = subprocess.run([bash, "-c", "echo ok"],
                           capture_output=True, timeout=5)
        return r.returncode == 0 and b"ok" in r.stdout
    except (OSError, subprocess.TimeoutExpired):
        return False

HAS_BASH = _bash_works()

EXPECTED_SKILLS = {
    "authoring", "auditing", "blueprinting", "optimizing",
    "releasing", "scaffolding", "using-bundles-forge",
}


class TestAuditSkillProjectMode(unittest.TestCase):
    """Tests for skills/auditing/scripts/audit_skill.py in project-level mode."""

    def _run_project(self, *extra_args):
        return subprocess.run(
            [sys.executable, str(AUDITING_SCRIPTS / "audit_skill.py"),
             "--all", *extra_args, str(REPO_ROOT)],
            capture_output=True, text=True
        )

    def test_project_mode_runs_without_error(self):
        result = self._run_project()
        self.assertIn("Skill Quality Audit", result.stdout)

    def test_project_mode_autodetect(self):
        result = subprocess.run(
            [sys.executable, str(AUDITING_SCRIPTS / "audit_skill.py"), str(REPO_ROOT)],
            capture_output=True, text=True
        )
        self.assertIn("Skill Quality Audit", result.stdout)

    def test_project_mode_json_output(self):
        result = self._run_project("--json")
        data = json.loads(result.stdout)
        self.assertIn("skills", data)
        self.assertIn("summary", data)
        self.assertIsInstance(data["skills"], list)
        self.assertGreater(len(data["skills"]), 0)

    def test_project_mode_finds_expected_skills(self):
        result = self._run_project("--json")
        data = json.loads(result.stdout)
        skill_names = {s["skill"] for s in data["skills"]}
        expected = {"blueprinting", "scaffolding", "authoring", "auditing",
                    "optimizing", "releasing",
                    "using-bundles-forge"}
        self.assertTrue(expected.issubset(skill_names),
                        f"Missing skills: {expected - skill_names}")

    def test_project_mode_no_deleted_skills(self):
        result = self._run_project("--json")
        data = json.loads(result.stdout)
        skill_names = {s["skill"] for s in data["skills"]}
        removed = {"scanning-security", "iterating-feedback", "managing-versions"}
        self.assertTrue(removed.isdisjoint(skill_names),
                        f"Deleted skills still present: {removed & skill_names}")


class TestScanSecurity(unittest.TestCase):
    """Tests for skills/auditing/scripts/scan_security.py"""

    def test_scan_runs_without_crash(self):
        result = subprocess.run(
            [sys.executable, str(AUDITING_SCRIPTS / "scan_security.py"), str(REPO_ROOT)],
            capture_output=True, text=True
        )
        self.assertIn("Security Scan", result.stdout)

    def test_scan_json_output(self):
        result = subprocess.run(
            [sys.executable, str(AUDITING_SCRIPTS / "scan_security.py"), "--json", str(REPO_ROOT)],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        self.assertIn("files", data)
        self.assertIn("summary", data)
        self.assertIsInstance(data["files"], list)

    def test_scan_classifies_file_types(self):
        result = subprocess.run(
            [sys.executable, str(AUDITING_SCRIPTS / "scan_security.py"), "--json", str(REPO_ROOT)],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        types_found = {f["type"] for f in data["files"]}
        self.assertIn("hook_script", types_found)
        self.assertIn("skill_content", types_found)

    def test_findings_have_confidence(self):
        result = subprocess.run(
            [sys.executable, str(AUDITING_SCRIPTS / "scan_security.py"), "--json", str(REPO_ROOT)],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        all_findings = [f for fr in data["files"] for f in fr["findings"]]
        for f in all_findings:
            self.assertIn(f.get("confidence"), ("deterministic", "suspicious"),
                          f"Finding {f.get('check_id')} missing valid confidence")

    def test_suspicious_findings_affect_exit_code(self):
        """Suspicious findings should affect exit code (at least exit 1)."""
        result = subprocess.run(
            [sys.executable, str(AUDITING_SCRIPTS / "scan_security.py"), "--json", str(REPO_ROOT)],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        s = data["summary"]
        has_suspicious = (s.get("suspicious_critical", 0) > 0
                          or s.get("suspicious_warning", 0) > 0)
        if has_suspicious:
            self.assertGreater(result.returncode, 0,
                               "Suspicious findings should cause non-zero exit")

    def test_summary_has_suspicious_counts(self):
        result = subprocess.run(
            [sys.executable, str(AUDITING_SCRIPTS / "scan_security.py"), "--json", str(REPO_ROOT)],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        s = data["summary"]
        self.assertIn("suspicious_critical", s)
        self.assertIn("suspicious_warning", s)


class TestAuditProject(unittest.TestCase):
    """Tests for skills/auditing/scripts/audit_project.py"""

    def test_audit_runs_without_crash(self):
        result = subprocess.run(
            [sys.executable, str(AUDITING_SCRIPTS / "audit_project.py"), str(REPO_ROOT)],
            capture_output=True, text=True
        )
        self.assertIn("Bundle-Plugin Audit", result.stdout)

    def test_audit_json_output(self):
        result = subprocess.run(
            [sys.executable, str(AUDITING_SCRIPTS / "audit_project.py"), "--json", str(REPO_ROOT)],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        self.assertIn("categories", data)
        self.assertIn("status", data)
        self.assertIn(data["status"], ("PASS", "WARN", "FAIL"))

    def test_audit_has_all_categories(self):
        result = subprocess.run(
            [sys.executable, str(AUDITING_SCRIPTS / "audit_project.py"), "--json", str(REPO_ROOT)],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        expected_cats = {"structure", "manifests", "version_sync",
                         "skill_quality", "cross_references", "hooks",
                         "documentation", "security"}
        actual_cats = set(data["categories"].keys())
        self.assertTrue(expected_cats.issubset(actual_cats),
                        f"Missing categories: {expected_cats - actual_cats}")


class TestGraphRules(unittest.TestCase):
    """Tests for G1-G4 graph analysis rules in audit_skill.py."""

    def _get_lint_data(self):
        result = subprocess.run(
            [sys.executable, str(AUDITING_SCRIPTS / "audit_skill.py"),
             "--all", "--json", str(REPO_ROOT)],
            capture_output=True, text=True
        )
        return json.loads(result.stdout)

    def test_lint_json_has_graph_key(self):
        """lint --json output includes 'graph' key when >=2 skills."""
        data = self._get_lint_data()
        self.assertIn("graph", data,
                       "lint JSON output missing 'graph' key")
        self.assertIsInstance(data["graph"], list)

    def test_no_undeclared_circular_dependencies(self):
        """G1: no undeclared circular dependency findings (warning level)."""
        data = self._get_lint_data()
        undeclared_cycles = [
            f for f in data["graph"]
            if f["check"] == "G1" and f["severity"] == "warning"
        ]
        self.assertEqual(undeclared_cycles, [],
                         f"Undeclared circular dependencies:\n"
                         + "\n".join(f["message"] for f in undeclared_cycles))

    def test_all_skills_reachable(self):
        """G2: all skills reachable from using-* entry points or declared direct-call."""
        data = self._get_lint_data()
        unreachable = [
            f for f in data["graph"]
            if f["check"] == "G2"
        ]
        self.assertEqual(unreachable, [],
                         f"Unreachable skills:\n"
                         + "\n".join(f["message"] for f in unreachable))

    def test_terminal_skills_have_outputs(self):
        """G3: terminal skills have ## Outputs section."""
        data = self._get_lint_data()
        missing_outputs = [
            f for f in data["graph"]
            if f["check"] == "G3"
        ]
        self.assertEqual(missing_outputs, [],
                         f"Terminal skills without Outputs:\n"
                         + "\n".join(f["message"] for f in missing_outputs))

    def test_referenced_skills_have_inputs(self):
        """G4: skills with incoming refs have ## Inputs section."""
        data = self._get_lint_data()
        missing_inputs = [
            f for f in data["graph"]
            if f["check"] == "G4"
        ]
        self.assertEqual(missing_inputs, [],
                         f"Referenced skills without Inputs:\n"
                         + "\n".join(f["message"] for f in missing_inputs))


class TestArtifactMatching(unittest.TestCase):
    """Tests for G5 artifact identifier matching."""

    def test_g5_no_critical_mismatches(self):
        """G5: workflow edges have matching artifact IDs (info level only)."""
        result = subprocess.run(
            [sys.executable, str(AUDITING_SCRIPTS / "audit_skill.py"),
             "--all", "--json", str(REPO_ROOT)],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        g5_findings = [
            f for f in data.get("graph", [])
            if f["check"] == "G5"
        ]
        for f in g5_findings:
            self.assertEqual(f["severity"], "info",
                             f"G5 should be info-level: {f['message']}")


class TestCrossReferences(unittest.TestCase):
    """Verify cross-references resolve to existing skills."""

    def test_no_broken_crossrefs(self):
        result = subprocess.run(
            [sys.executable, str(AUDITING_SCRIPTS / "audit_skill.py"),
             "--all", "--json", str(REPO_ROOT)],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        broken = []
        for skill in data["skills"]:
            for finding in skill["findings"]:
                if finding["check"] == "X1":
                    broken.append(f"{skill['skill']}: {finding['message']}")
        self.assertEqual(broken, [], f"Broken cross-references:\n" + "\n".join(broken))


class TestSkillDiscovery(unittest.TestCase):
    """Verify all skills exist with valid SKILL.md and frontmatter.

    Python equivalent of test-skill-discovery.sh.
    """

    def test_skills_directory_exists(self):
        self.assertTrue(SKILLS_DIR.is_dir(), "skills/ directory missing")

    def test_all_expected_skills_present(self):
        for skill in EXPECTED_SKILLS:
            self.assertTrue(
                (SKILLS_DIR / skill).is_dir(),
                f"{skill}/ directory missing")

    def test_each_skill_has_skill_md(self):
        for skill in EXPECTED_SKILLS:
            self.assertTrue(
                (SKILLS_DIR / skill / "SKILL.md").is_file(),
                f"{skill}/SKILL.md missing")

    def test_each_skill_has_valid_frontmatter(self):
        for skill in EXPECTED_SKILLS:
            path = SKILLS_DIR / skill / "SKILL.md"
            if not path.is_file():
                continue
            content = path.read_text(encoding="utf-8")
            lines = content.splitlines()
            self.assertEqual(lines[0], "---",
                             f"{skill}/SKILL.md missing frontmatter opening ---")
            fm_end = None
            for i, line in enumerate(lines[1:], 1):
                if line == "---":
                    fm_end = i
                    break
            self.assertIsNotNone(fm_end,
                                 f"{skill}/SKILL.md missing frontmatter closing ---")
            fm_block = "\n".join(lines[1:fm_end])
            self.assertTrue(
                re.search(r"^name:", fm_block, re.MULTILINE),
                f"{skill}/SKILL.md missing name field")
            self.assertTrue(
                re.search(r"^description:", fm_block, re.MULTILINE),
                f"{skill}/SKILL.md missing description field")

    def test_directory_names_match_frontmatter(self):
        name_re = re.compile(r'^name:\s*"?([^"\n]+)"?\s*$', re.MULTILINE)
        for skill in EXPECTED_SKILLS:
            path = SKILLS_DIR / skill / "SKILL.md"
            if not path.is_file():
                continue
            content = path.read_text(encoding="utf-8")
            end = content.index("\n---", 1)
            fm_block = content[:end]
            m = name_re.search(fm_block)
            self.assertIsNotNone(m, f"{skill}/SKILL.md has no parsable name field")
            self.assertEqual(m.group(1).strip(), skill,
                             f"{skill} directory vs frontmatter name '{m.group(1).strip()}'")


class TestBootstrapInjection(unittest.TestCase):
    """Verify session-start hook produces valid platform-appropriate JSON.

    Python equivalent of test-bootstrap-injection.sh.
    Pure-Python simulation always runs on all platforms; bash execution tests
    run as additional validation when bash is available.
    """

    def test_hook_script_exists(self):
        self.assertTrue(
            (HOOKS_DIR / "session-start").is_file(),
            "hooks/session-start missing")

    def test_hook_references_bootstrap_skill(self):
        content = (HOOKS_DIR / "session-start").read_text(encoding="utf-8")
        self.assertIn("using-bundles-forge/SKILL.md", content)

    @staticmethod
    def _simulate_hook(platform=None):
        """Pure-Python simulation of hooks/session-start logic."""
        skill_path = REPO_ROOT / "skills" / "using-bundles-forge" / "SKILL.md"
        content = skill_path.read_text(encoding="utf-8")
        escaped = (content.replace("\\", "\\\\")
                          .replace('"', '\\"')
                          .replace("\n", "\\n")
                          .replace("\r", "\\r")
                          .replace("\t", "\\t"))
        session_ctx = (
            "<EXTREMELY_IMPORTANT>\\nYou have bundles-forge skills loaded."
            "\\n\\n**Below is the full content of your "
            "'bundles-forge:using-bundles-forge' skill. For all other skills, "
            "use the 'Skill' tool:**\\n\\n"
            f"{escaped}\\n</EXTREMELY_IMPORTANT>")
        if platform == "cursor":
            return json.dumps({"additional_context": session_ctx})
        elif platform == "claude":
            return json.dumps({"hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": session_ctx}})
        else:
            return session_ctx

    def _run_hook(self, **extra_env):
        """Run the actual bash hook with the given env vars."""
        env = {**os.environ, **extra_env}
        for key in ("CURSOR_PLUGIN_ROOT", "CLAUDE_PLUGIN_ROOT"):
            if key not in extra_env:
                env.pop(key, None)
        return subprocess.run(
            ["bash", str(HOOKS_DIR / "session-start")],
            capture_output=True, env=env, encoding="utf-8", errors="replace")

    def test_claude_output_is_valid_json(self):
        output = self._simulate_hook(platform="claude")
        try:
            json.loads(output)
        except json.JSONDecodeError:
            self.fail("Claude Code hook output is not valid JSON")

    def test_cursor_output_is_valid_json(self):
        output = self._simulate_hook(platform="cursor")
        try:
            json.loads(output)
        except json.JSONDecodeError:
            self.fail("Cursor hook output is not valid JSON")

    def test_fallback_output_is_plain_text(self):
        """When neither platform env var is set, output is plain text."""
        output = self._simulate_hook()
        self.assertIn("EXTREMELY_IMPORTANT", output)
        self.assertNotIn("hookSpecificOutput", output,
                         "Fallback should not use Claude Code JSON")
        self.assertNotIn("additional_context", output,
                         "Fallback should not use Cursor JSON")

    def test_claude_output_contains_bootstrap_content(self):
        output = self._simulate_hook(platform="claude")
        self.assertIn("bundles-forge", output)

    def test_platform_appropriate_json_structure(self):
        cursor_output = self._simulate_hook(platform="cursor")
        self.assertIn("additional_context", cursor_output,
                       "Cursor output missing additional_context format")

        claude_output = self._simulate_hook(platform="claude")
        self.assertIn("hookSpecificOutput", claude_output,
                       "Claude Code output missing hookSpecificOutput format")

    @unittest.skipUnless(HAS_BASH, "bash not available")
    def test_bash_claude_output_is_valid_json(self):
        """Additional validation: run actual bash hook for Claude Code."""
        result = self._run_hook(CLAUDE_PLUGIN_ROOT=str(REPO_ROOT))
        self.assertEqual(result.returncode, 0, f"Hook exited {result.returncode}")
        try:
            json.loads(result.stdout)
        except json.JSONDecodeError:
            self.fail("Bash Claude Code hook output is not valid JSON")

    @unittest.skipUnless(HAS_BASH, "bash not available")
    def test_bash_cursor_output_is_valid_json(self):
        """Additional validation: run actual bash hook for Cursor."""
        result = self._run_hook(CURSOR_PLUGIN_ROOT=str(REPO_ROOT))
        self.assertEqual(result.returncode, 0, f"Hook exited {result.returncode}")
        try:
            json.loads(result.stdout)
        except json.JSONDecodeError:
            self.fail("Bash Cursor hook output is not valid JSON")


class TestVersionSync(unittest.TestCase):
    """Verify version consistency across all declared files.

    Python equivalent of test-version-sync.sh.
    """

    VERSION_BUMP_CONFIG = REPO_ROOT / ".version-bump.json"

    def test_version_bump_config_exists(self):
        self.assertTrue(self.VERSION_BUMP_CONFIG.is_file(),
                        ".version-bump.json missing")

    def test_all_declared_files_exist(self):
        config = json.loads(self.VERSION_BUMP_CONFIG.read_text(encoding="utf-8"))
        for entry in config["files"]:
            path = REPO_ROOT / entry["path"]
            self.assertTrue(path.is_file(), f"{entry['path']} missing")

    def test_bump_version_script_exists(self):
        self.assertTrue(
            (RELEASING_SCRIPTS / "bump_version.py").is_file(),
            "skills/releasing/scripts/bump_version.py missing")

    def test_no_version_drift(self):
        result = subprocess.run(
            [sys.executable, str(RELEASING_SCRIPTS / "bump_version.py"), "--check"],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(result.returncode, 0,
                         f"Version drift detected:\n{result.stdout}\n{result.stderr}")
        self.assertIn("in sync", result.stdout)


if __name__ == "__main__":
    unittest.main()
