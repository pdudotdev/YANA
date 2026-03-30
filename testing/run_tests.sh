#!/usr/bin/env bash
# YANA test runner — automated + optional live tests

cd "$(dirname "$0")/.."
PYTHON="yana/bin/python"

GREEN=$'\033[0;32m'
RED=$'\033[0;31m'
YELLOW=$'\033[0;33m'
BOLD=$'\033[1m'
NC=$'\033[0m'

echo ""
echo "========================================="
echo "  YANA Test Runner"
echo "========================================="
echo ""

# ── Automated Tests ──────────────────────────────────────────────────────
printf "%sAutomated Tests%s\n" "$BOLD" "$NC"
echo "-----------------------------------------"
$PYTHON -m pytest testing/automated/test_suite.py -v --tb=short --timeout=30
AUTO_EXIT=$?

# ── Live Tests ───────────────────────────────────────────────────────────
echo ""
printf "%sLive Tests%s\n" "$BOLD" "$NC"
echo "-----------------------------------------"
if [[ "${1:-}" == "--live" ]]; then
    $PYTHON -m pytest testing/live/test_platform_coverage.py --live -v --tb=short --timeout=60
    LIVE_EXIT=$?
    echo ""
    echo "Report: testing/live/platform_coverage_results.md"
else
    printf "%s[LT-001] Platform Coverage%s ... %sSKIP%s (pass --live to enable)\n" "$BOLD" "$NC" "$YELLOW" "$NC"
    LIVE_EXIT=0
fi

echo ""
echo "========================================="
[ "$AUTO_EXIT" -eq 0 ] && [ "$LIVE_EXIT" -eq 0 ] && exit 0 || exit 1
