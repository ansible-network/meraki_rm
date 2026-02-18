#!/usr/bin/env bash
# Run every molecule scenario, collect pass/fail without stopping on first error.
# Starts mock server + manager once via molecule, loops through all scenarios.
set -uo pipefail

cd /home/bthornto/github/openapi_module
source venv/bin/activate
export MOLECULE_GLOB="extensions/molecule/**/molecule.yml"

RESULTS_DIR="/tmp/molecule_results"
rm -rf "$RESULTS_DIR"
mkdir -p "$RESULTS_DIR"

pkill -f "tools.mock_server.server" 2>/dev/null || true
sleep 1
rm -rf /run/user/1000/meraki_rm 2>/dev/null || true

echo "=== Starting infrastructure (default > create) ==="
molecule create 2>&1 | tee "$RESULTS_DIR/_create.log"
if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo "FATAL: default create failed"
    exit 1
fi
echo ""

SCENARIOS=$(find extensions/molecule -name molecule.yml -not -path "*/default/*" \
    | sed 's|extensions/molecule/||; s|/molecule.yml||' | sort)

PASS=0
FAIL=0
FAIL_LIST=""
TOTAL=0

for scenario in $SCENARIOS; do
    TOTAL=$((TOTAL + 1))
    echo -n "[$TOTAL] $scenario ... "
    LOG="$RESULTS_DIR/${scenario//\//_}.log"

    ok=true
    for phase in converge verify idempotence verify cleanup; do
        if ! molecule "$phase" -s "$scenario" >> "$LOG" 2>&1; then
            echo "FAIL ($phase)"
            FAIL=$((FAIL + 1))
            FAIL_LIST="$FAIL_LIST\n  - $scenario ($phase)"
            tail -30 "$LOG" > "${LOG%.log}.err"
            ok=false
            # still run cleanup on failure
            if [ "$phase" != "cleanup" ]; then
                molecule cleanup -s "$scenario" >> "$LOG" 2>&1 || true
            fi
            break
        fi
    done
    if $ok; then
        echo "PASS"
        PASS=$((PASS + 1))
    fi
done

echo ""
echo "=== Tearing down infrastructure ==="
molecule destroy 2>&1 | tee "$RESULTS_DIR/_destroy.log"

echo ""
echo "========================================"
echo "RESULTS: $PASS passed, $FAIL failed out of $TOTAL"
echo "========================================"
if [ -n "$FAIL_LIST" ]; then
    echo -e "FAILED:$FAIL_LIST"
fi
