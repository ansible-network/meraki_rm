"""Unit tests for check mode (--check) and diff mode (--diff) support.

Tests the set-theoretic _predict_after() methods and diff output generation
in BaseResourceActionPlugin without requiring the Ansible runtime.
"""

from __future__ import annotations

import yaml
import pytest

from plugins.action.base_action import BaseResourceActionPlugin


# ---------------------------------------------------------------------------
# Minimal subclass for testing prediction logic
# ---------------------------------------------------------------------------

class FakePlugin(BaseResourceActionPlugin):
    MODULE_NAME = 'test_resource'
    SCOPE_PARAM = 'network_id'
    CANONICAL_KEY = 'item_id'
    SUPPORTS_DELETE = True


class SingletonPlugin(BaseResourceActionPlugin):
    MODULE_NAME = 'test_singleton'
    SCOPE_PARAM = 'network_id'
    CANONICAL_KEY = None
    SUPPORTS_DELETE = False


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def plugin():
    p = FakePlugin.__new__(FakePlugin)
    return p


@pytest.fixture
def singleton():
    p = SingletonPlugin.__new__(SingletonPlugin)
    return p


BEFORE = [
    {'item_id': '1', 'name': 'Alpha', 'enabled': True},
    {'item_id': '2', 'name': 'Beta', 'enabled': False},
    {'item_id': '3', 'name': 'Gamma', 'enabled': True},
]

SINGLETON_BEFORE = [
    {'name': 'Current', 'setting_a': 10, 'setting_b': 20},
]


# ===================================================================
# _predict_merged
# ===================================================================

class TestPredictMerged:
    """C' = C ∪ D — additive merge, never removes."""

    def test_update_existing_item(self, plugin):
        config = [{'item_id': '1', 'name': 'Alpha-Updated'}]
        result = plugin._predict_after('merged', BEFORE, config)
        assert len(result) == 3
        item1 = next(r for r in result if r['item_id'] == '1')
        assert item1['name'] == 'Alpha-Updated'
        assert item1['enabled'] is True

    def test_add_new_item(self, plugin):
        config = [{'item_id': '4', 'name': 'Delta', 'enabled': True}]
        result = plugin._predict_after('merged', BEFORE, config)
        assert len(result) == 4
        assert any(r['item_id'] == '4' for r in result)

    def test_no_change_when_identical(self, plugin):
        config = [{'item_id': '1', 'name': 'Alpha', 'enabled': True}]
        result = plugin._predict_after('merged', BEFORE, config)
        assert not plugin._lists_differ(BEFORE, result)

    def test_none_fields_preserved(self, plugin):
        """None in desired means 'don't touch this field' — existing value preserved."""
        config = [{'item_id': '1', 'name': None, 'enabled': False}]
        result = plugin._predict_after('merged', BEFORE, config)
        item1 = next(r for r in result if r['item_id'] == '1')
        assert item1['enabled'] is False
        assert item1['name'] == 'Alpha'

    def test_merge_multiple_items(self, plugin):
        config = [
            {'item_id': '1', 'name': 'A-New'},
            {'item_id': '5', 'name': 'Epsilon'},
        ]
        result = plugin._predict_after('merged', BEFORE, config)
        assert len(result) == 4

    def test_singleton_merge(self, singleton):
        config = [{'setting_a': 99}]
        result = singleton._predict_after('merged', SINGLETON_BEFORE, config)
        assert len(result) == 1
        assert result[0]['setting_a'] == 99
        assert result[0]['setting_b'] == 20

    def test_empty_config_no_change(self, plugin):
        result = plugin._predict_after('merged', BEFORE, [])
        assert not plugin._lists_differ(BEFORE, result)


# ===================================================================
# _predict_replaced
# ===================================================================

class TestPredictReplaced:
    """C' = (C \\ K(D)) ∪ D — item-level replacement."""

    def test_replace_existing_item(self, plugin):
        config = [{'item_id': '1', 'name': 'Replaced'}]
        result = plugin._predict_after('replaced', BEFORE, config)
        assert len(result) == 3
        item1 = next(r for r in result if r['item_id'] == '1')
        assert item1 == {'item_id': '1', 'name': 'Replaced'}
        assert 'enabled' not in item1

    def test_untouched_items_preserved(self, plugin):
        config = [{'item_id': '1', 'name': 'Replaced'}]
        result = plugin._predict_after('replaced', BEFORE, config)
        item2 = next(r for r in result if r['item_id'] == '2')
        assert item2['name'] == 'Beta'
        assert item2['enabled'] is False

    def test_add_new_via_replace(self, plugin):
        config = [{'item_id': '4', 'name': 'New'}]
        result = plugin._predict_after('replaced', BEFORE, config)
        assert len(result) == 4

    def test_singleton_replace(self, singleton):
        config = [{'name': 'Replaced', 'setting_a': 50}]
        result = singleton._predict_after('replaced', SINGLETON_BEFORE, config)
        assert len(result) == 1
        assert result[0] == {'name': 'Replaced', 'setting_a': 50}


