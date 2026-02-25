"""Action plugin for meraki_organization_alert_profiles module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'org_alert_profile'
    SCOPE_PARAM = 'organization_id'
    USER_MODEL = 'plugins.plugin_utils.user_models.org_alert_profile.UserOrgAlertProfile'
    SYSTEM_KEY = 'alert_config_id'
