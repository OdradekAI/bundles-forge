#!/usr/bin/env python3
"""Unit tests for internal modules: _parsing, _scoring, and bump_version helpers.

These test pure functions directly (no subprocess), complementing the
end-to-end tests in test_scripts.py and the graph fixture tests in
test_graph_fixtures.py.

Run: python tests/test_unit.py
Or:  python -m pytest tests/test_unit.py -v
"""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AUDITING_SCRIPTS = REPO_ROOT / "skills" / "auditing" / "scripts"
RELEASING_SCRIPTS = REPO_ROOT / "skills" / "releasing" / "scripts"

sys.path.insert(0, str(AUDITING_SCRIPTS))
sys.path.insert(0, str(RELEASING_SCRIPTS))

from _parsing import parse_frontmatter, estimate_tokens
from _scoring import compute_baseline_score, compute_weighted_average
from bump_version import _resolve_field_path, _set_field_path


# ---------------------------------------------------------------------------
# _parsing.parse_frontmatter
# ---------------------------------------------------------------------------

class TestParseFrontmatter(unittest.TestCase):
    """Edge cases for the zero-dependency YAML frontmatter parser."""

    def test_no_frontmatter_returns_none(self):
        content = "# Just a heading\n\nSome body text.\n"
        fm, body = parse_frontmatter(content)
        self.assertIsNone(fm)
        self.assertEqual(body, content)

    def test_empty_frontmatter_with_blank_line(self):
        content = "---\n\n---\nBody here.\n"
        fm, body = parse_frontmatter(content)
        self.assertIsNotNone(fm)
        self.assertEqual(fm, {})
        self.assertEqual(body.strip(), "Body here.")

    def test_empty_frontmatter_no_blank_line(self):
        """Adjacent --- markers with no content between them are not parsed."""
        content = "---\n---\nBody here.\n"
        fm, body = parse_frontmatter(content)
        self.assertIsNone(fm, "Parser requires at least one line between --- delimiters")

    def test_basic_key_value(self):
        content = "---\nname: my-skill\ndescription: Use when testing.\n---\nBody.\n"
        fm, body = parse_frontmatter(content)
        self.assertEqual(fm["name"], "my-skill")
        self.assertEqual(fm["description"], "Use when testing.")

    def test_quoted_values_stripped(self):
        content = '---\nname: "my-skill"\ndescription: \'Use when testing.\'\n---\nBody.\n'
        fm, _ = parse_frontmatter(content)
        self.assertEqual(fm["name"], "my-skill")
        self.assertEqual(fm["description"], "Use when testing.")

    def test_block_scalar_literal(self):
        content = "---\ndescription: |\n  Line one.\n  Line two.\n---\nBody.\n"
        fm, _ = parse_frontmatter(content)
        self.assertIn("Line one.", fm["description"])
        self.assertIn("Line two.", fm["description"])

    def test_block_scalar_folded(self):
        content = "---\ndescription: >\n  Folded line one.\n  Folded line two.\n---\nBody.\n"
        fm, _ = parse_frontmatter(content)
        self.assertIn("Folded line one.", fm["description"])
        self.assertIn("Folded line two.", fm["description"])

    def test_value_with_colon(self):
        content = "---\ndescription: Use when: testing things.\n---\nBody.\n"
        fm, _ = parse_frontmatter(content)
        self.assertEqual(fm["description"], "Use when: testing things.")

    def test_missing_closing_delimiter(self):
        content = "---\nname: broken\nNo closing delimiter.\n"
        fm, body = parse_frontmatter(content)
        self.assertIsNone(fm)
        self.assertEqual(body, content)

    def test_empty_value(self):
        content = "---\nname:\n---\nBody.\n"
        fm, _ = parse_frontmatter(content)
        self.assertEqual(fm["name"], "")

    def test_body_is_content_after_frontmatter(self):
        content = "---\nname: test\n---\nLine 1\nLine 2\n"
        _, body = parse_frontmatter(content)
        self.assertIn("Line 1", body)
        self.assertIn("Line 2", body)


# ---------------------------------------------------------------------------
# _parsing.estimate_tokens
# ---------------------------------------------------------------------------

class TestEstimateTokens(unittest.TestCase):
    """Token estimation with separate rates for code, tables, and prose."""

    def test_empty_input(self):
        self.assertEqual(estimate_tokens(""), 0)

    def test_pure_prose(self):
        prose = "This is a simple sentence with several words."
        tokens = estimate_tokens(prose)
        self.assertGreater(tokens, 0)
        word_count = len(prose.split())
        self.assertAlmostEqual(tokens, int(word_count * 1.3), delta=2)

    def test_pure_code_block(self):
        code = "```python\nfor i in range(10):\n    print(i)\n```"
        tokens = estimate_tokens(code)
        self.assertGreater(tokens, 0)

    def test_table_rows(self):
        table = "| Col1 | Col2 |\n|------|------|\n| a    | b    |\n"
        tokens = estimate_tokens(table)
        self.assertGreater(tokens, 0)

    def test_mixed_content(self):
        content = (
            "Some prose here.\n\n"
            "```python\nprint('hello')\n```\n\n"
            "| A | B |\n|---|---|\n| 1 | 2 |\n"
        )
        tokens = estimate_tokens(content)
        self.assertGreater(tokens, 0)


# ---------------------------------------------------------------------------
# _scoring.compute_baseline_score
# ---------------------------------------------------------------------------

