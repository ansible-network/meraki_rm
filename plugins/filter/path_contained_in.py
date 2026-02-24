# Copyright (c) 2025, Cisco Systems, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Path-dict comparison filter for round-trip assertions.

Expects two flat dicts (e.g. from ansible.utils.to_paths): expected and actual.
Returns a dict with:
  - contained: bool — True if every expected key is in result with same value (string comparison)
  - missing: dict — expected keys not in result or with different value (key -> expected_value)
  - extras: dict — keys in result not in expected (server-populated fields)
"""

from __future__ import annotations


def _norm(v):
    """Normalize for comparison (e.g. string)."""
    if v is None:
        return ""
    return str(v).strip()


def path_contained_in(expected: dict, result: dict) -> dict:
    """Compare expected path-dict to result path-dict.

    :param expected: Flat dict of path -> value (user-provided)
    :param result: Flat dict of path -> value (module/API return)
    :returns: dict with 'contained', 'missing', 'extras'
    """
    if not isinstance(expected, dict):
        expected = {}
    if not isinstance(result, dict):
        result = {}

    missing = {}
    for key, exp_val in expected.items():
        if key not in result:
            missing[key] = exp_val
        elif _norm(result[key]) != _norm(exp_val):
            missing[key] = exp_val  # expected; could add actual for debugging

    extras = {
        k: result[k] for k in result
        if k not in expected and result[k] is not None
    }

    return {
        "contained": len(missing) == 0,
        "missing": missing,
        "extras": extras,
    }


class FilterModule:
    """Ansible filter plugin: path_contained_in."""

    def filters(self):
        return {"path_contained_in": path_contained_in}