# ===================================================================
# _predict_overridden
# ===================================================================

class TestPredictOverridden:
    """C' = D — set equality."""

    def test_result_is_exactly_desired(self, plugin):
        config = [{'item_id': '1', 'name': 'Only-This'}]
        result = plugin._predict_after('overridden', BEFORE, config)
        assert len(result) == 1
        assert result[0]['item_id'] == '1'
        assert result[0]['name'] == 'Only-This'

    def test_extras_removed(self, plugin):
        config = [{'item_id': '1', 'name': 'Keep'}]
        result = plugin._predict_after('overridden', BEFORE, config)
        assert not any(r.get('item_id') == '2' for r in result)
        assert not any(r.get('item_id') == '3' for r in result)

    def test_empty_config_clears_all(self, plugin):
        result = plugin._predict_after('overridden', BEFORE, [])
        assert result == []

    def test_changed_when_different(self, plugin):
        config = [{'item_id': '1', 'name': 'Only-This'}]
        result = plugin._predict_after('overridden', BEFORE, config)
        assert plugin._lists_differ(BEFORE, result)

    def test_no_change_when_identical(self, plugin):
        result = plugin._predict_after('overridden', BEFORE, BEFORE)
        assert not plugin._lists_differ(BEFORE, result)


# ===================================================================
# _predict_deleted
# ===================================================================

class TestPredictDeleted:
    """C' = C \\ D — set difference."""

    def test_delete_specific_item(self, plugin):
        config = [{'item_id': '2'}]
        result = plugin._predict_after('deleted', BEFORE, config)
        assert len(result) == 2
        assert not any(r['item_id'] == '2' for r in result)

    def test_delete_multiple_items(self, plugin):
        config = [{'item_id': '1'}, {'item_id': '3'}]
        result = plugin._predict_after('deleted', BEFORE, config)
        assert len(result) == 1
        assert result[0]['item_id'] == '2'

    def test_delete_nonexistent_no_change(self, plugin):
        config = [{'item_id': '999'}]
        result = plugin._predict_after('deleted', BEFORE, config)
        assert len(result) == 3
        assert not plugin._lists_differ(BEFORE, result)

    def test_empty_config_deletes_all(self, plugin):
        result = plugin._predict_after('deleted', BEFORE, [])
        assert result == []

    def test_changed_when_items_deleted(self, plugin):
        config = [{'item_id': '1'}]
        result = plugin._predict_after('deleted', BEFORE, config)
        assert plugin._lists_differ(BEFORE, result)


# ===================================================================
# Diff output generation
# ===================================================================

class TestDiffOutput:
    """_build_result attaches YAML diff when diff mode is active."""

    def _make_plugin_with_diff(self, diff_enabled):
        p = FakePlugin.__new__(FakePlugin)
        p._manager_socket = None
        p._manager_authkey_b64 = None

        class FakeTask:
            diff = diff_enabled
        p._task = FakeTask()
        return p

    def test_diff_included_when_enabled(self):
        p = self._make_plugin_with_diff(True)
        result = p._build_result(
            failed=False, changed=True,
            before=[{'item_id': '1', 'name': 'Before'}],
            after=[{'item_id': '1', 'name': 'After'}],
        )
        assert 'diff' in result
        assert 'before' in result['diff']
        assert 'after' in result['diff']
        before_yaml = yaml.safe_load(result['diff']['before'])
        after_yaml = yaml.safe_load(result['diff']['after'])
        assert before_yaml[0]['name'] == 'Before'
        assert after_yaml[0]['name'] == 'After'

    def test_diff_excluded_when_disabled(self):
        p = self._make_plugin_with_diff(False)
        result = p._build_result(
            failed=False, changed=True,
            before=[{'item_id': '1'}],
            after=[{'item_id': '1'}],
        )
        assert 'diff' not in result

    def test_diff_excluded_when_no_before_after(self):
        p = self._make_plugin_with_diff(True)
        result = p._build_result(
            failed=False, changed=False,
            gathered=[{'item_id': '1'}],
        )
        assert 'diff' not in result

    def test_diff_excluded_on_error(self):
        p = self._make_plugin_with_diff(True)
        result = p._build_result(failed=True, msg='boom')
        assert 'diff' not in result


# ===================================================================
# Integration: predict + diff together
# ===================================================================

class TestCheckModeWithDiff:
    """Check mode prediction combined with diff output."""

    def test_overridden_check_with_diff(self):
        p = FakePlugin.__new__(FakePlugin)
        p._manager_socket = None
        p._manager_authkey_b64 = None

        class FakeTask:
            diff = True
        p._task = FakeTask()

        before = BEFORE
        config = [{'item_id': '1', 'name': 'Keep'}]
        after = p._predict_after('overridden', before, config)
        changed = p._lists_differ(before, after)

        result = p._build_result(
            failed=False, changed=changed,
            before=before, after=after, config=after,
        )
        assert result['changed'] is True
        assert len(result['after']) == 1
        assert 'diff' in result
        assert 'Alpha' in result['diff']['before']
        assert 'Keep' in result['diff']['after']
