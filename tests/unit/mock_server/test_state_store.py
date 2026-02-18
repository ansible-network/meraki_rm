"""Unit tests for the mock server state store."""

import sys
from pathlib import Path

_project_root = Path(__file__).parent.parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from tools.mock_server.state_store import StateStore


class TestStateStoreCreate:

    def test_create_with_primary_key(self):
        store = StateStore()
        result = store.create('vlans', 'vlanId', {'vlanId': '100', 'name': 'Test'})

        assert result['vlanId'] == '100'
        assert result['name'] == 'Test'

    def test_create_auto_id(self):
        store = StateStore()
        result = store.create('vlans', None, {'name': 'NoKey'})

        assert 'id' in result
        assert result['name'] == 'NoKey'

    def test_create_with_id_field(self):
        store = StateStore()
        result = store.create('admins', 'id', {'id': 'admin1', 'name': 'Jane'})

        assert result['id'] == 'admin1'


class TestStateStoreGet:

    def test_get_existing(self):
        store = StateStore()
        store.create('vlans', 'vlanId', {'vlanId': '100', 'name': 'Test'})

        result = store.get('vlans', '100')
        assert result is not None
        assert result['name'] == 'Test'

    def test_get_missing(self):
        store = StateStore()
        assert store.get('vlans', '999') is None

    def test_get_returns_copy(self):
        """Modifying the returned dict should not affect the store."""
        store = StateStore()
        store.create('vlans', 'vlanId', {'vlanId': '1', 'name': 'Original'})

        result = store.get('vlans', '1')
        result['name'] = 'Modified'

        original = store.get('vlans', '1')
        assert original['name'] == 'Original'


class TestStateStoreList:

    def test_list_all(self):
        store = StateStore()
        store.create('vlans', 'vlanId', {'vlanId': '100', 'name': 'A'})
        store.create('vlans', 'vlanId', {'vlanId': '200', 'name': 'B'})

        items = store.list('vlans')
        assert len(items) == 2

    def test_list_filtered(self):
        store = StateStore()
        store.create('vlans', 'vlanId', {'vlanId': '100', 'networkId': 'N1'})
        store.create('vlans', 'vlanId', {'vlanId': '200', 'networkId': 'N2'})

        items = store.list('vlans', {'networkId': 'N1'})
        assert len(items) == 1
        assert items[0]['vlanId'] == '100'

    def test_list_empty_type(self):
        store = StateStore()
        assert store.list('nonexistent') == []


class TestStateStoreUpdate:

    def test_update_existing(self):
        store = StateStore()
        store.create('vlans', 'vlanId', {'vlanId': '100', 'name': 'Old'})

        result = store.update('vlans', '100', {'name': 'New'})
        assert result is not None
        assert result['name'] == 'New'
        assert result['vlanId'] == '100'

    def test_update_missing(self):
        store = StateStore()
        assert store.update('vlans', '999', {'name': 'New'}) is None

    def test_update_merges(self):
        store = StateStore()
        store.create('vlans', 'vlanId', {'vlanId': '1', 'name': 'A', 'subnet': '10.0.0.0/8'})

        store.update('vlans', '1', {'name': 'B'})
        result = store.get('vlans', '1')

        assert result['name'] == 'B'
        assert result['subnet'] == '10.0.0.0/8'


class TestStateStoreDelete:

    def test_delete_existing(self):
        store = StateStore()
        store.create('vlans', 'vlanId', {'vlanId': '100'})

        assert store.delete('vlans', '100') is True
        assert store.get('vlans', '100') is None

    def test_delete_missing(self):
        store = StateStore()
        assert store.delete('vlans', '999') is False


class TestStateStoreClear:

    def test_clear_all(self):
        store = StateStore()
        store.create('vlans', 'vlanId', {'vlanId': '100'})
        store.create('admins', 'id', {'id': '1'})

        store.clear()

        assert store.list('vlans') == []
        assert store.list('admins') == []

    def test_clear_type(self):
        store = StateStore()
        store.create('vlans', 'vlanId', {'vlanId': '100'})
        store.create('admins', 'id', {'id': '1'})

        store.clear('vlans')

        assert store.list('vlans') == []
        assert len(store.list('admins')) == 1
