#!/usr/bin/env bash
#
# test-version-sync.sh — verify version consistency across all declared files
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG="$REPO_ROOT/.version-bump.json"

PASS=0
FAIL=0

pass() { PASS=$((PASS + 1)); echo "  PASS: $1"; }
fail() { FAIL=$((FAIL + 1)); echo "  FAIL: $1"; }

echo "=== Version Sync Tests ==="
echo ""

echo "[1] .version-bump.json exists"
if [[ -f "$CONFIG" ]]; then
  pass ".version-bump.json exists"
else
  fail ".version-bump.json missing"
  echo "=== Results: $PASS passed, $FAIL failed ==="
  exit 1
fi

echo ""
echo "[2] All declared files exist"
jq -r '.files[] | .path' "$CONFIG" | while IFS= read -r fpath; do
  if [[ -f "$REPO_ROOT/$fpath" ]]; then
    pass "$fpath exists"
  else
    fail "$fpath missing"
  fi
done

echo ""
echo "[3] bump-version.sh exists"
if [[ -f "$REPO_ROOT/scripts/bump-version.sh" ]]; then
  pass "scripts/bump-version.sh exists"
else
  fail "scripts/bump-version.sh missing"
fi

echo ""
echo "[4] Version drift check (via bump-version.sh --check)"
if [[ -f "$REPO_ROOT/scripts/bump-version.sh" ]]; then
  if bash "$REPO_ROOT/scripts/bump-version.sh" --check > /dev/null 2>&1; then
    pass "no version drift detected"
  else
    fail "version drift detected"
  fi
else
  fail "cannot run drift check — script missing"
fi

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
exit $FAIL