class TestComputeBaselineScore(unittest.TestCase):
    """Scoring edge cases for the deterministic baseline formula."""

    def test_empty_findings(self):
        self.assertEqual(compute_baseline_score([]), 10)

    def test_all_info_no_penalty(self):
        findings = [
            {"check": "Q10", "severity": "info"},
            {"check": "Q11", "severity": "info"},
            {"check": "Q12", "severity": "info"},
        ]
        self.assertEqual(compute_baseline_score(findings), 10)

    def test_single_critical(self):
        findings = [{"check": "Q1", "severity": "critical"}]
        self.assertEqual(compute_baseline_score(findings), 7)

    def test_multiple_criticals_floor_at_zero(self):
        findings = [
            {"check": "Q1", "severity": "critical"},
            {"check": "Q2", "severity": "critical"},
            {"check": "Q3", "severity": "critical"},
            {"check": "Q4", "severity": "critical"},
        ]
        self.assertEqual(compute_baseline_score(findings), 0)

    def test_single_warning(self):
        findings = [{"check": "Q5", "severity": "warning"}]
        self.assertEqual(compute_baseline_score(findings), 9)

    def test_cap_per_id_true_limits_same_check(self):
        findings = [
            {"check": "Q7", "severity": "warning"},
            {"check": "Q7", "severity": "warning"},
            {"check": "Q7", "severity": "warning"},
            {"check": "Q7", "severity": "warning"},
            {"check": "Q7", "severity": "warning"},
        ]
        score = compute_baseline_score(findings, cap_per_id=True)
        self.assertEqual(score, 7)

    def test_cap_per_id_false_counts_each(self):
        findings = [
            {"check": "Q7", "severity": "warning"},
            {"check": "Q7", "severity": "warning"},
            {"check": "Q7", "severity": "warning"},
            {"check": "Q7", "severity": "warning"},
            {"check": "Q7", "severity": "warning"},
        ]
        score = compute_baseline_score(findings, cap_per_id=False)
        self.assertEqual(score, 5)

    def test_mixed_severities(self):
        findings = [
            {"check": "Q1", "severity": "critical"},
            {"check": "Q5", "severity": "warning"},
            {"check": "Q10", "severity": "info"},
        ]
        score = compute_baseline_score(findings)
        self.assertEqual(score, 6)

    def test_risk_field_fallback(self):
        """Security findings use 'risk' instead of 'severity'."""
        findings = [{"check": "SC1", "risk": "critical"}]
        self.assertEqual(compute_baseline_score(findings), 7)


# ---------------------------------------------------------------------------
# _scoring.compute_weighted_average
# ---------------------------------------------------------------------------

class TestComputeWeightedAverage(unittest.TestCase):
    """Weighted average with None handling and edge cases."""

    def test_empty_scores(self):
        self.assertEqual(compute_weighted_average({}, {}), 0.0)

    def test_all_none_scores(self):
        scores = {"a": None, "b": None}
        weights = {"a": 3, "b": 2}
        self.assertEqual(compute_weighted_average(scores, weights), 0.0)

    def test_single_category(self):
        scores = {"quality": 8}
        weights = {"quality": 2}
        self.assertEqual(compute_weighted_average(scores, weights), 8.0)

    def test_mixed_weights(self):
        scores = {"structure": 10, "quality": 6}
        weights = {"structure": 3, "quality": 2}
        expected = round((10 * 3 + 6 * 2) / (3 + 2), 1)
        self.assertEqual(
            compute_weighted_average(scores, weights), expected)

    def test_none_scores_excluded(self):
        scores = {"structure": 10, "quality": None, "security": 8}
        weights = {"structure": 3, "quality": 2, "security": 3}
        expected = round((10 * 3 + 8 * 3) / (3 + 3), 1)
        self.assertEqual(
            compute_weighted_average(scores, weights), expected)

    def test_default_weight_one(self):
        scores = {"unknown_cat": 7}
        weights = {}
        self.assertEqual(compute_weighted_average(scores, weights), 7.0)


# ---------------------------------------------------------------------------
# bump_version._resolve_field_path / _set_field_path
# ---------------------------------------------------------------------------

class TestFieldPathResolution(unittest.TestCase):
    """JSON field path traversal for version bump."""

    def test_simple_key(self):
        data = {"version": "1.0.0"}
        self.assertEqual(_resolve_field_path(data, "version"), "1.0.0")

    def test_nested_dict(self):
        data = {"package": {"version": "2.0.0"}}
        self.assertEqual(_resolve_field_path(data, "package.version"), "2.0.0")

    def test_array_index(self):
        data = {"plugins": [{"version": "3.0.0"}]}
        self.assertEqual(
            _resolve_field_path(data, "plugins.0.version"), "3.0.0")

    def test_missing_key_returns_none(self):
        data = {"version": "1.0.0"}
        self.assertIsNone(_resolve_field_path(data, "nonexistent"))

    def test_array_index_out_of_bounds(self):
        data = {"plugins": []}
        self.assertIsNone(_resolve_field_path(data, "plugins.0.version"))

    def test_type_mismatch_dict_expected(self):
        data = {"version": "1.0.0"}
        self.assertIsNone(_resolve_field_path(data, "version.sub"))

    def test_type_mismatch_list_expected(self):
        data = {"plugins": {"version": "1.0.0"}}
        self.assertIsNone(_resolve_field_path(data, "plugins.0"))

    def test_set_simple_key(self):
        data = {"version": "1.0.0"}
        _set_field_path(data, "version", "2.0.0")
        self.assertEqual(data["version"], "2.0.0")

    def test_set_nested_path(self):
        data = {"package": {"version": "1.0.0"}}
        _set_field_path(data, "package.version", "2.0.0")
        self.assertEqual(data["package"]["version"], "2.0.0")

    def test_set_array_element(self):
        data = {"plugins": [{"version": "1.0.0"}]}
        _set_field_path(data, "plugins.0.version", "2.0.0")
        self.assertEqual(data["plugins"][0]["version"], "2.0.0")


if __name__ == "__main__":
    unittest.main()
