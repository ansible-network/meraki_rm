#!/usr/bin/env bash
# Run all molecule scenarios in batches of 10. Stops at first failure.
# Usage:
#   ./tools/run_all_scenarios.sh          # run all batches
#   ./tools/run_all_scenarios.sh 3        # resume from batch 3
set -euo pipefail

BATCH_SIZE=10
START_BATCH=${1:-1}

cd /home/bthornto/github/openapi_module
source venv/bin/activate
export MOLECULE_GLOB="extensions/molecule/**/molecule.yml"

molecule reset --all 2>/dev/null || true
pkill -f "tools.mock_server.server" 2>/dev/null || true
sleep 1
rm -rf /run/user/1000/meraki_rm 2>/dev/null || true

SCENARIOS=($(find extensions/molecule -name molecule.yml \
    -not -path "*/default/*" \
    | sed 's|extensions/molecule/||; s|/molecule.yml||' | sort))

TOTAL=${#SCENARIOS[@]}
BATCHES=$(( (TOTAL + BATCH_SIZE - 1) / BATCH_SIZE ))

echo "=== $TOTAL scenarios in $BATCHES batches of $BATCH_SIZE ==="
echo ""

for (( b=START_BATCH; b<=BATCHES; b++ )); do
    offset=$(( (b - 1) * BATCH_SIZE ))
    batch=("${SCENARIOS[@]:$offset:$BATCH_SIZE}")

    echo "=== Batch $b/$BATCHES ==="
    printf '  %s\n' "${batch[@]}"
    echo ""

    args=()
    for s in "${batch[@]}"; do
        args+=(-s "$s")
    done

    molecule test "${args[@]}"

    echo ""
    echo "=== Batch $b PASSED ==="
    echo ""
done

echo "========================================"
echo "ALL $TOTAL scenarios PASSED"
echo "========================================"
