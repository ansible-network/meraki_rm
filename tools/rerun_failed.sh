#!/usr/bin/env bash
set -euo pipefail
cd /home/bthornto/github/openapi_module
source venv/bin/activate
export MOLECULE_GLOB="extensions/molecule/**/molecule.yml"

RESULTS_DIR="/tmp/molecule_rerun"
rm -rf "$RESULTS_DIR"
mkdir -p "$RESULTS_DIR"
rm -rf /run/user/1000/meraki_rm 2>/dev/null || true

FAILED_MODS="appliance_port auth_users device device_management_interface organization_admins organization_alert_profiles organization_branding_policies organization_config_templates organization_policy_objects organization_vpn sensor_alert_profiles switch_acl switch_stacks wireless_air_marshal_rules"

PASS=0
FAIL=0
FAIL_LIST=""

for mod in $FAILED_MODS; do
    echo "=== Testing $mod/merged ==="
    if molecule test -s "${mod}/merged" > "$RESULTS_DIR/${mod}.log" 2>&1; then
        echo "  PASS"
        PASS=$((PASS + 1))
    else
        echo "  FAIL"
        FAIL=$((FAIL + 1))
        FAIL_LIST="$FAIL_LIST $mod"
        tail -20 "$RESULTS_DIR/${mod}.log" > "$RESULTS_DIR/${mod}.err"
    fi
done

echo ""
echo "========================================"
echo "RERUN RESULTS: $PASS passed, $FAIL failed out of $((PASS + FAIL))"
echo "========================================"
if [ -n "$FAIL_LIST" ]; then
    echo "STILL FAILING:"
    for f in $FAIL_LIST; do
        echo "  - $f"
    done
fi
