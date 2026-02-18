"""Colocated tests for types.py — EndpointOperation, ResourceModuleStates, ModuleConfig."""

from dataclasses import fields, asdict

from .types import EndpointOperation, ResourceModuleStates, ModuleConfig


class TestEndpointOperation:
    """EndpointOperation construction and field access."""

    def test_minimal(self):
        op = EndpointOperation(path='/foo', method='GET', fields=[])
        assert op.path == '/foo'
        assert op.method == 'GET'
        assert op.fields == []
        assert op.path_params is None
        assert op.order == 0
        assert op.batch_eligible is True

    def test_full(self):
        op = EndpointOperation(
            path='/networks/{networkId}/vlans',
            method='POST',
            fields=['id', 'name'],
            path_params=['networkId'],
            path_param_aliases={'networkId': ['network_id']},
            required_for='create',
            depends_on='find',
            order=2,
            batch_eligible=False,
        )
        assert op.path_params == ['networkId']
        assert op.path_param_aliases == {'networkId': ['network_id']}
        assert op.required_for == 'create'
        assert op.depends_on == 'find'
        assert op.order == 2
        assert op.batch_eligible is False

    def test_asdict(self):
        op = EndpointOperation(path='/x', method='DELETE', fields=['a'])
        d = asdict(op)
        assert d['path'] == '/x'
        assert d['method'] == 'DELETE'
        assert d['fields'] == ['a']


class TestResourceModuleStates:
    """ResourceModuleStates defaults and overrides."""

    def test_defaults(self):
        s = ResourceModuleStates()
        assert s.merged is True
        assert s.replaced is False
        assert s.overridden is False
        assert s.deleted is True
        assert s.gathered is True

    def test_all_enabled(self):
        s = ResourceModuleStates(
            merged=True, replaced=True, overridden=True,
            deleted=True, gathered=True,
        )
        for f in fields(s):
            assert getattr(s, f.name) is True

    def test_field_count(self):
        assert len(fields(ResourceModuleStates())) == 5


class TestModuleConfig:
    """ModuleConfig construction and defaults."""

    def test_minimal(self):
        mc = ModuleConfig(
            name='vlan', domain='appliance',
            scope='network', scope_param='networkId',
        )
        assert mc.name == 'vlan'
        assert mc.primary_key is None
        assert isinstance(mc.states, ResourceModuleStates)

    def test_with_states(self):
        states = ResourceModuleStates(replaced=True, overridden=True)
        mc = ModuleConfig(
            name='admin', domain='organization',
            scope='organization', scope_param='organizationId',
            primary_key='adminId', states=states,
        )
        assert mc.primary_key == 'adminId'
        assert mc.states.replaced is True
        assert mc.states.overridden is True

    def test_field_names(self):
        expected = {'name', 'domain', 'scope', 'scope_param', 'primary_key', 'states'}
        actual = {f.name for f in fields(ModuleConfig)}
        assert expected == actual
