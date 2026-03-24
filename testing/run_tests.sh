#!/usr/bin/env bash
# netKB test runner — automated + optional live tests

cd "$(dirname "$0")/.."
PYTHON="netkb/bin/python"
PASSED=0
FAILED=0
SKIPPED=0

GREEN=$'\033[0;32m'
RED=$'\033[0;31m'
YELLOW=$'\033[0;33m'
BOLD=$'\033[1m'
NC=$'\033[0m'

run_suite() {
    local id="$1"
    local name="$2"
    local path="$3"
    shift 3
    local extra_args=("$@")

    printf "%s[%s] %s%s ... " "$BOLD" "$id" "$name" "$NC"
    output=$($PYTHON -m pytest "$path" "${extra_args[@]}" --tb=short -q 2>&1) || true

    if echo "$output" | grep -qE "failed"; then
        printf "%sFAIL%s\n" "$RED" "$NC"
        echo "$output" | grep -E "FAILED|AssertionError" | head -5
        FAILED=$((FAILED + 1))
    elif echo "$output" | grep -q "skipped"; then
        printf "%sSKIP%s\n" "$YELLOW" "$NC"
        SKIPPED=$((SKIPPED + 1))
    else
        printf "%sPASS%s\n" "$GREEN" "$NC"
        PASSED=$((PASSED + 1))
    fi
}

echo ""
echo "========================================="
echo "  netKB Test Runner"
echo "========================================="
echo ""

# ── Automated Tests ──────────────────────────────────────────────────────
printf "%sAutomated Tests%s\n" "$BOLD" "$NC"
echo "-----------------------------------------"
run_suite "UT-001" "Input Model Validation"   "testing/automated/test_input_models.py"
run_suite "UT-002" "Platform Map"             "testing/automated/test_platform_map.py"
run_suite "UT-003" "Tool Layer"               "testing/automated/test_tools.py"
run_suite "UT-004" "Transport Dispatcher"     "testing/automated/test_transport.py"
run_suite "UT-005" "Vault Client"             "testing/automated/test_vault.py"
run_suite "UT-006" "Ingest Helpers"           "testing/automated/test_ingest.py"
run_suite "UT-007" "NetBox Loader"            "testing/automated/test_netbox.py"
run_suite "UT-008" "SSH Layer"               "testing/automated/test_ssh.py"
run_suite "UT-009" "MCP Server Registration" "testing/automated/test_mcp_server.py"
run_suite "IT-001" "RAG Pipeline"             "testing/automated/test_rag_pipeline.py"

# ── Live Tests ───────────────────────────────────────────────────────────
echo ""
printf "%sLive Tests%s\n" "$BOLD" "$NC"
echo "-----------------------------------------"
if [[ "${1:-}" == "--live" ]]; then
    run_suite "LT-001" "Platform Coverage (5 vendors)" "testing/live/test_platform_coverage.py" "--live"
    echo ""
    echo "Report: testing/live/platform_coverage_results.md"
else
    printf "%s[LT-001] Platform Coverage%s ... %sSKIP%s (pass --live to enable)\n" "$BOLD" "$NC" "$YELLOW" "$NC"
    SKIPPED=$((SKIPPED + 1))
fi

# ── Summary ──────────────────────────────────────────────────────────────
echo ""
echo "========================================="
TOTAL=$((PASSED + FAILED + SKIPPED))
printf "  %sPassed: %d%s  %sFailed: %d%s  %sSkipped: %d%s  Total: %d\n" \
    "$GREEN" "$PASSED" "$NC" "$RED" "$FAILED" "$NC" "$YELLOW" "$SKIPPED" "$NC" "$TOTAL"
echo "========================================="

[ "$FAILED" -eq 0 ] && exit 0 || exit 1
