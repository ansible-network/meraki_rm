"""Colocated tests for UserConfigTemplate — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import config_template


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserConfigTemplate can be constructed with all fields."""

    def test_defaults(self):
        obj = config_template.UserConfigTemplate()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserConfigTemplate -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = config_template.UserConfigTemplate(
            config_template_id='config_template_id_val',
            name='name_val',
            product_types=['item1', 'item2'],
            time_zone='time_zone_val',
            copy_from_network_id='copy_from_network_id_val',
        )
        api = user.to_api(_ctx())

        assert api.id == user.config_template_id
        assert api.name == user.name
        assert api.productTypes == user.product_types
        assert api.timeZone == user.time_zone
        assert api.copyFromNetworkId == user.copy_from_network_id

    def test_none_fields_omitted(self):
        user = config_template.UserConfigTemplate(config_template_id='config_template_id_val')
        api = user.to_api(_ctx())
        assert api.id == user.config_template_id
        assert getattr(api, 'name', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = config_template.UserConfigTemplate(organization_id='organization_id_val', config_template_id='config_template_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'organization_id' not in api_field_names or getattr(api, 'organization_id', None) is None

