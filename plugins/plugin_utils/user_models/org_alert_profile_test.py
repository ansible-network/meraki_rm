"""Colocated tests for UserOrgAlertProfile — forward transform & scope exclusion."""

from dataclasses import fields as dc_fields
from . import org_alert_profile


def _ctx():
    return {'manager': None, 'cache': {}}


class TestInstantiation:
    """Verify UserOrgAlertProfile can be constructed with all fields."""

    def test_defaults(self):
        obj = org_alert_profile.UserOrgAlertProfile()
        for f in dc_fields(obj):
            if f.name.startswith('_'):
                continue
            assert getattr(obj, f.name) is None


class TestForwardTransform:
    """UserOrgAlertProfile -> API (to_api) field mapping."""

    def test_mapped_fields(self):
        user = org_alert_profile.UserOrgAlertProfile(
            alert_config_id='alert_config_id_val',
            type='type_val',
            enabled=True,
            alert_condition={'enabled': True},
            recipients={'enabled': True},
            network_tags=['item1', 'item2'],
            description='description_val',
        )
        api = user.to_api(_ctx())

        assert api.id == user.alert_config_id
        assert api.type == user.type
        assert api.enabled == user.enabled
        assert api.alertCondition == user.alert_condition
        assert api.recipients == user.recipients
        assert api.networkTags == user.network_tags
        assert api.description == user.description

    def test_none_fields_omitted(self):
        user = org_alert_profile.UserOrgAlertProfile(alert_config_id='alert_config_id_val')
        api = user.to_api(_ctx())
        assert api.id == user.alert_config_id
        assert getattr(api, 'type', None) is None


class TestScopeExclusion:
    """Scope params must not appear in API output."""

    def test_scope_not_in_api(self):
        user = org_alert_profile.UserOrgAlertProfile(organization_id='organization_id_val', alert_config_id='alert_config_id_val')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in dc_fields(api)}
        assert 'organization_id' not in api_field_names or getattr(api, 'organization_id', None) is None

